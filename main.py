import json
from graph.decision_graph import build_graph

with open("data/company_data.json") as f:
    company_data = json.load(f)

app = build_graph()

state = {
    "company_data": company_data,
    "strategy_output": "",
    "marketing_output": "",
    "finance_output": "",
    "hr_output": "",
    "final_decision": "",
    "iteration_count": 0
}

result = app.invoke(state)
with open("output.json", "w") as f:
    json.dump(result, f, indent=2)

print("Pipeline executed successfully")
