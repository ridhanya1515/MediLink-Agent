# runner.py
"""
Run MediLink demo locally.
This runner directly calls the Coordinator (NO ADK).
"""

from agent import coordinator

def run_medilink(message: str):
    """
    Runs MediLink and RETURNS the response (important for evaluation).
    """
    print(f"User: {message}\n---")

    response = coordinator.run(message)

    print("MediLink:")
    print(response)
    print("\n")

    return response   # ✅ REQUIRED for evaluate.py

# ================= ENTRY POINT ====================

if __name__ == "__main__":
    user_input = input("Describe your symptoms: ")
    run_medilink(user_input)
