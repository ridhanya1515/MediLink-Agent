"""
Runner for MediLink demo.
Works on Kaggle & GitHub without API keys.
"""

from agent import coordinator  # import main agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk import types


# Session service
session_service = InMemorySessionService()

# Connect runner to coordinator agent
runner = Runner(
    agent=coordinator,
    app_name="medilink_app",
    session_service=session_service
)


def run_medilink(message: str):
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


if __name__ == "__main__":
    # Quick test
    run_medilink("I have headache and small fever")
