# memory.py
"""
Simple file-backed memory for MediLink (demo only).
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


def update_memory(user_id: str, key: str, value: Any):
    """
    Update memory for a user.
    """
    data = _load()
    user = data.get(user_id, {})
    user[key] = value
    data[user_id] = user
    _save(data)
    return user
