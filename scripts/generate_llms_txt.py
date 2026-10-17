import json
import os

with open("assets/data/search-index.json", "r", encoding="utf-8") as f:
    items = json.load(f)

categories = {}
for item in items:
    cat = item.get("c", "General")
    categories.setdefault(cat, []).append(item)

header = """# PromptHook AI - Full Blueprint Catalogue (llms-full.txt)

> Complete programmatic registry of 1,960 hyper-optimized system directives, agentic architecture blueprints, and parameter injection frameworks published on PromptHook AI (https://www.prompthookai.com/).

## Overview
PromptHook AI provides production-ready, deterministic prompt blueprints for frontier LLMs (Claude 3.7 Sonnet, GPT-4o, DeepSeek R1, Grok 3, Gemini 2.0).
Each blueprint enforces:
- Operational Parameter Binding (`{{VARIABLE}}`)
- Model Tuning Matrix (Temperature, Top-P, Presence Penalty)
- Multi-Turn Execution Protocols
- Adversarial Diagnostic Guardrails & Anti-Hallucination Checks
- Deterministic Output Formatting (JSON Schemas, Code, Markdown)

"""

out = [header]

# Sort categories
for cat_name in sorted(categories.keys()):
    cat_items = categories[cat_name]
    out.append(f"\n## {cat_name} ({len(cat_items)} Blueprints)\n")
    for b in cat_items:
        title = b["t"]
        url = "https://www.prompthookai.com" + b["u"]
        out.append(f"- [{title}]({url})")

with open("llms-full.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out) + "\n")

print(f"Generated llms-full.txt with {len(items)} blueprints across {len(categories)} categories.")
