import json
import requests
from pathlib import Path
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()
API_KEY = os.getenv("UPSTAGE_API_KEY")  # 반드시 .env에 UPSTAGE_API_KEY 변수 설정되어 있어야 함

if not API_KEY:
    raise ValueError("❌ .env 파일에 'UPSTAGE_API_KEY'가 정의되어 있지 않습니다.")

# 디렉토리 설정
PDF_DIR = "downloaded_manuals"
OUTPUT_DIR = "parsed_json"
pdf_path = Path(PDF_DIR)
save_path = Path(OUTPUT_DIR)
save_path.mkdir(parents=True, exist_ok=True)

# API 설정
API_URL = "https://api.upstage.ai/v1/document-ai/document-parse"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}
POST_DATA = {
    "output_formats": "['html', 'text', 'markdown']",
    "base64_encoding": "['table']",
    "ocr": "force",
    "coordinates": "true",
}

# PDF 파일 반복 처리
for idx, manual_pdf in enumerate(pdf_path.glob("*.pdf"), 1):
    print(f"{idx}. 업로드 중: {manual_pdf.name}")
    files = {"document": open(manual_pdf, "rb")}

    try:
        response = requests.post(
            API_URL,
            headers=HEADERS,
            files=files,
            data=POST_DATA,
            timeout=120
        )

        if response.status_code == 200:
            response_data = response.json()
            output_file = save_path / f"{manual_pdf.stem}.json"

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(response_data, f, ensure_ascii=False, indent=4)
            print(f"✅ 저장 완료: {output_file.name}")
        else:
            print(f"❌ 실패 [{response.status_code}]: {response.text}")

    except Exception as e:
        print(f"❌ 예외 발생: {manual_pdf.name} → {e}")
