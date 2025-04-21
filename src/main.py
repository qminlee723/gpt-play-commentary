import json
import os
from kopis_json_for_gpt import collect_unique_ids, build_performance_dataset
from utils import load_existing_ids, save_existing_ids
from datetime import datetime, timedelta

LOG_FILE_PATH = "frontend/log.txt"


def log(message: str):
    print(message)
    with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
        f.write(message + "\n")


def main():
    # 로그 초기화
    os.makedirs("frontend", exist_ok=True)
    with open(LOG_FILE_PATH, "w", encoding="utf-8") as f:
      f.write("[🚀 KOPIS 공연 수집 로그 시작]\n")

    yesterday = datetime.today() - timedelta(days=1)
    date_str = yesterday.strftime("%Y%m%d")  # 예: '20250420'

    start_date = date_str
    end_date = date_str

    log("🎬 공연 ID 수집 시작...")
    new_ids = collect_unique_ids(start_date, end_date)

    log("\n📁 기존 ID 로딩 중...")
    existing_ids = load_existing_ids()

    log(f"🔍 기존: {len(existing_ids)}개, 이번 수집: {len(new_ids)}개")
    diff_ids = new_ids - existing_ids
    log(f"✨ 새롭게 발견된 ID: {len(diff_ids)}개")

    if not diff_ids:
        log("✅ 새로운 공연 없음. 종료합니다.")
        return

    log("\n📋 공연 상세 정보 수집 중...")
    dataset = build_performance_dataset(list(diff_ids))

    output_file = "kopis_performances_new.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

    # 기존 ID 업데이트
    updated_ids = existing_ids.union(new_ids)
    save_existing_ids(updated_ids)

    log(f"\n✅ 저장 완료! 총 {len(dataset)}개 공연 정보 → {output_file}")



if __name__ == "__main__":
    main()
