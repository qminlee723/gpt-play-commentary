import openai
from openai import OpenAIError, BadRequestError 
import json
import csv
import os
import requests
from PIL import Image
from io import BytesIO
import pytesseract
from time import sleep
from gpt_prompt import build_summary_prompt

# ✅ 최신 방식: OpenAI client 인스턴스 생성
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ✅ GPT 요약 생성 함수 (단건)
def generate_summary(performance):
    prompt = build_summary_prompt(performance)

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content
    
    except BadRequestError as e:
        print(f"[요청 오류] {performance.get('mt20id')}: {e}")
        return "요청 오류로 요약 실패"
    
    except OpenAIError as e:
        print(f"[GPT 오류] {performance.get('mt20id')}: {e}")
        return "GPT 오류 발생"
    
    except Exception as e:
        print(f"[기타 오류] {performance.get('mt20id')}: {e}")
        return "오류 발생"

# ✅ 단건 테스트용
def process_and_save(json_path, output_csv):
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    summaries = []
    for i, item in enumerate(data[:3]):
        print(f"{i+1}/{len(data)} 처리 중: {item['prfnm']}")
        summary = generate_summary(item)
        summaries.append({"공연 ID": item["mt20id"], "공연 요약": summary})
        sleep(2)

    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["공연 ID", "공연 요약"])
        writer.writeheader()
        writer.writerows(summaries)

    print(f"\n✅ 단건 요약 저장 완료 → {output_csv}")

# ✅ 배치 처리용
def process_and_save_batch(json_path, output_csv, chunk_size=10):

    def chunk_list(data, chunk_size):
        for i in range(0, len(data), chunk_size):
            yield data[i:i + chunk_size]

    def parse_gpt_table(text):
        rows = []
        for line in text.splitlines():
            if line.startswith("|") and not any(sub in line for sub in ["| 공연 ID", "|--------"]):
                parts = [col.strip() for col in line.strip().split("|")[1:-1]]
                if len(parts) == 2:
                    rows.append({"공연 ID": parts[0], "공연 요약": parts[1]})
        return rows

    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    all_rows = []
    for i, chunk in enumerate(chunk_list(data, chunk_size)):
        print(f"\n🧠 GPT 요청 {i+1}차 (총 {len(chunk)}개)")
        prompts = []
        for perf in chunk:
            prompts.append(build_summary_prompt(perf))

        combined_prompt = "\n\n---\n\n".join(prompts)

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": combined_prompt}],
                temperature=0.7
            )
            gpt_output = response.choices[0].message.content
            parsed_rows = parse_gpt_table(gpt_output)
            all_rows.extend(parsed_rows)
            print(f"✅ 요약 {len(parsed_rows)}개 완료")
            
        except BadRequestError as e:
            print(f"[요청 오류 - 배치 {i+1}] {e}")
        except OpenAIError as e:
            print(f"[GPT 오류 - 배치 {i+1}] {e}")
        except Exception as e:
            print(f"[기타 오류 - 배치 {i+1}] {e}")

        sleep(2)

    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["공연 ID", "공연 요약"])
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"\n✅ 모든 배치 요약 저장 완료 → {output_csv}")
