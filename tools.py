# tools.py
import json
from datetime import datetime
from typing import Dict, Any

# Simple safe demo "database" and appointment tool for MediLink.

MEDICAL_DB = {
    "fever": {
        "possible_causes": ["common cold", "viral infection"],
        "advice": "Drink fluids, rest, and monitor temperature."
    },
    "headache": {
        "possible_causes": ["stress", "dehydration"],
        "advice": "Hydrate, rest, avoid bright screens."
    },
    "cough": {
        "possible_causes": ["cold", "throat irritation"],
        "advice": "Warm fluids and avoid dust."
    }
}

def lookup_symptom(symptom: str) -> Dict[str, Any]:
    """Return safe, non-diagnostic info about a symptom."""
    s = symptom.lower().strip()
    if s in MEDICAL_DB:
        return {"ok": True, "symptom": s, "data": MEDICAL_DB[s]}
    return {"ok": False, "error": "No safe data for that symptom."}

# Simple in-memory mock appointment calendar (not linked to real calendar)
APPOINTMENTS = []

def create_appointment(patient_name: str, date_iso: str, reason: str) -> Dict[str, Any]:
    """Create a demo appointment (safe mock). date_iso should be YYYY-MM-DD or ISO."""
    try:
        # Basic validation
        dt = datetime.fromisoformat(date_iso)
    except Exception:
        return {"ok": False, "error": "Invalid date format. Use YYYY-MM-DD or full ISO."}

    appt = {
        "id": len(APPOINTMENTS) + 1,
        "patient": patient_name,
        "date": dt.date().isoformat(),
        "reason": reason
    }
    APPOINTMENTS.append(appt)
    return {"ok": True, "appointment": appt}
