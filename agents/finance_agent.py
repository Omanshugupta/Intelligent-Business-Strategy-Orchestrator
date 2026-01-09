from llms.llm import llm

def finance_agent(state):
    state["iteration_count"] += 1
    prompt = f"""
    You are a finance manager.
    Analyze profit/loss, financial risks, and cost optimization.

    Company Data:
    {state['company_data']}

    Marketing Plan:
    {state['marketing_output']}

    Clearly mention if there is LOSS or RISK.
    """
    response = llm.invoke(prompt)
    state["finance_output"] = response.content
    return state
