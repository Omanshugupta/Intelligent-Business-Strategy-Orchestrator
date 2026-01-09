from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
import os
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import pandas as pd
import io

def generate_report(company, ai, pl_df=None, financial_metrics=None):
    path = "reports/Executive_Business_Report.pdf"

    doc = SimpleDocTemplate(
        path,
        pagesize=A4,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch
    )

    styles = getSampleStyleSheet()
    
    # Helper function to safely add styles (handle existing styles gracefully)
    def add_style_safe(style_name, style_obj):
        try:
            styles.add(style_obj)
        except KeyError:
            # Style already exists, update it instead
            styles.byName[style_name] = style_obj
    
    # Title Style
    add_style_safe("CoverTitle", ParagraphStyle(
        name="CoverTitle",
        parent=styles["Title"],
        fontSize=28,
        textColor=colors.HexColor("#1e3a8a"),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName="Helvetica-Bold"
    ))
    
    # Subtitle Style
    add_style_safe("CoverSubtitle", ParagraphStyle(
        name="CoverSubtitle",
        fontSize=14,
        textColor=colors.HexColor("#64748b"),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName="Helvetica"
    ))
    
    # Section Header Style
    add_style_safe("SectionHeader", ParagraphStyle(
        name="SectionHeader",
        fontSize=18,
        spaceAfter=12,
        spaceBefore=24,
        textColor=colors.HexColor("#1e40af"),
        fontName="Helvetica-Bold",
        leading=22
    ))
    
    # Subsection Header Style
    add_style_safe("SubsectionHeader", ParagraphStyle(
        name="SubsectionHeader",
        fontSize=14,
        spaceAfter=8,
        spaceBefore=16,
        textColor=colors.HexColor("#3b82f6"),
        fontName="Helvetica-Bold",
        leading=18
    ))
    
    # Body Text Style (use custom name to avoid conflict with default)
    add_style_safe("BodyTextCustom", ParagraphStyle(
        name="BodyTextCustom",
        fontSize=11,
        leading=16,
        spaceAfter=12,
        alignment=TA_JUSTIFY,
        fontName="Helvetica",
        textColor=colors.HexColor("#1f2937")
    ))
    
    # Bullet Point Style
    add_style_safe("BulletPoint", ParagraphStyle(
        name="BulletPoint",
        fontSize=11,
        leading=16,
        spaceAfter=8,
        leftIndent=20,
        bulletIndent=10,
        alignment=TA_LEFT,
        fontName="Helvetica",
        textColor=colors.HexColor("#374151")
    ))

    content = []

    # Cover Page
    content.append(Spacer(1, 2.5 * inch))
    content.append(Paragraph("Intelligent Business Strategy Orchestrator", styles["CoverTitle"]))
    content.append(Spacer(1, 0.3 * inch))
    content.append(Paragraph("AI-Driven Executive Decision System", styles["CoverSubtitle"]))
    content.append(Spacer(1, 0.5 * inch))
    content.append(Paragraph("Executive Business Report", styles["CoverSubtitle"]))
    content.append(Spacer(1, 3 * inch))
    content.append(PageBreak())

    # Executive Summary
    content.append(Paragraph("Executive Summary", styles["SectionHeader"]))
    summary_lines = [line.strip() for line in ai["final_decision"].split(".") if line.strip()][:5]
    for line in summary_lines:
        if line:
            # Remove markdown asterisks and clean text
            clean_line = line.replace("**", "").replace("*", "").strip()
            if clean_line:
                content.append(Paragraph(f"• {clean_line}", styles["BulletPoint"]))
    content.append(Spacer(1, 0.3 * inch))
    content.append(PageBreak())

    # Business Snapshot
    content.append(Paragraph("Business Snapshot", styles["SectionHeader"]))
    
    # Format table data
    profit_loss = company['revenue'] - company['expenses']
    table_data = [
        ["Metric", "Value"],
        ["Revenue", f"₹ {company['revenue']:,}"],
        ["Expenses", f"₹ {company['expenses']:,}"],
        ["Profit / Loss", f"₹ {profit_loss:,}"],
        ["Team Size", str(company.get("team_size", "N/A"))]
    ]
    
    table = Table(table_data, colWidths=[2.5 * inch, 3.5 * inch])
    table.setStyle(TableStyle([
        # Header row
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e40af")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 12),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ("TOPPADDING", (0, 0), (-1, 0), 12),
        # Data rows
        ("BACKGROUND", (0, 1), (-1, -1), colors.white),
        ("TEXTCOLOR", (0, 1), (-1, -1), colors.HexColor("#1f2937")),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 11),
        ("GRID", (0, 0), (-1, -1), 1, colors.HexColor("#e5e7eb")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f9fafb")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 1), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 10),
    ]))
    content.append(Spacer(1, 0.2 * inch))
    content.append(table)
    content.append(Spacer(1, 0.3 * inch))
    
    # Add charts if data is available
    if pl_df is not None and not pl_df.empty and "Month" in pl_df.columns:
        try:
            # Chart 1: Revenue vs Expenses Trend
            fig, ax = plt.subplots(figsize=(6, 3.5))
            ax.plot(pl_df["Month"], pl_df["Revenue"], marker='o', linewidth=2, label="Revenue", color='#2563eb')
            ax.plot(pl_df["Month"], pl_df["Expenses"], marker='s', linewidth=2, label="Expenses", color='#dc2626')
            ax.set_xlabel("Month", fontsize=10, fontweight='bold')
            ax.set_ylabel("Amount (₹)", fontsize=10, fontweight='bold')
            ax.set_title("Revenue vs Expenses Trend", fontsize=12, fontweight='bold', pad=15)
            ax.legend(loc='best', frameon=True, fancybox=True, shadow=True)
            ax.grid(True, alpha=0.3, linestyle='--')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            plt.tight_layout()
            
            # Save to buffer
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
            img_buffer.seek(0)
            plt.close()
            
            # Add to PDF
            chart_img = Image(img_buffer, width=5.5*inch, height=3.2*inch)
            content.append(Spacer(1, 0.2 * inch))
            content.append(chart_img)
        except Exception as e:
            pass  # Skip chart if there's an error
    
    content.append(Spacer(1, 0.3 * inch))
    content.append(PageBreak())

    # Financial Analysis
    content.append(Paragraph("Financial Analysis & Risk Assessment", styles["SectionHeader"]))
    # Split long text into paragraphs
    finance_paragraphs = [p.strip() for p in ai["finance_output"].split(". ") if p.strip()]
    for para in finance_paragraphs:
        if para:
            # Remove markdown asterisks and clean text
            clean_para = para.replace("**", "").replace("*", "").strip()
            if clean_para:
                content.append(Paragraph(clean_para + ".", styles["BodyTextCustom"]))
    
    # Add financial metrics chart if available
    if financial_metrics is not None:
        try:
            # Chart 2: Financial Metrics Comparison
            fig, ax = plt.subplots(figsize=(6, 3.5))
            metrics_names = ["Revenue", "Expenses", "Profit"]
            metrics_values = [
                company.get('revenue', 0),
                company.get('expenses', 0),
                company.get('revenue', 0) - company.get('expenses', 0)
            ]
            colors_list = ['#2563eb', '#dc2626', '#16a34a']
            bars = ax.bar(metrics_names, metrics_values, color=colors_list, alpha=0.8, edgecolor='black', linewidth=1.5)
            
            # Add value labels on bars
            for bar, value in zip(bars, metrics_values):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'₹{value:,.0f}',
                       ha='center', va='bottom' if height >= 0 else 'top',
                       fontsize=9, fontweight='bold')
            
            ax.set_ylabel("Amount (₹)", fontsize=10, fontweight='bold')
            ax.set_title("Financial Metrics Overview", fontsize=12, fontweight='bold', pad=15)
            ax.grid(True, alpha=0.3, axis='y', linestyle='--')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            plt.tight_layout()
            
            # Save to buffer
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
            img_buffer.seek(0)
            plt.close()
            
            # Add to PDF
            chart_img = Image(img_buffer, width=5.5*inch, height=3.2*inch)
            content.append(Spacer(1, 0.2 * inch))
            content.append(chart_img)
        except Exception as e:
            pass  # Skip chart if there's an error
    
    content.append(Spacer(1, 0.3 * inch))
    content.append(PageBreak())

    # Strategy Analysis
    content.append(Paragraph("Strategy Analysis", styles["SectionHeader"]))
    strategy_paragraphs = [p.strip() for p in ai["strategy_output"].split(". ") if p.strip()]
    for para in strategy_paragraphs:
        if para:
            # Remove markdown asterisks and clean text
            clean_para = para.replace("**", "").replace("*", "").strip()
            if clean_para:
                content.append(Paragraph(clean_para + ".", styles["BodyTextCustom"]))
    content.append(Spacer(1, 0.3 * inch))
    content.append(PageBreak())

    # Marketing Analysis
    content.append(Paragraph("Marketing Analysis", styles["SectionHeader"]))
    marketing_paragraphs = [p.strip() for p in ai["marketing_output"].split(". ") if p.strip()]
    for para in marketing_paragraphs:
        if para:
            # Remove markdown asterisks and clean text
            clean_para = para.replace("**", "").replace("*", "").strip()
            if clean_para:
                content.append(Paragraph(clean_para + ".", styles["BodyTextCustom"]))
    content.append(Spacer(1, 0.3 * inch))
    content.append(PageBreak())

    # Executive Direction
    content.append(Paragraph("Executive Direction & Strategic Priorities", styles["SectionHeader"]))
    ceo_paragraphs = [p.strip() for p in ai["final_decision"].split(". ") if p.strip()]
    for para in ceo_paragraphs:
        if para:
            # Remove markdown asterisks and clean text
            clean_para = para.replace("**", "").replace("*", "").strip()
            if clean_para:
                content.append(Paragraph(clean_para + ".", styles["BodyTextCustom"]))
    content.append(Spacer(1, 0.3 * inch))

    doc.build(content)
    return path
