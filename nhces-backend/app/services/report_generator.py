"""
iNHCES PDF Cost Report Generator
Builds a professional PDF cost report using fpdf2.
Applies the iNHCES Warm Ivory design system
(Accent #8b6400, Text #1a1410, Surface #ffffff, Background #f5f1eb).

Returns: (pdf_bytes: bytes, page_count: int)
"""

import io
from datetime import date
from typing import Optional

from fpdf import FPDF


# ── Warm Ivory palette ─────────────────────────────────────────────────────────
NAVY    = (15,  40,  80)
ACCENT  = (139, 100,  0)   # #8b6400
WHITE   = (255, 255, 255)
IVORY   = (245, 241, 235)  # #f5f1eb
DGREY   = ( 60,  60,  60)  # #1a1410 approx
MGREY   = (120, 120, 120)
GREEN   = (  0, 122,  94)  # #007a5e
AMBER   = (184,  98,  10)  # #b8620a
RED_C   = (192,  57,  43)  # #c0392b

FRESHNESS_COLOURS = {
    "GREEN": GREEN,
    "AMBER": AMBER,
    "RED":   RED_C,
}

PAGE_W = 186   # usable width (210 - 12*2)
LEFT   = 12


def _sanitize(text: str) -> str:
    return (str(text)
            .replace("—", " - ").replace("–", "-")
            .replace("‘", "'").replace("’", "'")
            .replace("“", '"').replace("”", '"')
            .replace("₦", "NGN").replace("≤", "<=")
            .encode("latin-1", errors="replace").decode("latin-1"))


def _fmt_ngn(value: float) -> str:
    """Format as NGN with K/M/B suffix."""
    if value >= 1_000_000_000:
        return f"NGN {value/1_000_000_000:.2f}B"
    if value >= 1_000_000:
        return f"NGN {value/1_000_000:.2f}M"
    if value >= 1_000:
        return f"NGN {value/1_000:.0f}K"
    return f"NGN {value:,.0f}"


class ReportPDF(FPDF):
    def header(self):
        self.set_fill_color(*NAVY)
        self.rect(0, 0, 210, 14, "F")
        self.set_font("Helvetica", "B", 7)
        self.set_text_color(*WHITE)
        self.set_xy(5, 4)
        self.cell(PAGE_W, 6, _sanitize(
            "iNHCES Cost Report  |  TETFund NRF 2025  |  Dept. of Quantity Surveying, ABU Zaria"
        ))
        self.set_text_color(*DGREY)
        self.ln(16)

    def footer(self):
        self.set_y(-13)
        self.set_draw_color(*ACCENT)
        self.set_line_width(0.4)
        self.line(LEFT, self.get_y(), 198, self.get_y())
        self.set_font("Helvetica", "I", 7.5)
        self.set_text_color(*MGREY)
        self.cell(0, 8, _sanitize(
            f"iNHCES Intelligent National Housing Cost Estimating System  |  Page {self.page_no()}"
        ), align="C")

    def section_bar(self, title: str):
        self.ln(3)
        self.set_fill_color(*NAVY)
        self.set_text_color(*WHITE)
        self.set_font("Helvetica", "B", 9.5)
        self.set_x(LEFT)
        self.cell(PAGE_W, 7.5, _sanitize(f"  {title}"), fill=True, ln=True)
        self.set_text_color(*DGREY)
        self.ln(1.5)

    def kv_row(self, label: str, value: str, fill: bool = False):
        self.set_fill_color(*IVORY if fill else WHITE)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*ACCENT)
        self.set_x(LEFT)
        self.cell(55, 6.5, _sanitize(label), fill=True)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*DGREY)
        self.cell(PAGE_W - 55, 6.5, _sanitize(str(value)), fill=True, ln=True)

    def freshness_badge(self, level: str):
        colour = FRESHNESS_COLOURS.get(level, RED_C)
        labels = {"GREEN": "Live Data", "AMBER": "AI Template", "RED": "Synthetic -- Replace Before Publication"}
        self.set_fill_color(*colour)
        self.set_font("Helvetica", "B", 8.5)
        self.set_text_color(*WHITE)
        self.set_x(LEFT)
        self.cell(PAGE_W, 6, _sanitize(f"  DATA FRESHNESS: {level} -- {labels.get(level, '')}"),
                  fill=True, ln=True)
        self.set_text_color(*DGREY)
        self.ln(1)


