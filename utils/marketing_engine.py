import pandas as pd


def generate_marketing_analysis(company_data: dict, pl_df: pd.DataFrame) -> dict:
    """
    Automatically generate marketing channel contribution, ROI,
    and strategic insights using business + financial signals.
    """

    # -------------------------------
    # BASIC BUSINESS SIGNALS
    # -------------------------------
    revenue = company_data.get("revenue", 0)
    expenses = company_data.get("expenses", 0)
    profit = revenue - expenses

    growth_rate = company_data.get("growth_rate", "0")
    growth_rate = float(growth_rate.replace("%", "")) if isinstance(growth_rate, str) else 0

    industry = company_data.get("industry", "E-commerce")

    # -------------------------------
    # INDUSTRY-SPECIFIC CHANNELS
    # -------------------------------
    industry_channels = {
        "E-commerce": ["Paid Ads", "Referral", "Influencer", "Email"],
        "SaaS": ["SEO", "Content", "Referral", "Paid Ads"],
        "Manufacturing": ["Direct Sales", "Channel Partners", "Trade Shows", "Digital"],
        "EdTech": ["Influencer", "Paid Ads", "Referral", "Email"],
        "Retail": ["In-store Promotion", "Loyalty Program", "Paid Ads", "Social Media"]
    }

    channels = industry_channels.get(
        industry,
        ["Paid Ads", "Referral", "Email", "Other"]
    )

    # -------------------------------
    # CHANNEL CONTRIBUTION LOGIC
    # -------------------------------
    if profit < 0:
        # Loss situation → reduce paid channels
        contribution_pattern = [50, 25, 15, 10]
    elif growth_rate >= 15:
        # High growth → aggressive acquisition
        contribution_pattern = [30, 30, 25, 15]
    else:
        # Stable situation
        contribution_pattern = [35, 25, 20, 20]

    channel_contribution = {
        channel: contribution_pattern[i]
        for i, channel in enumerate(channels)
    }

    # -------------------------------
    # ROI CALCULATION (AUTO)
    # -------------------------------
    avg_margin = (profit / revenue) * 100 if revenue > 0 else -10

    roi = {}
    base_roi = 110 if profit < 0 else 160

    for idx, channel in enumerate(channels):
        roi[channel] = round(
            base_roi + avg_margin + (len(channels) - idx) * 12,
            1
        )

    # -------------------------------
    # TREND-BASED ADJUSTMENT
    # -------------------------------
    if not pl_df.empty:
        recent_trend = pl_df.tail(3)
        rev_growth = recent_trend["Revenue"].pct_change().mean()
        exp_growth = recent_trend["Expenses"].pct_change().mean()

        if exp_growth > rev_growth:
            insight = (
                "Expenses are growing faster than revenue. "
                "Marketing spend should shift towards high-ROI and organic channels."
            )
        else:
            insight = (
                "Revenue growth outpaces expenses. "
                "Marketing investment can be scaled cautiously."
            )
    else:
        insight = "Insufficient trend data for detailed marketing trend analysis."

    # -------------------------------
    # FINAL STRATEGIC SUMMARY
    # -------------------------------
    strategic_summary = {
        "situation": (
            "Loss-making business" if profit < 0
            else "High-growth business" if growth_rate >= 15
            else "Stable business"
        ),
        "recommendation": insight
    }

    return {
        "channels": channel_contribution,
        "roi": roi,
        "summary": strategic_summary
    }
