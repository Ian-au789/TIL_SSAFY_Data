import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import matplotlib.font_manager as fm
import os

# 🔹 한글 폰트 설정 (예: Mac의 기본 폰트 사용 시)
plt.rcParams["font.family"] = "AppleGothic"
plt.rcParams["axes.unicode_minus"] = False

# 🔹 1. 평가 결과 로딩
qa_eval_df = pd.read_json("qa_eval_structured.jsonl", lines=True)

# 🔹 2. 실패한 메트릭스 리스트 합치기
def concat_failed_metrics(metrics_list):
    result = []
    for item in metrics_list:
        result.extend(item)
    return result

product_metrics = (
    qa_eval_df.groupby("product_name")["failed_metrics"]
    .apply(concat_failed_metrics)
    .reset_index()
)

product_metrics["failed_metrics"] = product_metrics["failed_metrics"].apply(
    lambda x: dict(Counter(x))
)

# 🔹 3. 누적 막대그래프 데이터 구성
categories = ["Hallucination", "Answer Relevancy", "Toxicity"]
product_names = product_metrics["product_name"]
category_counts = {category: [] for category in categories}

for metrics in product_metrics["failed_metrics"]:
    if isinstance(metrics, dict):
        for category in categories:
            category_counts[category].append(metrics.get(category, 0))
    else:
        for category in categories:
            category_counts[category].append(0)

# 🔹 4. 그래프 시각화
plt.figure(figsize=(14, 8))
bar_width = 0.8
x = range(len(product_names))

bottoms = [0] * len(product_names)
for category in categories:
    plt.bar(
        x,
        category_counts[category],
        bottom=bottoms,
        label=category,
    )
    bottoms = [b + c for b, c in zip(bottoms, category_counts[category])]

plt.xticks(x, product_names, rotation=90)
plt.xlabel("제품 이름")
plt.ylabel("실패한 메트릭스 수")
plt.title("제품 및 카테고리별 실패한 메트릭스 수")
plt.legend()
plt.tight_layout()

# 🔹 5. 저장
save_path = "fig_failed_metrics_by_product.png"
plt.savefig(save_path)
print(f"✅ 그래프 저장 완료: {save_path}")
plt.close()
