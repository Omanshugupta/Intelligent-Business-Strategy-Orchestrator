from llms.llm import llm

def ceo_agent(state):
    prompt = f"""
    You are the CEO.
    Make a final executive decision based on all inputs.

    Strategy:
    {state['strategy_output']}

    Marketing:
    {state['marketing_output']}

    Finance:
    {state['finance_output']}

    HR:
    {state['hr_output']}

    Provide a concise executive summary and final decision.
    """
    response = llm.invoke(prompt)
    state["final_decision"] = response.content
    return state
