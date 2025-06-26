import os
import json
import fitz  # PyMuPDF
import re
from pathlib import Path

# ========== 사용자 설정 ==========
pdf_dir = Path("downloaded_manuals")     # PDF 원본 경로
json_dir = Path("parsed_json")           # Upstage 파싱 JSON 경로
output_path = Path("processed_data_full.jsonl")
# =================================


def extract_product_name_from_pdf(pdf_path: Path) -> str:
    """PDF 메타데이터에서 title(product name) 추출"""
    try:
        doc = fitz.open(pdf_path)
        title = doc.metadata.get("title", "").strip()
        doc.close()
        return title
    except Exception as e:
        print(f"❌ {pdf_path.name} 메타데이터 추출 실패: {e}")
        return ""


def preprocess_markdown(markdown_text: str) -> list[str]:
    """Upstage 문서에서 추출된 마크다운 텍스트를 의미 있는 문장 단위로 정리"""
    
    # 마크다운 기본 제거
    text = re.sub(r'#+\s*', '', markdown_text)  # 제목
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # 굵은 글씨
    text = re.sub(r'\*(.*?)\*', r'\1', text)  # 이탤릭
    text = re.sub(r'__(.*?)__', r'\1', text)
    text = re.sub(r'_(.*?)_', r'\1', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)  # 링크 텍스트만
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)  # 이미지 제거
    text = re.sub(r'`{1,3}[^`]+`{1,3}', '', text)  # 코드블록 제거
    text = re.sub(r'>\s?', '', text)  # 인용 제거
    text = re.sub(r'\n[-*]{3,}\n', '\n', text)  # 수평선 제거
    text = re.sub(r'^\d+\.\s+', '', text, flags=re.M)  # 번호 있는 리스트

    # 특수기호 및 잡음 정리
    text = re.sub(r'[■●◆·\"\'\-–—•▶→∙·•]', '', text)
    text = re.sub(r'\.{3,}', '.', text)
    text = re.sub(r'\n{2,}', '\n', text)
    text = text.strip()

    # 문단 분할
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    clean_lines = []
    for line in lines:
        # 목차 스타일 제거 (예: 1.1 Something)
        if re.match(r'^\d+(\.\d+)*\s+[A-Za-z가-힣]+', line):
            continue
        # 의미 없는 잔해 제거: 5단어 이하 & 특수문자 비율 높거나 알파벳 없는 경우
        words = line.split()
        if len(words) < 5:
            continue
        if sum(1 for c in line if not c.isalnum() and not c.isspace()) / len(line) > 0.3:
            continue
        clean_lines.append(line)

    return clean_lines


def process_all_manuals():
    results = []

    for json_file in json_dir.glob("*.json"):
        try:
            pdf_name = json_file.stem + ".pdf"
            pdf_path = pdf_dir / pdf_name

            if not pdf_path.exists():
                print(f"⚠️ PDF 파일 없음: {pdf_path.name}, 스킵합니다.")
                continue

            # 1. product_name 추출
            product_name = extract_product_name_from_pdf(pdf_path)

            # 2. markdown 콘텐츠 불러오기
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                markdown = data.get("content", {}).get("markdown", "")

            if not markdown.strip():
                print(f"⚠️ {json_file.name}: markdown 콘텐츠 없음, 스킵합니다.")
                continue

            # 3. 전처리
            content_chunks = preprocess_markdown(markdown)

            # 4. flag 설정
            flag = any(product_name.lower() in chunk.lower() for chunk in content_chunks) if product_name else False

            # 5. 저장 포맷 구성
            result = {
                "title": product_name,
                "content": content_chunks,
                "flag": flag,
            }

            results.append(result)

        except Exception as e:
            print(f"❌ 처리 실패: {json_file.name}, 원인: {e}")

    # 6. jsonl 저장
    with open(output_path, "w", encoding="utf-8") as out_file:
        for item in results:
            json.dump(item, out_file, ensure_ascii=False)
            out_file.write("\n")

    print(f"\n✅ 전처리 완료: {len(results)}개의 매뉴얼이 저장되었습니다 → {output_path}")


if __name__ == "__main__":
    process_all_manuals()
