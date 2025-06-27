import os
import json
import re
from dotenv import load_dotenv
from tqdm import tqdm
from langchain_openai import ChatOpenAI

# 환경 변수 로딩 (.env 파일에 OPENAI_API_KEY 설정 필요)
load_dotenv()

# LLM 초기화
llm = ChatOpenAI(
    temperature=0.3,
    model="gpt-4o-mini"  # 필요 시 gpt-4로 변경 가능
)

# 프롬프트 생성 함수
def build_prompt(document_title: str, content: str) -> str:
    return (
        f"너는 스마트한 문서 독해 챗봇이다.\n\n"
        f"아래는 '{document_title}'이라는 제품 매뉴얼의 일부이다.\n"
        f"이 문서를 참고하여, 사용자가 실제로 질문할 만한 질문과 이에 대한 적절한 답변을 하나만 생성하라.\n\n"
        f"중요 조건:\n"
        f"- 생성된 Q&A는 반드시 주어진 정보만을 기반으로 해야 한다.\n"
        f"- 질문과 답변은 반드시 한국어로 작성해야 한다.\n"
        f"- 다음 JSON 형식으로 결과를 반환해야 한다.\n"
        f"- 주어진 문서 내용이 너무 부족하거나 질문할 만한 것이 없다면, 빈 리스트([])만 반환하라.\n\n"
        f"질문 카테고리:\n"
        f"1. '문제 해결' - 제품 사용 중 생기는 고장, 오류, 불편을 해결하는 질문\n"
        f"2. '제품 사용법 이해' - 기능, 설정, 절차, 조작법 등을 묻는 질문\n"
        f"3. '정보 탐색 및 선택' - 제품 스펙, 구성품, 비교, 구매 관련 정보 탐색 질문\n\n"
        f"JSON 형식 예시:\n"
        f"[{{\n"
        f"  \"question\": str,\n"
        f"  \"answer\": str,\n"
        f"  \"category\": str,\n"
        f"  \"product\": \"{document_title}\"\n"
        f"}}]\n\n"
        f"문서 내용:\n"
        f"{content}"
    )

# LLM 호출 및 결과 파싱
def generate_qa_pair(text: str, document_title: str) -> dict | None:
    prompt = build_prompt(document_title=document_title, content=text)
    try:
        response = llm.invoke(prompt)
        output = response.content.strip()

        if not output or output == "[]":
            return None

        # 코드 블록 제거 (```json 포함 가능성)
        cleaned = re.sub(r"```json|```", "", output).strip()

        parsed = json.loads(cleaned)
        if isinstance(parsed, list) and len(parsed) > 0:
            return parsed[0]
        else:
            return None

    except Exception as e:
        print("🔥 LLM 오류 발생:", e)
        return None

# 메인 실행
if __name__ == "__main__":
    input_path = "chunked_data.jsonl"
    output_path = "qa_dataset.jsonl"
    document_title = "삼성"  # 실제 제품 이름 입력

    with open(input_path, "r", encoding="utf-8") as infile, open(output_path, "w", encoding="utf-8") as outfile:
        for idx, line in enumerate(tqdm(infile, desc="Generating QA pairs", unit="chunk")):
            data = json.loads(line)
            chunk = data.get("chunk", "").strip()
            document_title = data.get("title", "미확인 제품")
            
            if len(chunk) < 100:
                continue

            qa = generate_qa_pair(chunk, document_title)
            if qa:
                json.dump(qa, outfile, ensure_ascii=False)
                outfile.write("\n")
