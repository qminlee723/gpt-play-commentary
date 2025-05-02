import openai
from openai import OpenAIError, BadRequestError 
import json
import csv
import os
import pandas as pd
from utils import log
from time import sleep
from gpt_prompt import build_summary_prompt

# ✅ 최신 방식: OpenAI client 인스턴스 생성
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ✅ GPT 요약 생성 함수 (단건)
def generate_summary(performance):
    prompt = build_summary_prompt(performance)

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "당신은 공연 정보를 요약해주는 친절한 전문가입니다."},
                {"role": "user", "content": prompt}
                ],
            temperature=0.7
        )
        return response.choices[0].message.content.replace('\n', '\\n')
    
    except BadRequestError as e:
        log(f"[요청 오류] {performance.get('mt20id')}: {e}")
        return "요청 오류로 요약 실패"
    
    except OpenAIError as e:
        log(f"[GPT 오류] {performance.get('mt20id')}: {e}")
        return "GPT 오류 발생"
    
    except Exception as e:
        log(f"[기타 오류] {performance.get('mt20id')}: {e}")
        return "오류 발생"


# ✅ 청크 처리용
def process_and_save_batch(json_path, output_csv, chunk_size=10):
    def chunk_list(data, chunk_size):
        for i in range(0, len(data), chunk_size):
            yield data[i:i + chunk_size]

    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    # ✅ 이미 요약된 공연 ID 로딩 (중단 복구용)
    if os.path.exists(output_csv):
        try:
            done_ids = set(pd.read_csv(output_csv)["공연 ID"])
            log(f"✅ 이미 완료된 공연 수: {len(done_ids)}")
        except Exception as e:
            log(f"[CSV 읽기 오류] {e}")
            done_ids = set()
    else:
        done_ids = set()

    # ✅ 아직 요약되지 않은 공연만 필터링
    data = [d for d in data if d["mt20id"] not in done_ids]

    write_mode = "a" if os.path.exists(output_csv) else "w"
    with open(output_csv, write_mode, newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["공연 ID", "공연 요약"])
        if write_mode == "w":
            writer.writeheader()

        for i, chunk in enumerate(chunk_list(data, chunk_size)):
            log(f"\n🧠 GPT 요청 {i+1}차 (총 {len(chunk)}개)")

            for j, perf in enumerate(chunk):
                try:
                    log(f"  - {j+1}/{len(chunk)}: {perf['prfnm']} 요약 중...")
                    summary = generate_summary(perf)
                    writer.writerow({
                        "공연 ID": perf["mt20id"],
                        "공연 요약": summary
                    })
                    f.flush()  # ✅ 매 건 저장

                except BadRequestError as e:
                    log(f"[요청 오류 - {perf['mt20id']}] {e}")
                    writer.writerow({"공연 ID": perf["mt20id"], "공연 요약": "요청 오류로 요약 실패"})
                    f.flush()
                except OpenAIError as e:
                    log(f"[GPT 오류 - {perf['mt20id']}] {e}")
                    writer.writerow({"공연 ID": perf["mt20id"], "공연 요약": "GPT 오류 발생"})
                    f.flush()
                except Exception as e:
                    log(f"[기타 오류 - {perf['mt20id']}] {e}")
                    writer.writerow({"공연 ID": perf["mt20id"], "공연 요약": "오류 발생"})
                    f.flush()

    print(f"\n✅ 모든 배치 요약 저장 완료 → {output_csv}")



# ✅ 단건 테스트용(3개)
def process_and_save(json_path, output_csv):
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    summaries = []
    for i, item in enumerate(data[:3]):
        log(f"{i+1}/{len(data)} 처리 중: {item['prfnm']}")

        summary = generate_summary(item)
        summaries.append({"공연 ID": item["mt20id"], "공연 요약": summary})

    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["공연 ID", "공연 요약"])
        writer.writeheader()
        writer.writerows(summaries)

    log(f"\n✅ 단건 요약 저장 완료 → {output_csv}")