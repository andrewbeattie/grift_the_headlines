import json
from typing import List, Dict

def json_save(file_path: str, data: List[Dict]):
    with open(file_path, "w+", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=True, indent=4)

def json_load(file_path: str) -> List[Dict]:
    with open(file_path, "r+", encoding="utf-8") as f:
        data = json.load(f)
    return data
