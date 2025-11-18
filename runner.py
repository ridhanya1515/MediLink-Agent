# runner.py
"""
Run MediLink demo locally or in Kaggle. No real API keys needed for this mock demo.
"""

from agent import coordinator
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk import types as adk_types

session_service = InMemorySessionService()
runner = Runner(agent=coordinator, app_name="medilink_app", session_service=session_service)

def run_medilink(message: str, user_id: str = "demo_user", session_id: str = "demo_session"):
    print(f"User: {message}\n---")
    content = adk_types.Content(parts=[adk_types.Part(text=message)])
    for event in runner.run(user_id=user_id, session_id=session_id, new_message=content):
        if event.is_final_response() and event.content:
            for part in event.content.parts:
                if hasattr(part, "text"):
                    print("MediLink:", part.text)
    print("\n")

if __name__ == "__main__":
    run_medilink("I have headache and a small fever")
