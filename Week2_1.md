# Task-oriented QA chatbot system

### Pipeline

- Input : 사용자의 자연어 질문
- NLU (Natural Input Processing) :  사용자의 의도 파악
- Dialog State Management : 대화 상태 관리 (사용자의 요청 및 대화 흐름을 추적하여 다음 대화 단계 설정)
- Knowledbe Base Interaction : DB, API 같은 외부 서비스와 통신
- NLG (Natural Language Generation) : 응답 생성 및 출력

### 데이터 중요성
- Domain-Specific Knowledge : 특정 분야 특정 챗봇
- 이미 배포 한 서비스의 부족한 능력을 데이터로 개선 가능
- 상대적으로 저렴한 수정 방법

### 데이터 수집 전략
1. 목표 정의 : 수집하려는 데이터가 문제와 어떤 관계가 있는지 정의
2. 데이터 요구사항 정의 : 데이터 유형, 형식, 그리고 범위 설정
3. 데이터 수집 방법 선정 및 QA 데이터 구축 : 웹 크롤링, API, 데이터 증강 등 방법을 사용해 JSON, CSV 등 형식으로 변환
4. 수집 데이터 품질 검토 및 수정 : 중복 제거, 오류 수정, 데이터 검증 등 (다국어 데이터 번역 품질 확인 등)
5. 수집 데이터 품질 관리 및 모니터링 : Grafana 같은 데이터 모니터링 도구를 통해 수집 데이터 품질 관리 (중복률 추적, 누락 데이터 비율, 데이터 유효성 검증)

## 웹 크롤링

1. 정의 : 웹사이트에서 데이터를 자동으로 수집하는 기술

2. 시작 url 설정 -> HTML 다운로드 -> 데이터 추출 -> 링크 탐색 -> 반복 -> 종료 조건

### 기초 라이브러리

1. Requests

- HTTP request 및 response 처리
- 간단한 GET, POST 등 요청을 통해 웹 페이지 데이터(HTML, XML 등) 가져오는 데 사용
- 데이터 다운로드 및 API 호출에 적합
예시) 

    import requests

    response = requests.get('https://edussafy.com')
    print(response.text)

2. BeautifulSoup

- HTML 및 XML 데이터 파싱
- HTML 문서를 구조화하여 원하는 데이터만 추출
- HTML 요소를 트리 구조(DOM)로 변환하여 데이터 검색이 쉬움
- 동적 웹사이트 처리 불가
예시)

    from bs4 import BeautifulSoup
    import requests

    response = requests.get('https://edussafy.com')
    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup.title.string)

3. Scrapy

- 대규모 웹 크롤링 프레임워크
- 대량의 데이터를 효율적으로 크롤링하고 구조화된 데이터로 저장
- 비동기 처리 기반으로 매우 빠름
- 다양한 출력 형식 지원, 단순 작업에는 과도함
예시)

    import scrapy

    class ExampleSpider(scrapy.Spider):
        name = 'ssafy'
        start_urls = ['https://edussafy.com']

        def parse(self, response):
            for title in response.css('title::text'):
                yield{'title': title.get()}

4. Selenium

- 동적 웹사이트 크롤링
- 브라우저를 자동으로 제어하여 동적 컨텐츠 처리 (Captcha, 로그인 등)
- 웹 테스트 자동화 도구로도 사용
- 속도가 느리고 리소스 사용량이 많음
예시)

    from selenium import webcriver

    driver = webdriver.Chrome()
    driver.get('https://edussafy.com')
    print(driver.title)
    driver.quit