def build_report_pdf(project: dict, prediction: dict) -> tuple:
    """
    Build a PDF cost report from project and prediction dicts.

    Args:
        project    : dict from Supabase projects table
        prediction : dict from Supabase predictions table

    Returns:
        (pdf_bytes: bytes, page_count: int)
    """
    pdf = ReportPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_margins(LEFT, 22, LEFT)

    # ── Page 1: Cover + Project Details ────────────────────────────────────────
    pdf.add_page()

    # Hero block
    pdf.set_fill_color(*NAVY)
    pdf.rect(0, 16, 210, 50, "F")
    pdf.set_xy(0, 24)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(*WHITE)
    pdf.cell(210, 10, "iNHCES Cost Estimation Report", align="C", ln=True)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(200, 215, 235)
    pdf.cell(210, 7, _sanitize(project.get("title", "Untitled Project")), align="C", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(180, 200, 225)
    pdf.cell(210, 6,
             _sanitize(f"{project.get('location_state','')} -- {project.get('location_zone','')}"),
             align="C", ln=True)
    pdf.set_draw_color(*ACCENT)
    pdf.set_line_width(0.8)
    pdf.line(30, 68, 180, 68)
    pdf.set_xy(LEFT, 76)
    pdf.set_text_color(*DGREY)

    pdf.section_bar("1. Project Information")
    for label, key, default in [
        ("Project Title",      "title",             "—"),
        ("Building Type",      "building_type",     "—"),
        ("Construction Type",  "construction_type", "—"),
        ("Floor Area",         "floor_area_sqm",    "—"),
        ("Number of Floors",   "num_floors",        "1"),
        ("Location State",     "location_state",    "—"),
        ("Geopolitical Zone",  "location_zone",     "—"),
        ("Report Date",        None,                date.today().strftime("%d %B %Y")),
    ]:
        val = (
            date.today().strftime("%d %B %Y") if key is None
            else f"{project.get(key, default)} sqm" if key == "floor_area_sqm"
            else str(project.get(key, default))
        )
        pdf.kv_row(label + ":", val, fill=False)

    # ── Page 2: Cost Estimate ───────────────────────────────────────────────────
    pdf.add_page()
    pdf.section_bar("2. Cost Estimate Summary")

    cost_per_sqm = float(prediction.get("predicted_cost_per_sqm", 0))
    total_cost   = float(prediction.get("total_predicted_cost_ngn", 0))
    conf_lower   = float(prediction.get("confidence_lower", 0))
    conf_upper   = float(prediction.get("confidence_upper", 0))
    mape         = float(prediction.get("mape_at_prediction", 13.66))
    floor_area   = float(project.get("floor_area_sqm", 0))

    # Primary cost box
    pdf.ln(2)
    pdf.set_fill_color(*IVORY)
    pdf.set_draw_color(*ACCENT)
    pdf.set_line_width(1.0)
    pdf.set_x(LEFT)
    pdf.rect(LEFT, pdf.get_y(), PAGE_W, 28, "FD")
    pdf.set_xy(LEFT + 4, pdf.get_y() + 4)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*MGREY)
    pdf.cell(PAGE_W - 8, 5, "PREDICTED COST PER SQM (NGN)")
    pdf.ln(5)
    pdf.set_x(LEFT + 4)
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(*ACCENT)
    pdf.cell(PAGE_W - 8, 11, _sanitize(f"NGN {cost_per_sqm:,.0f} / sqm"))
    pdf.ln(8)
    pdf.set_x(LEFT + 4)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*DGREY)
    pdf.cell(PAGE_W - 8, 5,
             _sanitize(f"90% Confidence: {_fmt_ngn(conf_lower)} -- {_fmt_ngn(conf_upper)} per sqm"))
    pdf.ln(12)
    pdf.set_text_color(*DGREY)

    # Total cost box
    pdf.set_fill_color(*NAVY)
    pdf.set_x(LEFT)
    pdf.rect(LEFT, pdf.get_y(), PAGE_W, 16, "F")
    pdf.set_xy(LEFT + 4, pdf.get_y() + 4)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*MGREY)
    pdf.cell(80, 5, "TOTAL ESTIMATED COST")
    pdf.set_x(LEFT + 4 + 80)
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(*WHITE)
    pdf.cell(PAGE_W - 90, 5, _sanitize(_fmt_ngn(total_cost)))
    pdf.ln(18)
    pdf.set_text_color(*DGREY)

    # Detailed rows
    pdf.kv_row("Cost per sqm:",      f"NGN {cost_per_sqm:,.0f}",   fill=False)
    pdf.kv_row("Floor Area:",        f"{floor_area:,.1f} sqm",      fill=True)
    pdf.kv_row("Total Estimate:",    _fmt_ngn(total_cost),          fill=False)
    pdf.kv_row("Lower Bound (90%):", _fmt_ngn(conf_lower),          fill=True)
    pdf.kv_row("Upper Bound (90%):", _fmt_ngn(conf_upper),          fill=False)
    pdf.kv_row("Model MAPE:",        f"{mape:.2f}%",                fill=True)
    pdf.kv_row("Model Name:",        prediction.get("model_version", "LightGBM"), fill=False)

    # Freshness badge
    freshness = prediction.get("data_freshness", "RED")
    pdf.ln(3)
    pdf.freshness_badge(freshness)

    # ── Page 3: Feature Importance ──────────────────────────────────────────────
    pdf.add_page()
    pdf.section_bar("3. Feature Importance (SHAP Analysis)")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 5.2, _sanitize(
        "The chart below shows the top macroeconomic factors driving this cost estimate. "
        "SHAP (SHapley Additive exPlanations) values quantify each feature's contribution "
        "to the predicted cost per sqm relative to the model baseline. "
        "Positive values increase the estimate; negative values decrease it."
    ))
    pdf.ln(2)

    shap_vals = prediction.get("shap_values", {})
    if shap_vals:
        # Simple horizontal bar chart using filled rectangles
        items = sorted(
            [(k, v) for k, v in shap_vals.items() if isinstance(v, (int, float))],
            key=lambda x: abs(x[1]), reverse=True
        )[:7]

        feature_labels = {
            "ret_ngn_usd":             "NGN/USD Return (%)",
            "d_cpi_annual_pct":        "CPI Inflation (change)",
            "ret_ngn_eur":             "NGN/EUR Return (%)",
            "d_brent_usd_barrel":      "Brent Crude (change)",
            "ret_ngn_gbp":             "NGN/GBP Return (%)",
            "d_gdp_growth_pct":        "GDP Growth (change)",
            "d_lending_rate_pct":      "Lending Rate (change)",
            "lag1_ret_ngn_usd":        "NGN/USD Return (lag-1)",
            "lag1_d_cpi_annual_pct":   "CPI Inflation (lag-1)",
            "lag1_d_brent_usd_barrel": "Brent Crude (lag-1)",
        }

        if items:
            max_abs = max(abs(v) for _, v in items) or 1
            bar_max_w = 90  # max bar width in mm

            # Header
            pdf.set_fill_color(*NAVY)
            pdf.set_text_color(*WHITE)
            pdf.set_font("Helvetica", "B", 8)
            pdf.set_x(LEFT)
            pdf.cell(65, 6, " Feature", fill=True)
            pdf.cell(bar_max_w + 10, 6, " SHAP Contribution (NGN/sqm)", fill=True)
            pdf.cell(PAGE_W - 65 - bar_max_w - 10, 6, " Value", fill=True, ln=True)
            pdf.set_text_color(*DGREY)

            for i, (feat, val) in enumerate(items):
                label = feature_labels.get(feat, feat)
                bar_w = abs(val) / max_abs * bar_max_w
                fill_bg = IVORY if i % 2 == 0 else WHITE

                pdf.set_fill_color(*fill_bg)
                pdf.set_font("Helvetica", "", 8.5)
                pdf.set_x(LEFT)
                pdf.cell(65, 6.5, _sanitize(f" {label}"), fill=True)

                # Bar
                bar_col = GREEN if val > 0 else RED_C
                pdf.set_fill_color(*fill_bg)
                pdf.cell(bar_max_w + 10, 6.5, "", fill=True)
                # Draw actual bar over it
                bar_x = LEFT + 65 + 2
                bar_y = pdf.get_y() - 6.5 + 1
                pdf.set_fill_color(*bar_col)
                if bar_w > 0.5:
                    pdf.rect(bar_x, bar_y, bar_w, 4.5, "F")

                pdf.set_fill_color(*fill_bg)
                pdf.set_font("Helvetica", "B", 8.5)
                pdf.set_text_color(*(GREEN if val > 0 else RED_C))
                pdf.cell(PAGE_W - 65 - bar_max_w - 10, 6.5,
                         _sanitize(f" {val:+,.0f}"), fill=True, ln=True)
                pdf.set_text_color(*DGREY)
        else:
            pdf.set_font("Helvetica", "I", 9)
            pdf.set_x(LEFT)
            pdf.cell(PAGE_W, 6, "No SHAP data available for this prediction.")
            pdf.ln(8)
    else:
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_x(LEFT)
        pdf.cell(PAGE_W, 6, "SHAP values not available (synthetic fallback model).")
        pdf.ln(8)

    # ── Page 4: Disclaimer ──────────────────────────────────────────────────────
    pdf.add_page()
    pdf.section_bar("4. Important Notices and Limitations")

    notices = [
        ("Data Source Status",
         f"This estimate uses data at freshness level: {freshness}. "
         "GREEN = live API data. AMBER = AI-generated template. "
         "RED = synthetic data -- must be replaced with real NIQS unit rate data "
         "before this estimate is used for any procurement, grant report, or publication."),
        ("Model Accuracy",
         f"The champion model (LightGBM) has a Leave-One-Out cross-validated MAPE "
         f"of {mape:.2f}% on the training dataset. This means the estimate may be "
         f"approximately {mape:.0f}% above or below the actual construction cost. "
         "Always obtain independent quantity surveying advice before committing to a budget."),
        ("Scope of Estimate",
         "This estimate covers construction cost per square metre of gross floor area. "
         "It does not include: land cost, professional fees, statutory charges, "
         "external works, furniture and fittings, or contingencies."),
        ("AI Disclosure",
         "This report was generated by the iNHCES ML system, an AI-assisted research "
         "tool (TETFund NRF 2025, ABU Zaria). It is not a certified quantity surveying "
         "valuation. Human QS verification is required before any formal use."),
        ("Data Replacement Obligation",
         "If this report shows RED data level, the underlying macroeconomic or material "
         "price data is synthetic (simulated). It must be replaced with real data from "
         "CBN, EIA, NIQS, or verified sources before this estimate is published, "
         "submitted to a grant body, or used in any official capacity."),
    ]

    for i, (title, body_text) in enumerate(notices):
        pdf.set_fill_color(*IVORY if i % 2 == 0 else WHITE)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*ACCENT)
        pdf.set_x(LEFT)
        pdf.cell(PAGE_W, 6.5, _sanitize(f"  {title}"), fill=True, ln=True)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*DGREY)
        pdf.set_x(LEFT)
        pdf.set_fill_color(*IVORY if i % 2 == 0 else WHITE)
        pdf.multi_cell(PAGE_W, 5.2, _sanitize(f"  {body_text}"), fill=True)
        pdf.ln(1)

    # Footer signature block
    pdf.ln(4)
    pdf.set_draw_color(*ACCENT)
    pdf.set_line_width(0.5)
    pdf.line(LEFT, pdf.get_y(), LEFT + PAGE_W, pdf.get_y())
    pdf.ln(3)
    pdf.set_font("Helvetica", "I", 8.5)
    pdf.set_text_color(*MGREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 5, _sanitize(
        f"Generated by iNHCES on {date.today().strftime('%d %B %Y')} | "
        "TETFund National Research Fund 2025 | "
        "Department of Quantity Surveying, Ahmadu Bello University Zaria | "
        "This document is AI-assisted. Verify all figures independently."
    ))

    # Render to bytes
    buf = io.BytesIO()
    pdf_bytes = pdf.output()
    if isinstance(pdf_bytes, bytearray):
        pdf_bytes = bytes(pdf_bytes)

    return pdf_bytes, pdf.page
