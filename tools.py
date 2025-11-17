"""
MediLink Tools
These are helper tools used by the agents.
All data is SAFE, NON-MEDICAL, and demo-only.
"""

import json

FAKE_APPOINTMENTS = {
    "slots": [
        "Tomorrow 10:00 AM",
        "Tomorrow 4:00 PM",
        "Day after tomorrow 11:30 AM"
    ]
}

def lookup_condition(condition: str) -> str:
    """Return simple predefined info for a condition (safe demo only)."""
    data = {
        "fever": {
            "info": "A temporary increase in body temperature.",
            "advice": "Drink fluids and rest."
        },
        "cough": {
            "info": "A reflex to clear your airways.",
            "advice": "Sip warm fluids and stay in a clean space."
        },
        "headache": {
            "info": "Pain or discomfort in the head.",
            "advice": "Rest, hydrate, and avoid bright lights."
        }
    }

    condition = condition.lower().strip()
    return json.dumps(data.get(condition, {"error": "No data found"}), indent=2)

def book_appointment(name: str) -> str:
    """Returns a fake appointment slot."""
    return json.dumps({
        "patient": name,
        "available_slots": FAKE_APPOINTMENTS["slots"]
    }, indent=2)
