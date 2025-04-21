from fetch_kopis_data import fetch_performance_list, fetch_performance_detail
from parse_kopis_data import parse_performance_ids, parse_performance_detail
from time import sleep
from utils import log

GENRE_CODES = {
    "연극": "AAAA",
    "뮤지컬": "GGGA",
    "서양음악(클래식)": "CCCA",
    "한국음악(국악)": "CCCC",
    "대중음악": "CCCD",
    "무용(서양/한국무용)": "BBBC",
    "대중무용": "BBBR",
    "서커스/마술": "EEEB",
    "복합": "EEEA",
    "아동": "KID",
    "오픈런": "OPEN"
}

def collect_unique_ids(start_date: str, end_date: str) -> set:
    all_ids = set()


    for genre_name, code in GENRE_CODES.items():
        print(f"[{genre_name}] 공연 ID 수집 중...")
        try:
            xml_data = fetch_performance_list(start_date, end_date, code)
            ids = parse_performance_ids(xml_data)


            log(f"[{genre_name}] → {len(ids)}개 수집됨")
            all_ids.update(ids)
        except Exception as e:
            log(f"  ❌ 오류 발생: {e}")
        sleep(0.3)

    log(f"\n총 중복 제거된 공연 ID 개수: {len(all_ids)}")
    return all_ids

def build_performance_dataset(mt20id_list: list[str]) -> list[dict]:
    result = []

    for idx, mt20id in enumerate(mt20id_list, start=1):
        try:
            print(f"[{idx}/{len(mt20id_list)}] 공연 ID: {mt20id} 상세 조회 중...")
            xml_data = fetch_performance_detail(mt20id)
            detail = parse_performance_detail(xml_data)
            if detail:
                result.append(detail)
        except Exception as e:
            log(f"  ❌ 오류: {e}")
        sleep(0.3)

    return result
