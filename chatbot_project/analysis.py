import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 시각화 스타일
plt.style.use("ggplot")
sns.set(font_scale=1.2)

# 평가 결과 JSON 로드
with open("qa_eval_result.json", "r") as f:
    raw_result = json.load(f)

# 평가 결과 추출
test_results = raw_result["test_results"]
processed = []

for case in test_results:
    product = case.get("context", [""])[0].split("제품명:")[-1].split("\n")[0].strip()  # 제품명 추출 시도
    input_text = case["input"]
    output = case["actual_output"]
    metrics = case["metrics_data"]

    result = {
        "question": input_text,
        "answer": output,
        "product": product,
        "passed": case["success"]
    }

    for m in metrics:
        metric_name = m["name"]
        result[f"{metric_name}_score"] = m["score"]
        result[f"{metric_name}_passed"] = m["success"]

    processed.append(result)

df = pd.DataFrame(processed)

# ✅ 제품별 통과율
pass_rate = df.groupby("product")["passed"].mean().sort_values(ascending=False)

plt.figure(figsize=(10, 6))
pass_rate.plot(kind="barh", color="skyblue")
plt.title("제품별 QA 통과율")
plt.xlabel("통과율")
plt.ylabel("제품명")
plt.tight_layout()
plt.savefig("통과율_제품별.png")
plt.close()

# ✅ 제품별 실패 건수
fail_count = df[df["passed"] == False].groupby("product").size().sort_values(ascending=True)

plt.figure(figsize=(10, 6))
fail_count.plot(kind="barh", color="salmon")
plt.title("제품별 실패 건수")
plt.xlabel("실패 수")
plt.ylabel("제품명")
plt.tight_layout()
plt.savefig("실패건수_제품별.png")
plt.close()

# ✅ 평가 지표별 평균 점수
metric_scores = [col for col in df.columns if col.endswith("_score")]
avg_scores = df[metric_scores].mean().sort_values(ascending=False)

plt.figure(figsize=(8, 4))
avg_scores.plot(kind="bar", color="orange")
plt.title("평가 지표별 평균 점수")
plt.ylabel("평균 점수")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("평가지표_평균점수.png")
plt.close()

# ✅ 평가 지표별 실패율
metric_fail_cols = [col for col in df.columns if col.endswith("_passed")]
metric_fail_rates = 1 - df[metric_fail_cols].mean()

plt.figure(figsize=(8, 4))
metric_fail_rates.plot(kind="bar", color="red")
plt.title("평가 지표별 실패율")
plt.ylabel("실패율")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("평가지표_실패율.png")
plt.close()

# ✅ 제품별 QA 수
qa_count = df["product"].value_counts().sort_values(ascending=True)
plt.figure(figsize=(10, 6))
qa_count.plot(kind="barh", color="green")
plt.title("제품별 QA 데이터 분포")
plt.xlabel("QA 개수")
plt.tight_layout()
plt.savefig("제품별_QA분포.png")
plt.close()

print("✅ 시각화 완료. 결과 이미지가 현재 디렉토리에 저장되었습니다.")

# 사진은 완성되면 파일로 다운로드