import json
import os

# 로그
BASE_DIR = os.path.dirname(__file__)
LOG_FILE_PATH = os.path.join(BASE_DIR, "data", "log.txt")

def log(message: str):
    print(message)
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
    with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
        f.write(message + "\n")
        f.flush()


# JSON 
def load_json(path: str):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def save_json(data, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_existing_ids(path: str) -> set:
    data = load_json(path)
    return set(data) if data else set()

def save_existing_ids(ids: set, path: str):
    save_json(list(ids), path)
