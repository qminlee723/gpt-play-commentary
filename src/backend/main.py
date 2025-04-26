import os
from datetime import datetime, timedelta
from kopis_json_for_gpt import collect_unique_ids, build_performance_dataset
from utils import log, load_existing_ids, save_existing_ids, save_json

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
EXISTING_IDS_PATH = os.path.join(DATA_DIR, "existing_ids.json")
LOG_FILE_PATH = os.path.join(DATA_DIR, "log.txt")


def main(start_date: str, end_date: str):
    
    # 로그 초기화
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(LOG_FILE_PATH, "w", encoding="utf-8") as f:
        f.write("[🚀 KOPIS 공연 수집 로그 시작]\n")
        f.write(f"시작일: {start_date}, 종료일: {end_date}\n")
        f.write("========================================\n")   

    log("🎬 공연 ID 수집 시작...")
    new_ids = collect_unique_ids(start_date, end_date)

    log("\n📁 기존 ID 로딩 중...")
    existing_ids = load_existing_ids(EXISTING_IDS_PATH)

    log(f"🔍 기존: {len(existing_ids)}개, 이번 수집: {len(new_ids)}개")
    diff_ids = new_ids - existing_ids
    log(f"✨ 새롭게 발견된 ID: {len(diff_ids)}개")

    if not diff_ids:
        log("✅ 새로운 공연 없음. 종료합니다.")
        return

    log("\n📋 공연 상세 정보 수집 중...")
    dataset = build_performance_dataset(list(diff_ids))

    today = datetime.now().strftime("%Y%m%d")
    output_file = os.path.join(DATA_DIR, f"kopis_performances_{today}.json")
    save_json(dataset, output_file)

    updated_ids = existing_ids.union(new_ids)
    save_existing_ids(updated_ids, EXISTING_IDS_PATH)

    log(f"\n✅ 저장 완료! 총 {len(dataset)}개 공연 정보 → {output_file}")
