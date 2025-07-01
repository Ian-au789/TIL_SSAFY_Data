import json
import pandas as pd

# 평가 결과 JSON 불러오기
with open("qa_eval_result3.json", "r", encoding="utf-8") as f:
    eval_result_dict = json.load(f)

# 평가 결과 리스트
test_results = eval_result_dict["test_results"]

# 변환된 결과 저장용 리스트
processed = []

for i, case in enumerate(test_results):
    # ✅ product_name 안전하게 추출
    product = None
    if case.get("additional_metadata") and isinstance(case["additional_metadata"], dict):
        product = case["additional_metadata"].get("product", "Unknown")

    result = {
        "index": i,
        "question": case["input"],
        "answer": case["actual_output"],
        "context": case["context"][0] if case.get("context") else "",
        "product_name": product,
        "passed": case["success"],
        "failed_metrics": [],
    }

    for metric in case["metrics_data"]:
        metric_name = metric["name"]
        result[metric_name + "_score"] = metric["score"]
        result[metric_name + "_success"] = metric["success"]
        if not metric["success"]:
            result["failed_metrics"].append(metric_name)

    processed.append(result)

# DataFrame으로 변환
eval_df = pd.DataFrame(processed)

# 저장
eval_df.to_csv("qa_eval_result_processed.csv", index=False)
print("✅ 평가 결과 전처리 및 저장 완료: qa_eval_result_processed.csv")
