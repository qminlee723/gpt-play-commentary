import os
import sys
from datetime import datetime
from glob import glob
from flask import Flask, jsonify, Response, send_from_directory
from flask_cors import CORS
import main
from utils import LOG_FILE_PATH # 로그 파일 경로
from pathlib import Path
from gpt_api import process_and_save_batch, process_and_save

# 현재 디렉토리 backend/를 모듈 경로에 추가
sys.path.append(os.path.dirname(__file__))

# 정적 파일 위치 지정
app = Flask(
    __name__,
    static_folder="../frontend",  # frontend 경로 조정
    static_url_path=""
)
CORS(app, resources={r"/*": {"origins": "*"}})

# 기본 라우트: index.html 반환
@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

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

@app.route("/list-downloads")
def list_downloads():
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    files = os.listdir(data_dir)

    # kopis_ 로 시작하고 .json / .csv 로 끝나는 파일 필터링
    downloadable_files = [
        f for f in files
        if f.endswith(".csv") or f.startswith("kopis_") and (f.endswith(".json"))
    ]

    # 파일명을 기준으로 내림차순 정렬 (최신 먼저)
    downloadable_files.sort(reverse=True)

    return jsonify(downloadable_files)

@app.route("/download/<filename>")
def download_file(filename):
    base_dir = os.path.dirname(__file__)  # src/backend
    data_dir = os.path.join(base_dir, "data")
    
    # 디버그용 로그
    file_path = os.path.join(data_dir, filename)
    print(f"[DEBUG] 다운로드 요청된 파일 경로: {file_path}")
    
    return send_from_directory(data_dir, filename, as_attachment=True)

@app.route("/summarize")
def run_gpt_summary():
    
    # 1. 최신 JSON 파일 찾기
    json_files = glob("data/kopis_*.json")
    if not json_files:
        return jsonify({"error": "No kopis JSON files found"}), 404

    latest_json = max(json_files, key=os.path.getmtime)

    # 2. 오늘 날짜로 CSV 이름 생성
    today = datetime.now().strftime("%Y%m%d")
    output_csv = f"data/gpt_summary_{today}.csv"

    # 3. 요약 처리
    try:
        process_and_save(json_path=latest_json, output_csv=output_csv)
        return jsonify({
            "message": "GPT 요약 완료!",
            "json_used": latest_json,
            "csv_saved": output_csv
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    # 대용량은 일단 주석
    # process_and_save_batch(
    #     json_path=latest_json,
    #     output_csv=output_csv,
    # )
    return jsonify({"message": "GPT 요약 완료!"})


if __name__ == "__main__":
    app.run(debug=True, port=5050)
