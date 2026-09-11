# crypto/utils.py
import os
import json
from typing import Any

def save_bytes(path: str, data: bytes):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)

def load_bytes(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()

def save_json(path: str, obj: Any):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f)

def load_json(path: str):
    with open(path, "r") as f:
        return json.load(f)
