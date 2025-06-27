import os
import json
import fitz  # PyMuPDF
import re
import unicodedata
from pathlib import Path

# ========== 사용자 설정 ==========
pdf_dir = Path("downloaded_manuals")     # PDF 원본 경로
json_dir = Path("parsed_json")           # Upstage 파싱 JSON 경로
output_path = Path("processed_data_full.jsonl")
# =================================


def extract_product_name_from_pdf(pdf_path: Path) -> str:
    """PDF 메타데이터에서 title(product name) 추출, 실패 시 파일명 기반"""
    try:
        doc = fitz.open(pdf_path)
        title = doc.metadata.get("title", "").strip()
        doc.close()

        if not title:
            # 메타데이터가 비어있을 경우, 파일명에서 추출
            title = pdf_path.stem.replace("_", " ").replace("-", " ").strip()

        return title

    except Exception as e:
        print(f"❌ {pdf_path.name} 메타데이터 추출 실패: {e}")
        # 예외 발생 시에도 파일명에서 추출
        return pdf_path.stem.replace("_", " ").replace("-", " ").strip()


import re

import re

def preprocess_markdown(markdown_text: str) -> list[str]:
    import re

    # 마크다운 제거
    text = re.sub(r'#+\s*', '', markdown_text)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'__(.*?)__', r'\1', text)
    text = re.sub(r'_(.*?)_', r'\1', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'`{1,3}[^`]+`{1,3}', '', text)
    text = re.sub(r'>\s?', '', text)
    text = re.sub(r'\n[-*]{3,}\n', '\n', text)
    text = re.sub(r'^\d+\.\s+', '', text, flags=re.M)

    # 특수기호 및 잡음 정리
    text = re.sub(r'[■●◆·\"\'\-–—•▶→∙·•☏⌀©ⓒ™®]', '', text)
    text = re.sub(r'\.{3,}', '.', text)
    text = re.sub(r'\n{2,}', '\n', text)
    text = text.strip()

    # Unicode 정규화
    text = unicodedata.normalize("NFKD", text)

    # 라인 분리 및 공백 제거
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    clean_lines = []
    for line in lines:
        # 전형적인 목차 포맷 제거 (점, 중괄호, 숫자 포함)
        if re.match(r'^.*[\.・·•]{2,}[\s\.]*\d{1,3}$', line):
            continue

        # Copyright 및 boilerplate 제거
        if re.search(r'Copyright|All rights reserved', line, re.IGNORECASE):
            continue

        # 표 형식 제거
        if line.startswith('|') or line.count('|') >= 2:
            continue

        # 기술 명칭, 회로도 약어 제거 (CN1, FFC, DGND, SPI 등)
        if re.search(r'\b(CN\d+|FFC|PWM|DGND|CLK|EEPROM|SENSOR|SPI|ROM|NAND|3\.3V|24VS|TXD|RXD|LSU|SMPS|TONER|CRUM|TR\.?\s?belt)\b', line):
            continue

        # 깨진 문자 제거
        if re.search(r'[�]', line):
            continue

        # 비정상 한자/일문 제거
        if re.search(r'[\u3000-\u30ff\u4e00-\u9fff]', line):
            continue

        # 숫자, 알파벳, 특수기호만 과도하게 섞인 줄 제거
        if re.match(r'^[A-Z0-9\s\-\(\)\/\.:]+$', line) and len(line.split()) <= 6:
            continue

        # 너무 짧거나 불완전한 문장 제거
        if len(line) < 10 or len(line.split()) < 4:
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
