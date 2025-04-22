def build_summary_prompt(performance: dict) -> str:
    prfnm = performance.get("prfnm", "정보 없음")
    prfpdfrom = performance.get("prfpdfrom", "정보 없음")
    prfpdto = performance.get("prfpdto", "정보 없음")
    genrenm = performance.get("genrenm", "정보 없음")
    prfcast = performance.get("prfcast", "정보 없음")
    prfage = performance.get("prfage", "정보 없음")
    sty = performance.get("sty", "")
    pid = performance.get("mt20id", "정보 없음")

    return f"""
📌 작성 규칙
- 공연 ID(PID)는 그대로 유지해주세요.
- 공연 요약은 3~4문장 분량으로 작성해주세요.
- 정보 나열이 아닌, 관람하고 싶게 만드는 감성적인 문장으로 표현해주세요.
- 이모지는 포함하지 마세요.
- bullet point 형식으로 작성해주세요.
- 웹 검색이 가능하다면 최신 정보를 반영해주세요.
- 포스터 이미지(styurls)가 있을 경우, OCR로 문구를 추출하여 감성 요약에 참고하세요.

⚠️ 주의 사항
- 공연 제목에 ‘19’, ‘성인’ 등의 단어가 있어도, 반드시 prfage 값을 기준으로 공연 성격을 판단해주세요.
- OCR로 추출한 문구가 prfage, genre, 공식 정보와 상충할 경우, 공식 정보 기준으로 작성해주세요.
- 이미지 내 문구가 없거나 부정확할 경우, 그 내용을 지어내지 말고 생략해주세요.
- 정보가 부족하면 “정보를 찾을 수 없어요”라고 명시해주세요.

✅ 공연 정보
- 공연 ID: {pid}
- 제목: {prfnm}
- 기간: {prfpdfrom} ~ {prfpdto}
- 장르: {genrenm}
- 출연: {prfcast}
- 관람 연령: {prfage}
- 공연 소개: {sty}

✅ 출력 예시 (반드시 아래 형식으로 표기)
| 공연 ID | 공연 요약 |
|--------|-----------|
| {pid} | (공연 요약 3~4문장) |
"""
