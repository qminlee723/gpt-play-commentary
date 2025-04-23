# gpt-play-commentary

A vibe-coded AI commentary engine — built with vibes, powered by GPT 4o



## Getting Started

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



