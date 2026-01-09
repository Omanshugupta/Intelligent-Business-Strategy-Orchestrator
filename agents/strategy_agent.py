from llms.llm import llm

def strategy_agent(state):
    prompt = f"""
    You are a business strategy consultant.
    Analyze the company data and suggest growth strategy and risks.

    Company Data:
    {state['company_data']}
    """
    response = llm.invoke(prompt)
    state["strategy_output"] = response.content
    return state
