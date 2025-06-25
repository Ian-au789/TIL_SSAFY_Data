## Task oriented QA

1. Open-domain Dialogue : 자유로운 대화 또는 다양한 주제에 대해 응답, 사용자의 목표가 항상 바뀌며 여러 주제에 대해 열린 대화 형식으로 응답

2. Task-oriented : 특정 목표나 작업을 중심으로 설계된 서비스, 목표 달성을 위해 필요한 기능 제공 및 자동화

## Task Classification

1. Top-down : 큰 그림에서 시작해 세부적인 사례로 구체화

2. Bottom-up : 구체적인 사례를 먼저 파악하고 이를 조합하여 전체적인 구조 정의

## Custmoer Feedback

1. QA dataset : query & response

2. DPO dataset : query & response (복수) & preferred response

3. KTO dataset : query & response & feedback

## Synthetic Data
: 실제 데이터를 모방하여 인위적으로 생성된 데이터

1. Chunking : LLM에서 긴 문서나 텍스트를 처리할 때, 텍스트를 작은 단위로 나누는 과정 -> 메모리 제한 극복 & 성능 최적화

- 길이 기반 or 패턴 기반 

2. Prompt Chaining : Question을 먼저 생성하고 그에 맞는 Answer을 찾아 QA dataset 완성

3. Few Shot Prompt QA : 적은 수의 예시를 제공하여 특정 작업 수행하도록 유도 

4. RAG (Retrival-Augmented Generation) : LLM이 스스로 필요 정보를 검색 후 질문에 대한 답변을 생성 (중요!!)

- 스스로 지속적으로 변하는 정보를 업데이트

- 학습 공백을 스스로 메꿔 설계 당시 스펙 극복 

## Dataset quality check

- 적합도
- 정확도
- 일관성
- 유창성
- 다양성
