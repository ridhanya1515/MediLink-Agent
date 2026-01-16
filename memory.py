# memory.py
"""
Simple file-backed conversation memory for MediLink (SAFE DEMO).
Stores limited conversation history per user.
"""

import json
from pathlib import Path
from typing import Any, Dict, List

MEMORY_FILE = Path("data/memory.json")
MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)

MAX_MESSAGES = 10  # prevent unlimited growth

# ================= INTERNAL HELPERS =================

def _load() -> Dict[str, Any]:
    if MEMORY_FILE.exists():
        try:
            return json.loads(MEMORY_FILE.read_text())
        except Exception:
            return {}
    return {}

def _save(data: Dict[str, Any]):
    MEMORY_FILE.write_text(json.dumps(data, indent=2))

# ================= PUBLIC API =======================

def get_history(user_id: str) -> List[Dict[str, str]]:
    """
    Returns conversation history for a user.
    """
    data = _load()
    return data.get(user_id, {}).get("history", [])

def save_message(user_id: str, role: str, content: str):
    """
    Save a message to user conversation history.
    role: 'user' | 'assistant'
    """
    data = _load()
    user = data.get(user_id, {})

    history = user.get("history", [])
    history.append({"role": role, "content": content})

    # Keep last N messages only
    history = history[-MAX_MESSAGES:]

    user["history"] = history
    data[user_id] = user

    _save(data)

def clear_memory(user_id: str):
    """
    Clears memory for a user.
    """
    data = _load()
    if user_id in data:
        del data[user_id]
        _save(data)
