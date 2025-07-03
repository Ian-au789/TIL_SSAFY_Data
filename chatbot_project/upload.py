from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# JSONL 파일 열기 및 업로드
with open("qa_dataset_cleaned.json", "rb") as f:
    file = client.files.create(file=f, purpose="assistants")

print("📁 Uploaded file ID:", file.id)
