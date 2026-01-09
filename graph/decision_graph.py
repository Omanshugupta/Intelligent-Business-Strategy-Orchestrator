from typing import TypedDict
from langgraph.graph import StateGraph, END

from agents.strategy_agent import strategy_agent
from agents.marketing_agent import marketing_agent
from agents.finance_agent import finance_agent
from agents.hr_agent import hr_agent
from agents.ceo_agent import ceo_agent


class MBAState(TypedDict):
    company_data: dict
    strategy_output: str
    marketing_output: str
    finance_output: str
    hr_output: str
    final_decision: str
    iteration_count: int

MAX_ITERATIONS = 3

def route_after_finance(state: MBAState):
    if state["iteration_count"] >= MAX_ITERATIONS:
        return "ceo"

    finance_text = state["finance_output"].lower()
    if "loss" in finance_text or "risk" in finance_text:
        return "strategy"   # Re-plan
    return "hr"             # Continue


def build_graph():
    graph = StateGraph(MBAState)

    graph.add_node("strategy", strategy_agent)
    graph.add_node("marketing", marketing_agent)
    graph.add_node("finance", finance_agent)
    graph.add_node("hr", hr_agent)
    graph.add_node("ceo", ceo_agent)

    graph.set_entry_point("strategy")

    graph.add_edge("strategy", "marketing")
    graph.add_edge("marketing", "finance")

    graph.add_conditional_edges(
        "finance",
        route_after_finance,
        {
            "strategy": "strategy",
            "hr": "hr",
            "ceo" : "ceo"
        }
    )

    graph.add_edge("hr", "ceo")
    graph.add_edge("ceo", END)

    return graph.compile()
