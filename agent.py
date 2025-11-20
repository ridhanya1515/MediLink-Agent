# agent.py
"""
MediLink - multi-agent healthcare assistant (safe demo).
Coordinator uses A2A to talk to SymptomAgent and RecommendAgent.
Rewritten to remove deprecated google.adk and use google.generativeai instead.
"""

import google.generativeai as genai
from tools import lookup_symptom, create_appointment
import memory

genai.configure(api_key="YOUR_API_KEY_HERE")  # <-- Replace with your key

# ================ SIMPLE AGENT CLASS =====================

class SimpleAgent:
    def __init__(self, name, instruction, model="gemini-2.5-flash", tools=None):
        self.name = name
        self.instruction = instruction
        self.model = model
        self.tools = tools or []

    def run(self, message):
        """Call the Gemini model with instruction + message."""
        prompt = f"{self.instruction}\nUser: {message}"
        response = genai.GenerativeModel(self.model).generate_content(prompt)
        return response.text


# ================ AGENTS =================================

symptom_agent = SimpleAgent(
    name="SymptomAgent",
    model="gemini-2.5-flash",
    instruction=(
        "Extract the primary symptom keyword (e.g., 'fever', 'headache', 'cough'). "
        "Return only the keyword. If unclear, ask a clarifying question."
    )
)

recommend_agent = SimpleAgent(
    name="RecommendAgent",
    model="gemini-2.5-flash",
    instruction=(
        "Given a safe summary about a symptom, produce a short, general next-step "
        "suggestion. DO NOT diagnose. Focus on safety and when to seek care."
    )
)

# =============== COORDINATOR ==============================

class Coordinator:
    def run(self, user_msg):
        # 1) Extract symptom keyword
        symptom_keyword = symptom_agent.run(user_msg)

        # 2) Lookup safe info
        lookup_info = lookup_symptom(symptom_keyword.strip())

        # 3) Ask RecommendAgent
        advice = recommend_agent.run(lookup_info)

        # 4) Offer appointment
        appointment_offer = (
            "\nIf you'd like, I can create a demo appointment for you."
        )

        final_answer = (
            f"**Symptom:** {symptom_keyword}\n"
            f"**Info:** {lookup_info}\n"
            f"**Advice:** {advice}\n"
            f"{appointment_offer}"
        )
        return final_answer

    def create_demo_appointment(self, name):
        return create_appointment(name)


# Export coordinator object for runner.py
coordinator = Coordinator()
