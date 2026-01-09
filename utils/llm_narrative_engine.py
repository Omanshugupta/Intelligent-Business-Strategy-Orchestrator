from llms.llm import llm

def generate_financial_narrative(company, financial_metrics):
    prompt = f"""
You are a senior management consultant preparing an executive financial review.

Context:
- Revenue: {company.get('revenue')}
- Expenses: {company.get('expenses')}
- Net Result: {financial_metrics['profit']}
- Operating Margin: {financial_metrics['margin']}%
- Financial Risk Classification: {financial_metrics['risk_level']}
- Revenue Growth Trend (%): {financial_metrics['revenue_trend']}
- Expense Growth Trend (%): {financial_metrics['expense_trend']}

Instructions:
Write a formal, executive-level financial assessment.
Use precise business language.
Avoid casual phrasing and generic statements.
Focus on implications, sustainability, and financial discipline.
Structure the response as a professional management commentary.
"""
    return llm.invoke(prompt).content


def generate_strategy_narrative(company, strategy, financial_metrics):
    prompt = f"""
You are a strategy consultant presenting to the executive committee.

Context:
- Growth Rate: {company.get('growth_rate')}
- Financial Risk Profile: {financial_metrics['risk_level']}
- Recommended Strategic Posture: {strategy['strategy_type']}
- Strategic Focus Areas: {strategy['focus_areas']}

Instructions:
Provide a professional strategic rationale.
Explain the strategic logic and trade-offs.
Avoid operational language; focus on strategic intent.
Use terminology suitable for board-level discussion.
"""
    return llm.invoke(prompt).content




def generate_marketing_narrative(marketing_analysis):
    prompt = f"""
You are a senior go-to-market and growth strategy advisor.

Context:
- Channel Contribution Mix: {marketing_analysis['channels']}
- Channel ROI Performance: {marketing_analysis['roi']}

Instructions:
Deliver a professional assessment of marketing effectiveness.
Focus on efficiency, capital allocation, and performance differentials.
Avoid tactical advice; frame insights at a strategic level.
Use language appropriate for executive leadership.
"""
    return llm.invoke(prompt).content


def generate_ceo_narrative(company, financial_metrics, strategy, marketing_analysis):
    prompt = f"""
You are the Chief Executive Officer preparing a formal decision memorandum.

Context:
- Financial Risk Level: {financial_metrics['risk_level']}
- Net Result: {financial_metrics['profit']}
- Strategic Posture: {strategy['strategy_type']}
- Strategic Priorities: {strategy['focus_areas']}
- Marketing Assessment: {marketing_analysis['summary']['recommendation']}

Instructions:
Produce a concise, authoritative CEO-level synthesis.
Use professional, non-emotional language.
Clearly articulate priorities, constraints, and directional intent.
Explicitly state what the organization will prioritize and what it will defer.
This should read like a board-ready decision memo.
"""
    return llm.invoke(prompt).content
