# evaluate.py
"""
Simple evaluation runner that loads integration.evalset.json and runs through cases.
Saves result to .adk_eval_results.json
"""

import json
from runner import run_medilink

def load_evalset(path="integration.evalset.json"):
    with open(path, "r") as f:
        return json.load(f)

def run_all():
    evalset = load_evalset()
    results = []
    for case in evalset.get("eval_cases", []):
        prompt = case["conversation"][0]["user_content"]["parts"][0]["text"]
        print("=== Running:", case["eval_id"], "===", prompt)
        # This demo simply prints the output to console via run_medilink
        run_medilink(prompt)
        results.append({"eval_id": case["eval_id"], "status": "ran"})
    with open(".adk_eval_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("Evaluation run finished. Results saved to .adk_eval_results.json")

if __name__ == "__main__":
    run_all()
