import json
import os

EXISTING_IDS_FILE = "existing_ids.json"

def load_existing_ids() -> set:
    if os.path.exists(EXISTING_IDS_FILE):
        with open(EXISTING_IDS_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()

def save_existing_ids(ids: set):
    with open(EXISTING_IDS_FILE, "w", encoding="utf-8") as f:
        json.dump(list(ids), f, ensure_ascii=False, indent=2)
