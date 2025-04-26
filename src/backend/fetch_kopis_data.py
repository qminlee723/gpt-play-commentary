import os
import requests
from dotenv import load_dotenv
from parse_kopis_data import parse_performance_ids

# .env 불러오기
load_dotenv()
API_KEY = os.getenv("KOPIS_API_KEY")

def fetch_performance_list(start_date: str, end_date: str) -> list[str]:
    url = "http://kopis.or.kr/openApi/restful/pblprfr"
    all_ids = set()
    cpage = 1
    rows = 100
    
    while True:
        params = {
            "service": API_KEY,
            "stdate": start_date,
            "eddate": end_date,
            "cpage": cpage,
            "rows": rows,
        }

        response = requests.get(url, params=params, timeout=10)

        if response.status_code != 200:
            raise Exception(f"API 요청 실패! 상태코드: {response.status_code}")
        
        xml_data = response.text
        ids = parse_performance_ids(xml_data)

        if not ids:
            break
        
        all_ids.update(ids)
        cpage += 1 

    return all_ids


def fetch_performance_detail(mt20id: str) -> str:
    url = f"http://kopis.or.kr/openApi/restful/pblprfr/{mt20id}"
    params = {
        "service": API_KEY
    }

    response = requests.get(url, params=params, timeout=10)
    if response.status_code != 200:
        raise Exception(f"공연 상세 API 실패! mt20id: {mt20id}, 상태코드: {response.status_code}")

    return response.text
