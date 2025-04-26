import xml.etree.ElementTree as ET

def parse_performance_ids(xml_data: str) -> list[str]:
    """전체 공연 목록 조회 API 결과에서 공연 ID(mt20id) 리스트 추출"""
    root = ET.fromstring(xml_data)
    ids = []

    for elem in root.findall(".//db"):  

        mt20id = elem.findtext("mt20id")
        if mt20id:
            ids.append(mt20id)

    return ids


def parse_performance_detail(xml_data: str) -> dict:

    """공연 상세 API 결과에서 필요한 정보만 추출"""
    root = ET.fromstring(xml_data)
    prf = root.find("db")

    if prf is None:
        return {}

    styurls = prf.find("styurls")
    styurl_list = []
    if styurls is not None:
        for item in styurls.findall("styurl"):
            if item.text:
                styurl_list.append(item.text)

    return {
        "mt20id": prf.findtext("mt20id"),
        "prfnm": prf.findtext("prfnm"),
        "prfpdfrom": prf.findtext("prfpdfrom"),
        "prfpdto": prf.findtext("prfpdto"),
        "prfcast": prf.findtext("prfcast"),
        "prfage": prf.findtext("prfage"),
        "sty": prf.findtext("sty"),
        "genrenm": prf.findtext("genrenm"),
        "styurls": styurl_list
    }
