import os
import json
import re
import pandas as pd
from tqdm import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import seaborn as sns


# ✅ 1. JSON 구조 검사 및 필드 정제
def load_valid_qa_data(jsonl_path: str) -> list:
    valid_data = []
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f):
            try:
                item = json.loads(line)
                if all(k in item for k in ("question", "answer", "category", "product")):
                    if item["question"].strip() and item["answer"].strip():
                        valid_data.append(item)
            except json.JSONDecodeError:
                print(f"⚠️ JSON 오류 at line {idx}")
                continue
    return valid_data


# ✅ 2. 중복 제거 (TF-IDF + 코사인 유사도)
def deduplicate_df(df: pd.DataFrame, threshold: float = 0.9):
    vectorizer = TfidfVectorizer().fit_transform(df["question"])
    sim_matrix = cosine_similarity(vectorizer)

    to_drop = set()
    for i in range(len(sim_matrix)):
        for j in range(i + 1, len(sim_matrix)):
            if sim_matrix[i][j] > threshold:
                to_drop.add(j)
    return df.drop(df.index[list(to_drop)])


def recursive_deduplicate(df: pd.DataFrame, chunk_size=100, threshold=0.9):
    deduped_dfs = []
    for i in range(0, len(df), chunk_size):
        chunk = df.iloc[i:i + chunk_size]
        deduped_chunk = deduplicate_df(chunk, threshold=threshold)
        deduped_dfs.append(deduped_chunk)
    return pd.concat(deduped_dfs).reset_index(drop=True)


# ✅ 3. 카테고리 분포 시각화
def plot_category_distribution(df: pd.DataFrame):
    plt.figure(figsize=(8, 6))
    sns.countplot(data=df, x="category", order=df["category"].value_counts().index)
    plt.title("QA 카테고리 분포")
    plt.xlabel("Category")
    plt.ylabel("Count")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()


# ✅ 4. 제품별 QA 수 분포 시각화
def plot_product_distribution(df: pd.DataFrame, top_n=10):
    top_products = df["product"].value_counts().head(top_n)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_products.index, y=top_products.values)
    plt.title(f"제품별 QA 수 분포 (상위 {top_n}개)")
    plt.xlabel("Product")
    plt.ylabel("QA 개수")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# ✅ 5. 실행 메인
if __name__ == "__main__":
    input_path = "qa_dataset.jsonl"
    output_path = "qa_dataset_cleaned.jsonl"

    print("🔍 원본 데이터 로딩 중...")
    raw_data = load_valid_qa_data(input_path)
    df = pd.DataFrame(raw_data)
    print(f"✅ 원본 QA 개수: {len(df)}")

    print("🧹 중복 제거 중...")
    df_deduped = recursive_deduplicate(df)
    print(f"✅ 중복 제거 후 QA 개수: {len(df_deduped)}")

    print("📊 카테고리 분포 시각화 중...")
    plot_category_distribution(df_deduped)

    print("📦 제품별 QA 수 분포 시각화 중...")
    plot_product_distribution(df_deduped)

    print("💾 결과 저장 중...")
    df_deduped.to_json(output_path, orient="records", lines=True, force_ascii=False)
    print(f"🎉 저장 완료 → {output_path}")