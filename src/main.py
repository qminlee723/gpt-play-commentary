import json
from kopis_json_for_gpt import collect_unique_ids, build_performance_dataset
from utils import load_existing_ids, save_existing_ids
from datetiem import datetime, timedelta

def main():
    yesterday = datetime.today() - timedelta(days=1)
    date_str = yesterday.strftime("%Y%m%d")  # 예: '20250420'

    start_date = date_str
    end_date = date_str

    print("🎬 공연 ID 수집 시작...")
    new_ids = collect_unique_ids(start_date, end_date)

    print("\n📁 기존 ID 로딩 중...")
    existing_ids = load_existing_ids()

    print(f"🔍 기존: {len(existing_ids)}개, 이번 수집: {len(new_ids)}개")
    diff_ids = new_ids - existing_ids
    print(f"✨ 새롭게 발견된 ID: {len(diff_ids)}개")

    if not diff_ids:
        print("✅ 새로운 공연 없음. 종료합니다.")
        return

    print("\n📋 공연 상세 정보 수집 중...")
    dataset = build_performance_dataset(list(diff_ids))

    output_file = "kopis_performances_new.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

    # 기존 ID 업데이트
    updated_ids = existing_ids.union(new_ids)
    save_existing_ids(updated_ids)

    print(f"\n✅ 저장 완료! 총 {len(dataset)}개 공연 정보 → {output_file}")


if __name__ == "__main__":
    main()
