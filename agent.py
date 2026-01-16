# agent.py
"""
MediLink - Multi-Agent Healthcare Assistant (SAFE DEMO)

Agents:
1. SymptomAgent   -> Extract primary symptom
2. SafetyAgent    -> Detect red-flag / emergency symptoms
3. RecommendAgent -> Provide safe, non-diagnostic guidance

Coordinator orchestrates agents and manages memory.
"""

import os
import google.generativeai as genai
from tools import lookup_symptom, create_appointment
import memory

# ================= API CONFIG =====================

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ================= SIMPLE AGENT ===================

class SimpleAgent:
    def __init__(self, name, instruction, model="gemini-2.5-flash"):
        self.name = name
        self.instruction = instruction
        self.model = model

    def run(self, message: str) -> str:
        prompt = f"{self.instruction}\n\nInput:\n{message}\n\nOutput:"
        model = genai.GenerativeModel(self.model)
        response = model.generate_content(prompt)
        return response.text.strip()

# ================= AGENTS =========================

symptom_agent = SimpleAgent(
    name="SymptomAgent",
    instruction=(
        "Extract ONE primary symptom keyword from the input.\n"
        "Return ONLY a single lowercase word.\n"
        "Examples: fever, headache, cough.\n"
        "If unclear, return: unclear"
    )
)

safety_agent = SimpleAgent(
    name="SafetyAgent",
    instruction=(
        "Check if the input mentions any emergency or red-flag symptoms such as:\n"
        "chest pain, difficulty breathing, seizures, loss of consciousness, severe bleeding.\n"
        "Return ONLY 'YES' or 'NO'."
    )
)

recommend_agent = SimpleAgent(
    name="RecommendAgent",
    instruction=(
        "Provide general, safe health guidance based on the information.\n"
        "DO NOT diagnose.\n"
        "Mention when to seek medical care.\n"
        "Keep the response short, calm, and supportive."
    )
)

# ================= COORDINATOR ====================

class Coordinator:
    def run(self, user_msg: str, user_id: str = "demo_user") -> str:
        """
        Main orchestration logic for MediLink.
        """

        # Save user message to memory
        memory.save_message(user_id, "user", user_msg)

        # 1️⃣ Safety / red-flag check
        danger = safety_agent.run(user_msg)
        if danger == "YES":
            response = (
                "⚠️ Your symptoms may indicate a medical emergency.\n"
                "Please seek immediate medical care or contact emergency services."
            )
            memory.save_message(user_id, "assistant", response)
            return response

        # 2️⃣ Extract symptom
        symptom = symptom_agent.run(user_msg)
        if symptom == "unclear":
            response = "Could you please describe your main symptom more clearly?"
            memory.save_message(user_id, "assistant", response)
            return response

        # 3️⃣ Lookup safe symptom information
        info_text = lookup_symptom(symptom)

        # 4️⃣ Generate safe recommendation
        advice = recommend_agent.run(info_text)

        final_response = (
            f"Symptom identified: {symptom}\n\n"
            f"{info_text}\n\n"
            f"Guidance:\n{advice}\n\n"
            "If you want, I can also help you create a demo doctor appointment."
        )

        # Save assistant response
        memory.save_message(user_id, "assistant", final_response)

        return final_response

    def create_demo_appointment(self, name: str, date_iso: str, reason: str):
        """
        Optional appointment creation hook.
        """
        return create_appointment(name, date_iso, reason)

# ================= EXPORT =========================

coordinator = Coordinator()
