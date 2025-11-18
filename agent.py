# agent.py
"""
MediLink - multi-agent healthcare assistant (safe demo).
Coordinator uses A2A to talk to SymptomAgent and RecommendAgent.
"""

from google.adk import Agent
from google.adk.tools import FunctionTool
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.models import Gemini
from google.adk import types as adk_types

from tools import lookup_symptom, create_appointment
import memory

# Tools wrapped as FunctionTool (ADK)
lookup_tool = FunctionTool(
    name="lookup_symptom",
    description="Return safe info about a simple symptom (non-diagnostic).",
    func=lookup_symptom,
)

appointment_tool = FunctionTool(
    name="create_appointment",
    description="Create a demo appointment (mock).",
    func=create_appointment,
)

# SymptomAgent: extracts keywords (A2A consumer)
symptom_agent = Agent(
    name="SymptomAgent",
    model=Gemini(model="gemini-2.5-flash"),
    instruction=(
        "Extract the primary symptom keyword (e.g., 'fever', 'headache', 'cough'). "
        "Return only the keyword as text if found, otherwise ask a clarifying question."
    ),
    tools=[lookup_tool],
)

# RecommendAgent: uses symptom info to craft safe recommendations
recommend_agent = Agent(
    name="RecommendAgent",
    model=Gemini(model="gemini-2.5-flash"),
    instruction=(
        "Given a safe summary about a symptom, produce a short, general next-step suggestion. "
        "Do NOT diagnose. Emphasize when to seek medical care and safety."
    ),
)

# Coordinator: orchestrator that uses A2A calls (agents list creates A2A capability)
coordinator = Agent(
    name="Coordinator",
    model=Gemini(model="gemini-2.5-flash"),
    agents=[symptom_agent, recommend_agent],
    tools=[appointment_tool],
    instruction=(
        "You orchestrate: 1) send the user's message to SymptomAgent to extract symptom; "
        "2) call lookup_symptom tool using the extracted symptom; 3) send the lookup result to RecommendAgent; "
        "4) optionally offer to create a demo appointment using create_appointment; 5) return a safe combined answer."
    ),
)
