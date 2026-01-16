# agent.py
"""
MediLink - Multi-Agent Healthcare Assistant (SAFE DEMO)
------------------------------------------------------
Agents:
1. SymptomAgent      -> Extract symptom keyword
2. SafetyAgent       -> Check for red-flag symptoms
3. RecommendAgent    -> Provide safe guidance (NO diagnosis)

Coordinator orchestrates agents.
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

    def run(self, message):
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
        "Check if the symptom description contains any RED-FLAG signs "
        "(chest pain, breathing difficulty, seizures, loss of consciousness, severe bleeding).\n"
        "Return only YES or NO."
    )
)

recommend_agent = SimpleAgent(
    name="RecommendAgent",
    instruction=(
        "Provide safe, general health guidance based on the symptom.\n"
        "DO NOT diagnose.\n"
        "Mention when to seek medical care.\n"
        "Keep it short and reassuring."
    )
)

# ================= COORDINATOR ====================

class Coordinator:
    def run(self, user_msg):
        # Store user message in memory
        memory.save_message("user", user_msg)

        # 1. Safety check
        danger = safety_agent.run(user_msg)
        if danger == "YES":
            return (
                "⚠️ Your symptoms may need urgent medical attention.\n"
                "Please seek immediate care or contact emergency services."
            )

        # 2. Extract symptom
        symptom = symptom_agent.run(user_msg)
        if symptom == "unclear":
            return "Could you please describe your main symptom more clearly?"

        # 3. Lookup safe information
        info = lookup_symptom(symptom)

        # 4. Generate recommendation
        advice = recommend_agent.run(info)

        # Save system response
        memory.save_message("assistant", advice)

        return (
            f"**Symptom Identified:** {symptom}\n\n"
            f"**General Information:** {info}\n\n"
            f"**Guidance:** {advice}\n\n"
            "If you'd like, I can help you create a demo doctor appointment."
        )

    def create_demo_appointment(self, name):
        return create_appointment(name)

# Export coordinator
coordinator = Coordinator()
