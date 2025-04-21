import sys
import os
import time
from flask import Flask, jsonify, Response, stream_with_context
from flask_cors import CORS
import main
from utils import LOG_FILE_PATH  # ✨ 이제 utils에서 경로 가져옴

# 현재 디렉토리 backend/를 모듈 경로에 추가
sys.path.append(os.path.dirname(__file__))

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/run")
def run_kopis():
    try:
        main.main()
        return jsonify({"status": "ok", "message": "공연 데이터 수집 완료!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/log")
def get_log():
    with open(LOG_FILE_PATH, "r", encoding="utf-8") as f:
        return f.read(), 200, {"Content-Type": "text/plain"}


if __name__ == "__main__":
    app.run(debug=True, port=5050)
