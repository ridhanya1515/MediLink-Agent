"""
Local evaluation script for MediLink.
Checks agent response similarity and tool usage.
"""

import json
from google.adk.evaluation.local_eval_service import LocalEvalService
from google.adk.evaluation.evaluation_config import EvaluationConfig

def run_evaluation():
    evalset_path = "tests/integration.evalset.json"
    config_path = None  # default criteria

    eval_service = LocalEvalService()
    results = eval_service.evaluate_evalset(
        evalset_path=evalset_path,
        config_path=config_path,
        print_detailed=True
    )

    print("\n=== Evaluation Summary ===")
    print(json.dumps(results.summary(), indent=2))

if __name__ == "__main__":
    run_evaluation()
