import os
import time
from urllib.parse import urlparse
import requests
from requests.exceptions import RequestException, ReadTimeout, ChunkedEncodingError

pdf_links = [
    "https://laserpros.com/img/manuals/samsung-manuals/samsung-xpress-sl-m283x-series-service-manual.pdf",
    "https://www.laserpros.com/img/manuals/samsung-manuals/samsung-xpress-c1810-series-sl-c1810w-service-manual.pdf",
    "https://arbikas.com/pub/media/files/ML-1650-%3A-ML1640-userguide.pdf",
    "https://h10032.www1.hp.com/ctg/Manual/c05790048.pdf",
    "https://h10032.www1.hp.com/ctg/Manual/c05787199.pdf",
    "https://h10032.www1.hp.com/ctg/Manual/c05787831.pdf",
    "https://h10032.www1.hp.com/ctg/Manual/c05790356.pdf",
    "https://h10032.www1.hp.com/ctg/Manual/c05753215.pdf",
    "https://images10.newegg.com/User-Manual/User_Manual_28-112-076.pdf",
    "https://amarketplaceofideas.com/wp-content/uploads/2017/04/Samsung_ML-20101.pdf"
]

save_dir = "downloaded_manuals"
os.makedirs(save_dir, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": "https://www.google.com"
}

def download_pdf(url, filepath, max_retries=3):
    for attempt in range(1, max_retries + 1):
        try:
            with requests.get(url, headers=headers, stream=True, timeout=120) as resp:
                resp.raise_for_status()
                with open(filepath, 'wb') as f:
                    for chunk in resp.iter_content(chunk_size=1024 * 1024):  # 1MB씩 받기
                        if chunk:
                            f.write(chunk)
            return True
        except (ReadTimeout, ChunkedEncodingError, RequestException) as e:
            print(f"⚠️ 재시도 {attempt}/{max_retries} 실패: {e}")
            time.sleep(2 * attempt)
    return False

for idx, url in enumerate(pdf_links, 1):
    filename = os.path.basename(urlparse(url).path)
    filepath = os.path.join(save_dir, filename)
    print(f"{idx}. 다운로드 중: {filename}")
    success = download_pdf(url, filepath)
    if success:
        print(f"✅ 완료: {filepath}")
    else:
        print(f"❌ 실패: {url}")
