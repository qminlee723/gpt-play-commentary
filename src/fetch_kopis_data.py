import os
import requests
from dotenv import load_dotenv

# .env 불러오기
load_dotenv()
API_KEY = os.getenv("KOPIS_API_KEY")

def fetch_performance_list(start_date: str, end_date: str, category_code: str = None, area_code: int = None):
    url = "http://kopis.or.kr/openApi/restful/boxoffice"
    params = {
        "service": API_KEY,
        "stdate": start_date,
        "eddate": end_date,
    }

    if category_code:
        params["catecode"] = category_code
    if area_code:
        params["area"] = area_code

    response = requests.get(url, params=params, timeout=10)
    if response.status_code != 200:
        raise Exception(f"API 요청 실패! 상태코드: {response.status_code}")

    return response.text


def fetch_performance_detail(mt20id: str) -> str:
    url = f"http://kopis.or.kr/openApi/restful/pblprfr/{mt20id}"
    params = {
        "service": API_KEY
    }

    response = requests.get(url, params=params, timeout=10)
    if response.status_code != 200:
        raise Exception(f"공연 상세 API 실패! mt20id: {mt20id}, 상태코드: {response.status_code}")

    return response.text
