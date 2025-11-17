"""
MediLink Runner
This file demonstrates how the agents work together.
"""

import asyncio
from agent import coordinator_agent
from google.adk.runner import Runner
from google.adk.session import InMemorySessionService
from google.genai import types

async def run_chat():
    session_service = InMemorySessionService()

    runner = Runner(
        agent=coordinator_agent,
        app_name="medilink_app",
        session_service=session_service,
    )

    user_query = "I have fever and headache. What should I do?"
    print("\nUser:", user_query)

    msg = types.Content(parts=[types.Part(text=user_query)])

    async for event in runner.run_async(
        user_id="demo_user",
        session_id="session1",
        new_message=msg
    ):
        if event.is_final_response() and event.content:
            for part in event.content.parts:
                if hasattr(part, "text"):
                    print("\nMediLink:", part.text)

if __name__ == "__main__":
    asyncio.run(run_chat())
