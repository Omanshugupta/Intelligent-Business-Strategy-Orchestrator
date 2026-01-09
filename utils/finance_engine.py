import pandas as pd


def generate_financial_analysis(company, pl_df):
    revenue = company.get("revenue", 0)
    expenses = company.get("expenses", 0)
    profit = revenue - expenses
    margin = (profit / revenue) * 100 if revenue > 0 else -100

    # Trend analysis
    recent = pl_df.tail(3)
    rev_trend = recent["Revenue"].pct_change().mean()
    exp_trend = recent["Expenses"].pct_change().mean()

    # Risk level
    if profit < 0 or exp_trend > rev_trend:
        risk = "High"
    elif margin < 10:
        risk = "Medium"
    else:
        risk = "Low"

    analysis = {
        "profit": profit,
        "margin": round(margin, 2),
        "revenue_trend": round(rev_trend * 100, 2),
        "expense_trend": round(exp_trend * 100, 2),
        "risk_level": risk
    }

    # Human-readable insight
    if risk == "High":
        insight = (
            "The business is under financial stress. "
            "Expenses are growing faster than revenue, "
            "indicating an urgent need for cost control."
        )
    elif risk == "Medium":
        insight = (
            "The business shows moderate financial stability, "
            "but margins are thin and require optimization."
        )
    else:
        insight = (
            "The business demonstrates strong financial health "
            "with controlled expenses and healthy margins."
        )

    return analysis, insight
