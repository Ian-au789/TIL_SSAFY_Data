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