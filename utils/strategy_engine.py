def generate_strategy_analysis(company, financial_analysis):
    growth = company.get("growth_rate", "0")
    growth = float(growth.replace("%", "")) if isinstance(growth, str) else 0
    risk = financial_analysis["risk_level"]

    if risk == "High" and growth < 10:
        strategy = "Defensive Strategy"
        focus = [
            "Cost optimization",
            "Reducing marketing spend",
            "Improving operational efficiency"
        ]
    elif risk == "Low" and growth >= 15:
        strategy = "Aggressive Growth Strategy"
        focus = [
            "Market expansion",
            "Increased marketing investment",
            "Strategic hiring"
        ]
    else:
        strategy = "Balanced Strategy"
        focus = [
            "Selective growth initiatives",
            "ROI-driven investments",
            "Process improvements"
        ]

    return {
        "strategy_type": strategy,
        "focus_areas": focus
    }
