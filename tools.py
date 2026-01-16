# tools.py
"""
Safe medical tools for MediLink (NON-diagnostic).
"""

from datetime import datetime
from typing import Dict, Any

# ================= SAFE MEDICAL DB =================

MEDICAL_DB = {
    "fever": {
        "possible_causes": ["common cold", "viral infection"],
        "advice": "Drink fluids, rest, and monitor temperature."
    },
    "headache": {
        "possible_causes": ["stress", "dehydration"],
        "advice": "Hydrate well, rest, and reduce screen time."
    },
    "cough": {
        "possible_causes": ["common cold", "throat irritation"],
        "advice": "Drink warm fluids and avoid dust or smoke."
    }
}

# ================= SYMPTOM LOOKUP ==================

def lookup_symptom(symptom: str) -> str:
    """
    Return SAFE, TEXT-ONLY medical information.
    This text is passed to the LLM (NO diagnosis).
    """
    s = symptom.lower().strip()

    if s not in MEDICAL_DB:
        return (
            "There is limited general information available for this symptom. "
            "If it persists or worsens, consider seeking medical advice."
        )

    data = MEDICAL_DB[s]

    return (
        f"General information about {s}: "
        f"Common non-serious causes may include {', '.join(data['possible_causes'])}. "
        f"General care advice: {data['advice']}"
    )

# ================= APPOINTMENT TOOL =================

APPOINTMENTS = []  # In-memory mock storage

def create_appointment(patient_name: str, date_iso: str, reason: str) -> Dict[str, Any]:
    """
    Create a demo appointment (SAFE MOCK).
    """
    try:
        dt = datetime.fromisoformat(date_iso)
    except Exception:
        return {
            "ok": False,
            "error": "Invalid date format. Use YYYY-MM-DD."
        }

    appointment = {
        "id": len(APPOINTMENTS) + 1,
        "patient": patient_name,
        "date": dt.date().isoformat(),
        "reason": reason
    }

    APPOINTMENTS.append(appointment)

    return {
        "ok": True,
        "appointment": appointment
    }
