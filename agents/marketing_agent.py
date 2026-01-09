from llms.llm import llm

def marketing_agent(state):
    prompt = f"""
    You are a marketing manager.
    Based on the strategy below, suggest marketing channels and campaigns.

    Strategy:
    {state['strategy_output']}
    """
    response = llm.invoke(prompt)
    state["marketing_output"] = response.content
    return state
