"""
MediLink - Multi-Agent Healthcare Assistant
Main agent definitions.
Note: This is a SAFE demonstration prototype ONLY.
"""

from google.adk import Agent, Tool
from google.adk.tools import CodeExecutionTool
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.models import Gemini
from google.adk import types
import json

# -------------------------------------------------------------------
# 1. Simple Medical Database (fake, safe, non-medical content)
# -------------------------------------------------------------------
MEDICAL_DB = {
    "fever": {
        "possible_causes": ["common cold", "viral infection"],
        "advice": "Stay hydrated, rest, and monitor your temperature."
    },
    "headache": {
        "possible_causes": ["stress", "dehydration"],
        "advice": "Drink water, rest, and avoid bright screens."
    },
    "cough": {
        "possible_causes": ["cold", "throat irritation"],
        "advice": "Sip warm fluids and avoid dust."
    }
}

# -------------------------------------------------------------------
# 2. TOOL: Lookup simple symptom info
# -------------------------------------------------------------------
def lookup_symptom(symptom: str) -> str:
    symptom = symptom.lower().strip()
    if symptom in MEDICAL_DB:
        return json.dumps(MEDICAL_DB[symptom], indent=2)
    return json.dumps({"error": "No data available for this symptom."})

lookup_tool = Tool(
    name="lookup_symptom",
    description="Returns basic safe info for a symptom.",
    func=lookup_symptom,
    args_schema={"symptom": "string"}
)

# -------------------------------------------------------------------
# 3. AGENT: Symptom Understanding Agent
# -------------------------------------------------------------------
symptom_agent = Agent(
    name="SymptomAgent",
    model=Gemini(model="gemini-2.5-flash-lite"),
    instruction=(
        "You help understand user symptoms in a SAFE and GENERAL way. "
        "You NEVER diagnose. You only identify keywords like 'fever' or 'cough'."
    ),
    tools=[lookup_tool]
)

# -------------------------------------------------------------------
# 4. AGENT: Recommendation Agent
# -------------------------------------------------------------------
recommend_agent = Agent(
    name="RecommendAgent",
    model=Gemini(model="gemini-2.5-flash-lite"),
    instruction=(
        "You give general safe next-step recommendations. "
        "Avoid medical claims. Suggest hydration, rest, or seeing a doctor if needed."
    )
)

# -------------------------------------------------------------------
# 5. AGENT: Coordinator (Main agent)
# -------------------------------------------------------------------
coordinator = Agent(
    name="Coordinator",
    model=Gemini(model="gemini-2.5-flash-lite"),
    instruction=(
        "You coordinate between agents. Steps:\n"
        "1. Send user message to SymptomAgent to identify symptom.\n"
        "2. Forward extracted symptom to lookup tool.\n"
        "3. Send info to RecommendAgent.\n"
        "4. Return final combined answer.\n"
        "Always keep responses safe and general."
    ),
    # The coordinator calls the other agents
    agents=[symptom_agent, recommend_agent]
)

# -------------------------------------------------------------------
# 6. RUNNER (Test runner used in notebooks)
# -------------------------------------------------------------------
session_service = InMemorySessionService()
runner = Runner(agent=coordinator, app_name="medilink_app", session_service=session_service)

def run_medilink(message: str):
    """
    Helper for notebooks. Runs the coordinator agent.
    """
    content = types.Content(parts=[types.Part(text=message)])
    session_id = "demo_session"

    print(f"User: {message}\n---")

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
