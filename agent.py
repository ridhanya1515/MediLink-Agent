"""
MediLink - Multi-Agent Healthcare Assistant (Safe Demo)
This version is FIXED for Kaggle (google-adk latest version).
"""

from google.adk import Agent
from google.adk.tools import FunctionTool   
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.models import Gemini
from google.adk import types
import json


# -------------------------------------------------------------------
# 1. Simple Medical Database (safe demo)
# -------------------------------------------------------------------
MEDICAL_DB = {
    "fever": {
        "possible_causes": ["common cold", "viral infection"],
        "advice": "Drink fluids, rest, and monitor temperature."
    },
    "headache": {
        "possible_causes": ["stress", "dehydration"],
        "advice": "Hydrate, rest, avoid screens."
    },
    "cough": {
        "possible_causes": ["cold", "throat irritation"],
        "advice": "Warm fluids and avoid dust."
    }
}


# -------------------------------------------------------------------
# 2. TOOL: lookup symptom (fixed)
# -------------------------------------------------------------------
def lookup_symptom(symptom: str):
    symptom = symptom.lower().strip()
    if symptom in MEDICAL_DB:
        return MEDICAL_DB[symptom]
    return {"error": "No data available for this symptom."}


lookup_tool = FunctionTool(
    name="lookup_symptom",
    description="Returns basic safe demo info for a symptom.",
    func=lookup_symptom,
)


# -------------------------------------------------------------------
# 3. AGENT: Symptom Agent
# -------------------------------------------------------------------
symptom_agent = Agent(
    name="SymptomAgent",
    model=Gemini(model="gemini-2.5-flash"),
    instruction=(
        "Extract simple symptom keywords such as fever, cough, headache. "
        "Do NOT diagnose. Only identify keywords."
    ),
    tools=[lookup_tool],
)


# -------------------------------------------------------------------
# 4. AGENT: Recommendation Agent
# -------------------------------------------------------------------
recommend_agent = Agent(
    name="RecommendAgent",
    model=Gemini(model="gemini-2.5-flash"),
    instruction=(
        "Give VERY general safe recommendations such as rest, hydration, "
        "or seeing a doctor. Avoid medical statements."
    )
)


# -------------------------------------------------------------------
# 5. Coordinator Agent (main)
# -------------------------------------------------------------------
coordinator = Agent(
    name="Coordinator",
    model=Gemini(model="gemini-2.5-flash"),
    agents=[symptom_agent, recommend_agent],
    instruction=(
        "You coordinate:\n"
        "1. Send message to SymptomAgent to extract symptom.\n"
        "2. Call lookup_symptom tool.\n"
        "3. Send info to RecommendAgent.\n"
        "4. Return combined safe answer."
    ),
)


# -------------------------------------------------------------------
# 6. Runner for notebook
# -------------------------------------------------------------------
session_service = InMemorySessionService()
runner = Runner(agent=coordinator, app_name="medilink_app", session_service=session_service)


def run_medilink(message: str):
    """
    Helper for Kaggle notebook.
    """
    print(f"User: {message}\n---")
    content = types.Content(parts=[types.Part(text=message)])
    session_id = "demo_session"

    for event in runner.run(
        user_id="demo_user",
        session_id=session_id,
        new_message=content
    ):
        if event.is_final_response() and event.content:
            for part in event.content.parts:
                if hasattr(part, "text"):
                    print("MediLink:", part.text)

    print("\n")
