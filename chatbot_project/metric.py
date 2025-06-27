import os
import json
import pandas as pd
from dotenv import load_dotenv
from deepeval.test_case import LLMTestCase
from deepeval.dataset import EvaluationDataset
from deepeval.metrics import HallucinationMetric, AnswerRelevancyMetric, ToxicityMetric
from deepeval import evaluate

# 1. 평가 결과를 dict로 변환하는 함수
def convert_eval_to_dict(test_cases, metrics: list):
    results = []

    for i, test_case in enumerate(test_cases):
        result = {
            "index": i,
            "question": test_case.input,
            "answer": test_case.actual_output,
            "context": test_case.context[0] if test_case.context else "",
            "failed_metrics": [],
        }

        passed = True
        for metric in metrics:
            metric_name = metric.__class__.__name__

            metric_result = test_case.metric_outputs.get(metric_name, {})
            score = metric_result.get("score")
            success = metric_result.get("success", True)

            result[metric_name + "_score"] = score
            result[metric_name + "_pass"] = success

            if not success:
                passed = False
                result["failed_metrics"].append(metric_name)

        result["passed"] = passed
        results.append(result)

    return results


# 2. 환경 변수 로딩 및 OpenAI API Key 설정
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# 3. QA 데이터셋 로딩 (200개 샘플)
qa_df = pd.read_json("qa_dataset_cleaned.jsonl", lines=True)
qa_df = qa_df.sample(200, random_state=42)

# 4. EvaluationDataset 구성
dataset = EvaluationDataset()
for q, a in zip(qa_df["question"], qa_df["answer"]):
    dataset.add_test_case(
        LLMTestCase(
            input=q,
            actual_output=a,
            context=[a]  # context가 없을 경우 answer 기반
        )
    )

# 5. 평가 메트릭 정의
hal_metric = HallucinationMetric(threshold=0.3, model="gpt-4o-mini")
relevan_metric = AnswerRelevancyMetric(threshold=0.5, model="gpt-4o-mini")
toxicity_metric = ToxicityMetric(threshold=0.5, model="gpt-4o-mini")

# 1. 평가 실행
evaluation_result = evaluate(dataset, [hal_metric, relevan_metric, toxicity_metric])

# 2. 평가 결과를 JSON 형식으로 저장
def save_eval_result_to_json(path, result):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(result.model_dump(), f, ensure_ascii=False, indent=2)

# 3. 경로 설정
save_path = "qa_eval_result.json"
temp_path = "qa_eval_result_temp.json"

# 4. 저장 및 복사
save_eval_result_to_json(save_path, evaluation_result)
os.system(f"cp {save_path} {temp_path}")

print(f"✅ 평가 결과가 {save_path}에 저장되었고, {temp_path}로 복사되었습니다.")