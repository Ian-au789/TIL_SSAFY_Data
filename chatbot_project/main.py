# # main.py
# from crawler.search_manuals import search_manual_pdfs
# from crawler.downloader import download_pdfs
# import os

# if __name__ == "__main__":
#     query = input("🔍 검색어를 입력하세요 (예: Samsung Printer): ")

#     # PDF 저장 디렉토리 준비
#     save_dir = os.path.join("data", "manuals")
#     os.makedirs(save_dir, exist_ok=True)

#     # 1. 검색어 기반 PDF 링크 수집
#     pdf_links = search_manual_pdfs(query)

#     if not pdf_links:
#         print("PDF 링크를 찾을 수 없습니다. 다른 검색어를 시도해보세요.")
#     else:
#         # 2. 다운로드 수행
#         download_pdfs(pdf_links, save_dir)
#         print("\n매뉴얼 수집 완료")

from crawler.search_manuals import search_manuals

if __name__ == "__main__":
    keyword = "Samsung Printer"
    pdfs = search_manuals(keyword)

    print(f"\n총 {len(pdfs)}개의 PDF 링크 수집 완료:")
    for link in pdfs:
        print(link)