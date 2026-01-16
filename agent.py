# agent.py
"""
Coordinator agent for MediLink.
Decides which tool to use and generates safe responses.
"""

from tools import lookup_symptom, create_appointment
from memory import update_memory

class CoordinatorAgent:
    def run(self, user_message: str) -> str:
        text = user_message.lower()

        # ---------- APPOINTMENT INTENT ----------
        if "book" in text or "appointment" in text:
            return self._handle_appointment(user_message)

        # ---------- SYMPTOM INTENT ----------
        for symptom in ["fever", "headache", "cough"]:
            if symptom in text:
                info = lookup_symptom(symptom)

                update_memory(
                    user_id="demo_user",
                    key="last_symptom",
                    value=symptom
                )

                return (
                    f"{info}\n\n"
                    "If symptoms become severe or persistent, consider seeking medical care."
                )

        # ---------- FALLBACK ----------
        return (
            "I can help with general symptom information or booking a doctor appointment. "
            "Please describe your symptoms or request an appointment."
        )

    def _handle_appointment(self, text: str) -> str:
        # VERY SIMPLE parsing (demo purpose)
        date = "2025-12-05"
        reason = "general checkup"

        if "cough" in text:
            reason = "cough"
        if "fever" in text:
            reason = "fever"

        result = create_appointment(
            patient_name="Demo",
            date_iso=date,
            reason=reason
        )

        if not result["ok"]:
            return "Sorry, I could not create the appointment. Please check the date."

        appt = result["appointment"]
        return (
            f"Your appointment has been booked successfully.\n"
            f"Date: {appt['date']}\n"
            f"Reason: {appt['reason']}"
        )

# Single coordinator instance
coordinator = CoordinatorAgent()
