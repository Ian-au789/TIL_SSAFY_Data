import json
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 경로 설정
input_path = Path("processed_data_full.jsonl")
output_path = Path("chunked_data.jsonl")

# 청크 분할기 설정
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ".", " ", ""]
)

def chunk_manuals():
    with open(input_path, "r", encoding="utf-8") as infile, open(output_path, "w", encoding="utf-8") as outfile:
        for line in infile:
            item = json.loads(line)
            title = item.get("title", "")
            content_list = item.get("content", [])
            full_text = "\n".join(content_list).strip()

            if not full_text:
                continue

            # RecursiveCharacterTextSplitter로 청크 분할
            chunks = text_splitter.split_text(full_text)

            for chunk in chunks:
                chunk_item = {
                    "title": title,
                    "chunk": chunk
                }
                json.dump(chunk_item, outfile, ensure_ascii=False)
                outfile.write("\n")

    print(f"✅ 청크 분할 완료 → {output_path}")

if __name__ == "__main__":
    chunk_manuals()
