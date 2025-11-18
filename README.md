MediLink — Multi-Agent Healthcare Assistant

Short Description
MediLink is an AI-powered multi-agent healthcare assistant that performs symptom triage, provides safe preliminary guidance, and supports basic healthcare workflow tasks using coordinated intelligent agents.

Project Goal

Build a reliable agentic healthcare prototype demonstrating:

Multi-agent communication (A2A)

Custom tool-calling

Sessions & memory

Context compaction

Observability (logging/tracing)

Evaluation using ADK

The system focuses on safe, explainable, and low-risk healthcare triage with simple appointment assistance.

Features

Extracts symptoms and returns structured information

Provides safe, general recommendations

Mock appointment scheduling

Multi-agent architecture (Coordinator, Symptom Agent, Recommendation Agent)

FunctionTool-based actions

Session-aware memory support

Context compaction (architecture ready)

Evaluation with test cases

Repository Structure
MediLink/
├─ README.md
├─ LICENSE
├─ .gitignore
├─ requirements.txt
├─ agent.py
├─ tools.py
├─ memory.py
├─ runner.py
├─ evaluate.py
├─ integration.evalset.json
├─ notebooks/
│   ├─ demo.ipynb
│   └─ evaluation.ipynb
├─ docs/
│   ├─ architecture.png
│   └─ submission_writeup.md
└─ tests/
    └─ integration.evalset.json

Overview

MediLink is a safe demonstration project built for the Kaggle × Google AI Agents Intensive Capstone.
It offers general, non-diagnostic healthcare assistance using multiple agents, tools, memory, and evaluation logic.

(Disclaimer: This prototype does not provide medical advice.)

Problem Statement

Searching symptoms online often results in:

Unsafe or inconsistent answers

Confusion

No structured follow-up

No clear next steps

MediLink fixes this by offering:

Structured symptom extraction

Safe guidance

Clear next-step suggestions

Simple appointment assistance

Memory-aware conversation flow

Solution

MediLink uses a coordinated multi-agent design:

1. Coordinator Agent

Routes tasks between agents and tools.

2. Symptom Agent

Extracts simple symptom keywords safely.

3. Recommendation Agent

Provides very general, safe, non-medical recommendations.

Tools

lookup_symptom → returns predefined safe info

create_appointment → mock appointment handler

The architecture ensures safety, modularity, and clarity.

Key Concepts Used

✔ Multi-agent system

✔ Custom FunctionTools

✔ Sessions & memory

✔ Long-term memory (file-based)

✔ Context compaction support

✔ A2A communication between agents

✔ Evaluation workflow

Architecture

How to Run
Install needed libraries:
pip install -r requirements.txt

Run the agent:
python runner.py

Evaluate:
python evaluate.py

File Description
File	Description
agent.py	All agent definitions and A2A logic
tools.py	Tools for symptom lookup & appointment
memory.py	Simple memory handling
runner.py	Runner for testing the main agent
evaluate.py	Evaluation script
notebooks/demo.ipynb	Interactive demo
notebooks/evaluation.ipynb	Evaluation notebook
docs/architecture.png	Architecture diagram
docs/submission_writeup.md	Kaggle write-up
tests/integration.evalset.json	Evaluation cases
Links

GitHub Repository: https://github.com/ridhanya1515/MediLink-Agent
