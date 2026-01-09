from llms.llm import llm

def hr_agent(state):
    prompt = f"""
    You are an HR manager.
    Suggest hiring, downsizing, or reskilling decisions.

    Strategy:
    {state['strategy_output']}

    Finance Analysis:
    {state['finance_output']}
    """
    response = llm.invoke(prompt)
    state["hr_output"] = response.content
    return state
