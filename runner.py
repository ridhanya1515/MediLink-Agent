# runner.py
"""
Local runner for MediLink (used by evaluate.py)
"""

from agent import coordinator


def run_medilink(message: str):
    return coordinator.run(message)


if __name__ == "__main__":
    user_input = input("Describe your symptoms: ")
    print(run_medilink(user_input))
