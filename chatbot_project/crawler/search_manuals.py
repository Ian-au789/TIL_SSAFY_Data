from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def search_manuals(keyword: str, max_results: int = 10) -> list:
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # UI 없이 실행
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 ...")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        search_url = f"https://manuals.plus/?s={keyword.replace(' ', '+')}"
        driver.get(search_url)
        time.sleep(3)

        with open("search_result.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

        result_links = driver.find_elements(By.CSS_SELECTOR, "h2.entry-title a")
        manual_links = []

        for link in result_links[:max_results]:
            href = link.get_attribute("href")
            print(f"🔗 상세 페이지: {href}")
            driver.get(href)
            time.sleep(2)

            a_tags = driver.find_elements(By.TAG_NAME, "a")
            for a in a_tags:
                pdf = a.get_attribute("href")
                if pdf and pdf.endswith(".pdf"):
                    manual_links.append(pdf)
                    print(f"✅ PDF 링크 발견: {pdf}")
                    break

        return manual_links

    finally:
        driver.quit()


'''
requests 라이브러리를 이용한 방법 
하지만 웹사이트가 비브라우저 클라이언트 요청을 차단하고 있어서 403 Forbidden Error 발생
header에 User agent를 추가해서 우회 시도했으나 그것조차 차단됨
'''

# import requests
# from bs4 import BeautifulSoup

# def search_manual_links(keyword: str, max_results: int = 10) -> list:
#     """
#     manuals.plus의 검색 API를 이용해 keyword에 해당하는 매뉴얼 상세 페이지를 찾고,
#     각 페이지에서 PDF 링크를 추출해 반환한다.
#     """
#     api_url = "https://manuals.plus/wp-json/wp/v2/search"
#     params = {
#         "search": keyword,
#         "_embed": "true"
#     }

#     try:
#         headers = {
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
#         }

#         res = requests.get(api_url, params=params, headers=headers, timeout=10)
#         res.raise_for_status()
#         search_results = res.json()
#     except Exception as e:
#         print(f"검색 요청 실패: {e}")
#         return []

#     pdf_links = []

#     for item in search_results[:max_results]:
#         page_url = item.get("url")
#         print(f"🔎 매뉴얼 페이지: {page_url}")

#         try:
#             page_res = requests.get(page_url, timeout=10)
#             page_res.raise_for_status()
#             soup = BeautifulSoup(page_res.text, "html.parser")

#             for a in soup.find_all("a", href=True):
#                 href = a["href"]
#                 if href.lower().endswith(".pdf"):
#                     pdf_links.append(href)
#                     print(f"PDF 링크 발견: {href}")
#                     break  # 페이지당 하나만 수집

#         except Exception as e:
#             print(f"페이지 크롤링 실패: {page_url} → {e}")

#     return pdf_links