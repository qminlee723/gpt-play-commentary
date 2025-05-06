# gpt-play-commentary

> A vibe-coded AI commentary engine — built with vibes, powered by ChatGPT 4o

- GPT API를 통해 공연 데이터 요약 작업을 한 번에 처리할 수 있는 자동화 프로그램입니다. 
- 모델은 GPT-4.1을, 요약 대상인 기본 공연 정보는 KOPIS API를 사용했습니다.


<br>


## 🎬 Demo

#### 공연 ID 수집

- 시작날짜 및 종료 날짜 설정해 해당 날짜에 조회되는 공연 ID 수집

https://github.com/user-attachments/assets/06c80e37-f052-41fa-8971-a77b7ac03158


<br>

#### 수집 정보 저장

- 개별 공연의 상세 데이터를 수집하여 `.json` 파일로 저장합니다.
- 해당 json파일은 아래 파일 목록에서 다운로드 가능

https://github.com/user-attachments/assets/17173b41-9d0b-4bcd-bb4d-49a13cb54907



<br>


#### 중복 데이터 외 새로운 데이터만 수집

- 기존 데이터와 비교해 새로운 공연 내용만 수집합니다

https://github.com/user-attachments/assets/30bb6336-f706-45ca-b63e-7f6cdb97925a



<br>

#### GPT 요약

- GPT 요약은 처리 효율과 에러 방지를 위해 데이터를 10개 단위로 분할해 순차 요청


https://github.com/user-attachments/assets/ae3df3b0-1f1b-4b9e-b1ac-4d163ebb05b9




<br>

#### 에러 핸들링: GPT 요약 처리 중간에 멈추는 경우

- 요약 요청 보내는 중간에 에러로 멈추게 되는 경우에도 이미 요약 요청 되어 있는 요약 정보 확인해 그 이후부터 요청 보내도록 처리
- 요청 결과는 즉시 저장되어 유실되는 데이터 없도록 처리

https://github.com/user-attachments/assets/3f8b066f-bf40-4496-aace-f45e6d71dce1


<br>

#### UI

- 수집 진행 상황과 로그를 페이지에서도 확인 가능하도록 로그 정보 업데이트
  - 작업 수행시 매 1초마다 로그 갱신하도록 함
  - 새로운 작업 수행시 log 덮어쓰기
- 버튼 중복 클릭 방지를 위해 프론트엔드에서 재클릭 비활성화 처리
- 시작 날짜는 요청 보내는 날짜의 하루 전날로 디폴트 세팅
- 업데이트 된 파일 목록 페이지에서 클릭시 다운로드 받을 수 있도록 세팅


<br>

#### 출력 파일

- `kopis_performances_YYYYMMDD.json`: 공연 상세 정보
- `gpt_summary_YYYYMMDD.csv`: GPT 요약 결과



<br>
<br>


## 🤖 OpenAI API 

#### 사용 모델

- GPT-4.1



#### PRICING

- 4177개 공연 요약 → $5.25 



#### PROMPT

```
다음 공연 정보를 바탕으로 감성적인 요약을 작성해 주세요.

조건:
- 총 5줄 이하로, 각 문장은 '∙'로 시작하고 줄바꿈으로 구분
- '~요' 말투의 부드러운 구어체 사용
- 제목은 포함하지 마세요
- 출연진·곡명 등은 최대 3개까지만 언급하고 ‘등’으로 생략
- 주제, 특징, 감성 포인트 위주로 요약 (줄거리 상상 금지)

예시:
∙ 따뜻한 이야기와 감동을 전하는 공연이에요.  
∙ 익숙한 음악이 새롭게 해석되어 특별한 감정을 줘요.  
∙ 혼자 또는 가족과 함께 즐기기 좋아요.  

공연 정보:
- 기간: {prfpdfrom} ~ {prfpdto}
- 장르: {genrenm}
- 출연: {prfcast}
- 관람 등급: {prfage}
- 시놉시스: {sty if sty.strip() else '[시놉시스 없음]'}
```



<br>
<br>


## ⚒️ Tech Stack

- Python
- Flask
- Pandas
- HTML, CSS, JavaScript
- OpenAI GPT API - [GPT4.1](https://platform.openai.com/docs/models/gpt-4.1)
- [KOPIS API](https://www.kopis.or.kr/por/cs/openapi/openApiInfo.do?menuId=MNU_00074)



<br>
<br>


## 🚀 Getting Started

1. 가상환경 세팅

```bash
python -m venv venv
```

2. 가상환경 activate

```bash
# macOS/Linux
source venv/bin/activate
```

```bash
# Windows
.\venv\Scripts\activate
```

3. 필요한 패키지 설치

```bash
pip install -r requirements.txt
```

4. 환경변수 설정(`.env`)

```ini
# src/.env
KOPIS_API_KEY="your_kopis_api_key"
OPENAI_API_KEY="your_openai_api_key"
```

5. 서버 실행

```bash
python flask_server.py
```

6. 프론트엔드 주소(⚠️로컬에서만 가능)

```
http://127.0.0.1:5050/
```



