# memory.py
"""
Simple file-backed long-term memory for demo (not encrypted).
Stores small JSON objects per user_id.
"""

import json
from pathlib import Path
from typing import Any, Dict

MEMORY_FILE = Path("data/memory.json")
MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)

def _load() -> Dict[str, Any]:
    if MEMORY_FILE.exists():
        try:
            return json.loads(MEMORY_FILE.read_text())
        except Exception:
            return {}
    return {}

def _save(data: Dict[str, Any]):
    MEMORY_FILE.write_text(json.dumps(data, indent=2))

def get_memory(user_id: str) -> Dict[str, Any]:
    data = _load()
    return data.get(user_id, {})

def update_memory(user_id: str, key: str, value: Any):
    data = _load()
    user = data.get(user_id, {})
    user[key] = value
    data[user_id] = user
    _save(data)
    return user
