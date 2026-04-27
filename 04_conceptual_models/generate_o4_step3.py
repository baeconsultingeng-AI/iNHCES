"""
iNHCES O4 Step 3 — Data Flow Diagrams Document Generator
Deliverable: O4_03_Data_Flow_Diagrams.pdf
DATA SOURCE: AMBER — AI-authored diagrams derived from O3 SRS, O4 Step 1
             architecture, and O4 Step 2 database schema.

TETFund NRF 2025 | Department of Quantity Surveying, ABU Zaria
"""

import sys
import os
from datetime import date

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, os.path.join(_ROOT, '01_literature_review'))

from generate_o1_pdfs import (
    DocPDF, sanitize, _ds_page,
    DARK_NAVY, GOLD, LIGHT_BLUE, WHITE, DARK_GREY, MID_GREY,
    PAGE_W, LEFT, LINE_H,
)

OUT_DIR   = _HERE
DOC_ID    = "O4-03"
DOC_TITLE = "iNHCES Data Flow Diagrams"
DOC_SUBTITLE = "DFD Level 0, DFD Level 1, User Journey Map, Pipeline Flow"


class DfdPDF(DocPDF):
    def __init__(self):
        super().__init__(DOC_TITLE, DOC_ID)

    def header(self):
        self.set_fill_color(*DARK_NAVY)
        self.rect(0, 0, 210, 14, 'F')
        self.set_font("Helvetica", "B", 7)
        self.set_text_color(*WHITE)
        self.set_xy(5, 4)
        self.cell(PAGE_W, 6, sanitize(
            "iNHCES  |  TETFund NRF 2025  |  Dept. Quantity Surveying, ABU Zaria"
            "  |  O4 Step 3 — Data Flow Diagrams"
        ))
        self.set_text_color(*DARK_GREY)
        self.ln(16)

    def footer(self):
        self.set_y(-13)
        self.set_draw_color(*GOLD)
        self.set_line_width(0.4)
        self.line(LEFT, self.get_y(), 198, self.get_y())
        self.set_font("Helvetica", "I", 7.5)
        self.set_text_color(*MID_GREY)
        self.cell(0, 8, sanitize(
            f"{DOC_TITLE}  |  ABU Zaria / TETFund NRF 2025  |  Page {self.page_no()}"
        ), align="C")

    def h1(self, text):
        self.ln(3)
        self.set_fill_color(*DARK_NAVY)
        self.set_text_color(*WHITE)
        self.set_font("Helvetica", "B", 10)
        self.set_x(LEFT)
        self.cell(PAGE_W, 8, sanitize(f"  {text}"), fill=True, ln=True)
        self.set_text_color(*DARK_GREY)
        self.ln(2)

    def h2(self, text):
        self.ln(2)
        self.set_font("Helvetica", "B", 9.5)
        self.set_text_color(*DARK_NAVY)
        self.set_x(LEFT)
        self.multi_cell(PAGE_W, 5.5, sanitize(text))
        self.set_text_color(*DARK_GREY)
        self.ln(1)

    def h3(self, text):
        self.ln(1)
        self.set_font("Helvetica", "BI", 9)
        self.set_text_color(*DARK_GREY)
        self.set_x(LEFT)
        self.multi_cell(PAGE_W, 5.2, sanitize(text))
        self.ln(0.5)

    def para(self, text, indent=0):
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(*DARK_GREY)
        self.set_x(LEFT + indent)
        self.multi_cell(PAGE_W - indent, 5.2, sanitize(text))
        self.ln(1.5)

    def bullet(self, items, indent=4):
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(*DARK_GREY)
        for item in items:
            self.set_x(LEFT + indent)
            self.cell(4, 5.2, "-")
            self.set_x(LEFT + indent + 4)
            self.multi_cell(PAGE_W - indent - 4, 5.2, sanitize(item))
        self.ln(1)

    def diagram_ref_box(self, filename, diagram_type, description):
        self.ln(2)
        self.set_fill_color(*LIGHT_BLUE)
        self.set_draw_color(*DARK_NAVY)
        self.set_line_width(0.5)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*DARK_NAVY)
        self.set_x(LEFT)
        self.cell(PAGE_W, 6.5, sanitize(f"  DIAGRAM FILE:  {filename}  [{diagram_type}]"),
                  border="LTR", fill=True, ln=True)
        self.set_font("Helvetica", "", 9)
        self.set_fill_color(240, 245, 255)
        self.set_text_color(*DARK_GREY)
        self.set_x(LEFT)
        self.multi_cell(PAGE_W, 5, sanitize(
            f"  {description}\n"
            "  Render: paste into mermaid.live  OR  open in VS Code with "
            "Mermaid Preview extension installed."
        ), border="LBR", fill=True)
        self.set_text_color(*DARK_GREY)
        self.ln(2)

    def flow_table(self, title, rows, widths):
        self.h3(title)
        self.thead([h for h, _ in zip(
            ["Flow", "From", "To", "Data / Description"],
            widths
        )], widths)
        for i, row in enumerate(rows):
            self.mrow(row, widths, fill=(i % 2 == 1))
        self.ln(1)


# ── Cover ──────────────────────────────────────────────────────────────────────
def make_cover(pdf):
    pdf.add_page()
    pdf.set_fill_color(*DARK_NAVY)
    pdf.rect(0, 18, 210, 55, 'F')
    pdf.set_xy(0, 26)
    pdf.set_font("Helvetica", "B", 15)
    pdf.set_text_color(*WHITE)
    pdf.cell(210, 9, sanitize(DOC_TITLE), align="C", ln=True)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(200, 215, 235)
    pdf.cell(210, 7, sanitize(DOC_SUBTITLE), align="C", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*LIGHT_BLUE)
    pdf.cell(210, 6, "Intelligent National Housing Cost Estimating System (iNHCES)", align="C", ln=True)
    pdf.cell(210, 6, "TETFund NRF 2025  |  Department of Quantity Surveying, ABU Zaria", align="C", ln=True)
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(0.8)
    pdf.line(30, 76, 180, 76)
    pdf.set_xy(LEFT, 84)
    meta = [
        ("Objective:",   "O4 — Develop Conceptual Models for the iNHCES System"),
        ("Step:",        "3 — Data Flow Diagrams (DFDs), User Journey, Pipeline Flow"),
        ("Document ID:", DOC_ID),
        ("Version:",     "1.0 — Initial AI-Assisted Draft"),
        ("Date:",        date.today().strftime("%d %B %Y")),
        ("Grant:",       "TETFund National Research Fund (NRF) 2025"),
        ("Diagrams:",    "04_DFD_Level0.mmd  |  04_DFD_Level1.mmd  |  "
                         "04_User_Journey.mmd  |  04_Pipeline_Flow.mmd"),
        ("Next Step:",   "O4 Step 4 — Chapter 4 Conceptual Models Write-up"),
    ]
    for label, val in meta:
        pdf.set_x(LEFT)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*DARK_NAVY)
        pdf.cell(40, 6.5, sanitize(label))
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*DARK_GREY)
        pdf.cell(PAGE_W - 40, 6.5, sanitize(val), ln=True)


# ── Section 1: Overview ────────────────────────────────────────────────────────
def section1(pdf):
    pdf.add_page()
    pdf.h1("1. Diagrams Overview")
    pdf.para(
        "This document describes four Mermaid-format diagrams that together provide "
        "a complete behavioural model of the iNHCES system. The diagrams are stored "
        "as `.mmd` files in `04_conceptual_models/` and should be rendered using "
        "mermaid.live or the VS Code Mermaid Preview extension. They complement "
        "the structural models in O4 Steps 1 and 2 (architecture and schema)."
    )
    ow = [45, 35, PAGE_W - 80]
    pdf.thead(["Diagram", "Type", "Purpose"], ow)
    diag_rows = [
        ("04_DFD_Level0.mmd",    "DFD Level 0\n(Context Diagram)",
         "Shows iNHCES as a single system with all 8 external entities "
         "and their data flows in and out."),
        ("04_DFD_Level1.mmd",    "DFD Level 1\n(Process Decomposition)",
         "Explodes the system into 6 processes, 3 data stores, and "
         "all inter-process and entity-to-process data flows."),
        ("04_User_Journey.mmd",  "User Journey Map",
         "Satisfaction-scored journey for QS Professional (5 stages, "
         "21 touchpoints) and Researcher/PI (4 stages, 9 touchpoints)."),
        ("04_Pipeline_Flow.mmd", "Pipeline Flow\n(Airflow DAGs)",
         "Shows all 9 Airflow DAGs, their cron schedules, external "
         "sources, database targets, and ML retrain + drift detection flows."),
    ]
    for i, row in enumerate(diag_rows):
        pdf.mrow(list(row), ow, fill=(i % 2 == 1))
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 1: O4 Step 3 diagram inventory. All diagrams are in Mermaid format."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)

    pdf.h2("1.1 How to Render the Diagrams")
    pdf.bullet([
        "Online: Copy the .mmd file contents and paste into mermaid.live. "
        "Export as SVG or PNG for inclusion in reports and papers.",
        "VS Code: Install the 'Mermaid Preview' extension (ID: bierner.markdown-mermaid "
        "or similar). Open any .mmd file -> right-click -> 'Open Preview'.",
        "GitHub: Mermaid diagrams embedded in .md files render automatically "
        "in GitHub README and wiki pages. Wrap in ```mermaid ... ``` code fences.",
        "For Paper P4 and P7: Export as high-resolution PNG (>300 dpi) from "
        "mermaid.live for inclusion in journal figures. Ensure font size is "
        "legible at A4 column width (~86mm for two-column journals).",
    ])


# ── Section 2: DFD Level 0 ────────────────────────────────────────────────────
def section2(pdf):
    pdf.add_page()
    pdf.h1("2. DFD Level 0 — Context Diagram")
    pdf.diagram_ref_box(
        "04_DFD_Level0.mmd",
        "DFD Level 0 — Context Diagram (Mermaid graph TD)",
        "Shows iNHCES as a single process (Process 0) with 9 external entities "
        "and all inbound and outbound data flows."
    )

    pdf.h2("2.1 Description")
    pdf.para(
        "The Level 0 DFD (context diagram) presents the highest-level view of "
        "the iNHCES system. The entire system is represented as a single process "
        "bubble (Process 0: iNHCES). All entities outside the system boundary "
        "are shown as rectangles with directed arrows representing data flows. "
        "This diagram defines the system boundary and documents every external "
        "interface that the O6 implementation team must build."
    )

    pdf.h2("2.2 External Entities")
    ew = [38, PAGE_W - 38]
    pdf.thead(["External Entity", "Role and Data Flows"], ew)
    entities = [
        ("QS Professional",
         "PRIMARY USER. Sends project details (building type, floor area, location, "
         "construction type). Receives cost estimate (NGN/sqm), confidence interval, "
         "SHAP explanation, and PDF report."),
        ("Researcher / PI",
         "SECONDARY USER. Sends analysis queries, data export requests, "
         "model performance review requests. Receives aggregated project data, "
         "macro data series, and model metrics."),
        ("System Admin",
         "OPERATIONS. Sends user management commands, model promotion decisions, "
         "manual pipeline triggers, and NIQS CSV uploads. Receives system status, "
         "pipeline health, audit log, and user list."),
        ("World Bank Open Data API",
         "DATA SOURCE. Sends GDP growth %, CPI inflation %, lending rate % "
         "(annual frequency). No authentication required."),
        ("EIA API (Brent Crude)",
         "DATA SOURCE. Sends Brent crude oil price (USD/barrel). "
         "Requires EIA_API_KEY. Currently synthetic (RED) until key configured."),
        ("FRED / CBN API",
         "DATA SOURCE. Sends NGN/USD, NGN/EUR, NGN/GBP exchange rates (daily). "
         "Requires FRED_API_KEY. Currently synthetic (RED)."),
        ("PropertyPro + Private Property",
         "DATA SOURCE. Sends property listing prices (NGN/sqm by zone and type) "
         "via web scraper. Weekly frequency."),
        ("BusinessDay + Jiji.ng",
         "DATA SOURCE. Sends cement prices (NGN per 50kg by brand/region) and "
         "iron rod prices (NGN/tonne by diameter/region) via scrapers. Weekly."),
        ("NNPC / NMDPRA",
         "DATA SOURCE. Sends PMS (petrol) pump prices by state. Monthly. "
         "HTTP API or web scraper."),
        ("NIQS",
         "DATA SOURCE. Sends quarterly unit rates via manual CSV upload "
         "by System Admin through the admin dashboard."),
        ("GitHub",
         "CI/CD. Receives code deployments (push to main). "
         "Returns build and deployment status via GitHub Actions."),
    ]
    for i, (ent, desc) in enumerate(entities):
        pdf.mrow([ent, desc], ew, fill=(i % 2 == 1))
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 2: DFD Level 0 external entities and data flows."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)


# ── Section 3: DFD Level 1 ────────────────────────────────────────────────────
def section3(pdf):
    pdf.add_page()
    pdf.h1("3. DFD Level 1 — System Process Decomposition")
    pdf.diagram_ref_box(
        "04_DFD_Level1.mmd",
        "DFD Level 1 — Process Decomposition (Mermaid graph TD)",
        "Decomposes the iNHCES system into 6 processes and 3 data stores, "
        "with all inter-process and entity-to-process data flows."
    )

    pdf.h2("3.1 Processes")
    pw = [28, 38, PAGE_W - 66]
    pdf.thead(["Process", "Name", "Description"], pw)
    processes = [
        ("1.0", "User Authentication",
         "Validates credentials via Supabase Auth (GoTrue). Issues JWT tokens "
         "with role claims. Logs login events to audit_log."),
        ("2.0", "Cost Estimation\n(ML Inference)",
         "Receives project parameters from QS Professional. Reads latest macro "
         "and material features from D1 (Supabase). Loads champion model from D2 (R2). "
         "Runs inference, stores prediction record, returns cost estimate + SHAP values."),
        ("3.0", "Data Ingestion\nPipeline",
         "Airflow DAGs orchestrate collection from all external data sources. "
         "Validates, cleans, and inserts records into appropriate Supabase tables. "
         "Handles synthetic fallback when live API keys are absent."),
        ("4.0", "ML Model Management\n(Train + Promote)",
         "Weekly retrain: assembles feature matrix from D1, trains all model family, "
         "logs to D3 (MLflow), compares challenger vs. champion MAPE, auto-promotes "
         "if improvement >= 0.5%. Admin can manually promote via dashboard."),
        ("5.0", "Report Generation",
         "Compiles project + prediction + SHAP data into a PDF (fpdf2). "
         "Uploads to D2 (Cloudflare R2). Stores report record in D1. "
         "Returns presigned download URL (24-hour expiry) to user."),
        ("6.0", "Pipeline Monitoring\n(Drift + Health)",
         "Daily drift detection: computes PSI per feature vs. training baseline. "
         "If PSI > 0.2, triggers emergency retrain via Process 4.0. "
         "Provides DAG health status to Admin and Researcher on demand."),
    ]
    for i, row in enumerate(processes):
        pdf.mrow(list(row), pw, fill=(i % 2 == 1))
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 3: DFD Level 1 processes. FastAPI implements P1-P2 and P5-P6. "
        "Airflow implements P3 and triggers P4."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)

    pdf.h2("3.2 Data Stores")
    pdf.bullet([
        "D1 — Supabase PostgreSQL: The primary persistent store for all application "
        "data. Accessed by all six processes. 16 tables as defined in O4 Step 2. "
        "Processes read and write via Supabase Python client (service_role key).",
        "D2 — Cloudflare R2: Object storage for binary artefacts. Receives PDF "
        "reports from P5 and model .pkl files from P4. Serves champion model "
        "to P2 on /estimate startup. S3-compatible; accessed via boto3.",
        "D3 — MLflow Registry: Experiment and model tracking store. Receives "
        "training run data from P4 (metrics, params, feature importance). "
        "Provides model metadata to P2 (/estimate) and P5 (report). "
        "Self-hosted on Railway.",
    ])

    pdf.h2("3.3 Key Inter-Process Flows")
    pdf.bullet([
        "P3 -> P4 (data availability trigger): When P3 successfully loads a "
        "new batch of data, it signals P4 via the nhces_retrain_weekly DAG "
        "schedule. An emergency retrain can also be triggered by P6.",
        "P6 -> P4 (drift alert): When P6 detects PSI > 0.2 for any key feature, "
        "it triggers an emergency retrain task within the nhces_drift_monitor DAG, "
        "which calls the same feature assembly and training pipeline as P4.",
        "P2 -> D2 (model loading): The champion model .pkl is loaded from "
        "Cloudflare R2 into FastAPI memory at startup and cached. It is refreshed "
        "when P4 promotes a new champion (via a background task or rolling restart).",
        "P1 -> P2, P5 (JWT propagation): All requests to P2 and P5 carry "
        "a validated JWT. The user_id extracted from the JWT is stored in "
        "every prediction and report record for RLS enforcement.",
    ])


# ── Section 4: User Journey Map ────────────────────────────────────────────────
def section4(pdf):
    pdf.add_page()
    pdf.h1("4. User Journey Map")
    pdf.diagram_ref_box(
        "04_User_Journey.mmd",
        "User Journey Map (Mermaid journey diagram)",
        "Satisfaction-scored journey for QS Professional (primary persona, 5 stages, "
        "21 touchpoints) and Researcher/PI (secondary persona, 4 stages, 9 touchpoints). "
        "Scale: 1 (very poor) to 5 (excellent)."
    )

    pdf.h2("4.1 QS Professional — Primary Persona")
    pdf.para(
        "The QS Professional is the primary user of iNHCES. Their core task is "
        "to obtain a reliable, explainable cost estimate per square metre for a "
        "Nigerian housing construction project, and to generate a professional "
        "PDF report for client or BQ documentation purposes. The journey has "
        "five stages with 21 touchpoints."
    )
    jw = [30, 12, PAGE_W - 42]
    pdf.thead(["Stage", "Score", "Key Touchpoints and Pain Points"], jw)
    qs_stages = [
        ("1. Discovery\n& Onboarding",   "3-4",
         "Awareness via NIQS or ABU Zaria network (score 3 — awareness gap is a risk). "
         "Registration and email verification (score 3-4 — standard friction). "
         "Login with JWT (score 5 — instant, no extra steps once registered)."),
        ("2. Project Setup",              "4-5",
         "All touchpoints score 5. The form is intuitive. "
         "Pain point: requiring zone selection (6 geopolitical zones) may confuse "
         "users unfamiliar with the classification — provide a map or dropdown hint."),
        ("3. Cost Estimation",            "3-5",
         "Prediction and SHAP results score 5 — this is the core value. "
         "Data freshness warning (score 3) is a pain point: if EIA or FRED keys "
         "are not configured, RED-level warnings may reduce user confidence. "
         "Fix: configure API keys before public launch."),
        ("4. Report Generation",          "4-5",
         "Report generation and download score 5. "
         "Presigned URL expiry (24hrs) scores 4 — user must download promptly. "
         "Consider a permanent report history page with re-download option."),
        ("5. Ongoing Use",                "2-5",
         "Return visits score 5. Data freshness check (score 3) and contacting "
         "admin about RED warnings (score 2) are friction points. "
         "Recommendation: automated email notification when data sources are refreshed."),
    ]
    for i, row in enumerate(qs_stages):
        pdf.mrow(list(row), jw, fill=(i % 2 == 1))
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 4: QS Professional journey stages, satisfaction scores, "
        "and pain point analysis."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)

    pdf.h2("4.2 Researcher / PI — Secondary Persona")
    pdf.para(
        "The Researcher/PI accesses iNHCES primarily for data analysis, model "
        "performance review, and pipeline oversight rather than project estimation. "
        "The journey has four stages with nine touchpoints. All research access "
        "touchpoints score 4-5, reflecting the researcher's comfort with technical "
        "interfaces. The main friction point is the absence of a direct MLflow "
        "interface — researchers must go via admin redirect to view experiment history."
    )

    pdf.h2("4.3 Design Recommendations from Journey Analysis")
    pdf.bullet([
        "Add a 'State Map' tooltip or interactive map on the location selection "
        "field to reduce friction for users unfamiliar with geopolitical zones.",
        "Display a prominent 'Data Freshness' indicator on the estimation results "
        "page showing the as-of date for each feature used. Colour-code GREEN/AMBER/RED.",
        "Implement a persistent report history page (list of past predictions and "
        "downloadable PDFs) to remove the 24-hour URL expiry pain point.",
        "Add email notifications to QS Professionals when the champion model "
        "is retrained (MAPE improved) — builds trust and encourages return visits.",
        "Add a read-only MLflow link for researchers in the Models page to "
        "avoid the admin redirect friction.",
    ])


# ── Section 5: Pipeline Flow ───────────────────────────────────────────────────
def section5(pdf):
    pdf.add_page()
    pdf.h1("5. Airflow Pipeline Flow Diagram")
    pdf.diagram_ref_box(
        "04_Pipeline_Flow.mmd",
        "Pipeline Flow — Airflow DAGs (Mermaid graph TD)",
        "Shows all 9 Airflow DAGs with cron schedules, external data sources, "
        "Supabase table targets, ML retrain pipeline, and drift detection flow."
    )

    pdf.h2("5.1 DAG Schedule Reference")
    dw = [48, 38, PAGE_W - 86]
    pdf.thead(["DAG Name", "Schedule (WAT)", "Data Source -> Target Table(s)"], dw)
    dags = [
        ("nhces_daily_fx_oil",      "06:00 daily\n(0 5 * * *)",
         "FRED API -> macro_fx  |  EIA API -> macro_oil"),
        ("nhces_weekly_materials",  "Monday 06:00\n(0 5 * * 1)",
         "BusinessDay + Jiji.ng scrapers -> material_cement, material_steel"),
        ("nhces_weekly_property",   "Tuesday 06:00\n(0 5 * * 2)",
         "PropertyPro + PrivateProperty scrapers -> market_prices"),
        ("nhces_monthly_macro",     "1st of month 06:00\n(0 5 1 * *)",
         "World Bank API -> macro_cpi, macro_interest  |  NNPC -> material_pms"),
        ("nhces_quarterly_niqs",    "Manual trigger\n(admin upload)",
         "Admin CSV upload -> unit_rates"),
        ("nhces_quarterly_nbs",     "Quarterly 06:00\n(0 5 1 1,4,7,10 *)",
         "NBS + CBN Stats -> macro_gdp (supplementary)"),
        ("nhces_worldbank_annual",  "2 Jan annually\n(0 5 2 1 *)",
         "World Bank API -> macro_gdp (annual refresh)"),
        ("nhces_retrain_weekly",    "Sunday 02:00 WAT\n(0 1 * * 0)",
         "All macro + material tables -> Feature matrix -> MLflow + R2"),
        ("nhces_drift_monitor",     "18:00 daily\n(0 17 * * *)",
         "Latest feature values vs. MLflow training baseline -> PSI check"),
    ]
    for i, row in enumerate(dags):
        pdf.mrow(list(row), dw, fill=(i % 2 == 1))
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 5: iNHCES Airflow DAG schedule reference. "
        "WAT = West Africa Time (UTC+1). "
        "DAG code for nhces_retrain_weekly: 05_ml_models/05_dags/nhces_retrain_weekly.py (O5 Step 4)."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)

    pdf.h2("5.2 ML Retrain Pipeline (DAG 8: nhces_retrain_weekly)")
    pdf.para(
        "The weekly retrain pipeline is the most complex Airflow DAG in iNHCES. "
        "It runs every Sunday at 02:00 WAT and follows this task sequence:"
    )
    pdf.bullet([
        "Task 1 — ASSEMBLE_FEATURES: Join all macro_* and material_* tables "
        "into a single feature matrix. Apply the same transformations as O2 "
        "feature engineering (first differences, log transforms, lag features). "
        "Save as a versioned CSV to Cloudflare R2 (datasets/{date}/train.csv).",
        "Task 2 — TRAIN_CHALLENGERS: Train all challenger models in parallel "
        "(Ridge/Lasso/ElasticNet, RF, XGBoost, LightGBM, MLP, SVR). "
        "Log each run to MLflow with metrics (MAPE, R2, MAE) and hyperparameters.",
        "Task 3 — TRAIN_STACKING: Train the stacking ensemble (XGBoost + "
        "LightGBM + RF base learners -> Ridge meta-learner) using cross-validated "
        "OOF predictions from Task 2 base models.",
        "Task 4 — COMPARE: Compare stacking ensemble MAPE against current "
        "Production champion MAPE. If challenger MAPE < (champion MAPE - 0.5%), "
        "mark challenger as Staging in MLflow.",
        "Task 5 — PROMOTE (conditional): If Task 4 flags improvement, "
        "update ml_models table: set is_champion=FALSE for old champion, "
        "is_champion=TRUE for new champion. Store .pkl to R2. "
        "Trigger FastAPI model cache refresh.",
        "Task 6 — AUDIT: Log retrain event to audit_log table with "
        "old champion MAPE, new champion MAPE, and promotion decision.",
    ])

    pdf.h2("5.3 Drift Detection Pipeline (DAG 9: nhces_drift_monitor)")
    pdf.para(
        "The drift monitor runs every evening at 18:00 WAT, after the "
        "nhces_daily_fx_oil DAG has completed, ensuring the latest FX and "
        "oil data is included in the drift assessment."
    )
    pdf.bullet([
        "Step 1: Load the training baseline distribution for each feature "
        "from the champion model's training dataset in MLflow.",
        "Step 2: Fetch the latest 30-day window of each feature from Supabase.",
        "Step 3: Compute Population Stability Index (PSI) for each feature. "
        "PSI = sum((actual% - expected%) * ln(actual% / expected%)) across buckets.",
        "Step 4: If PSI > 0.2 for any of the top-4 SHAP features "
        "(NGN/USD, CPI, NGN/EUR, Brent crude), trigger the "
        "nhces_retrain_weekly DAG immediately (emergency retrain).",
        "Step 5: Store PSI scores to audit_log for trend monitoring. "
        "Alert sent to System Admin if emergency retrain triggered.",
        "PSI thresholds: < 0.1 = stable (GREEN); 0.1-0.2 = slight drift "
        "(AMBER, monitor); > 0.2 = significant drift (RED, emergency retrain).",
    ])

    pdf.h2("5.4 Pipeline Failure Handling")
    pdf.bullet([
        "All DAGs are configured with retries=2, retry_delay=5 minutes. "
        "If all retries fail, Airflow marks the task as FAILED and sends "
        "an alert to the System Admin email.",
        "The nhces_daily_fx_oil DAG uses a synthetic fallback: if FRED or EIA "
        "API calls fail, the DAG extrapolates the last known value (forward fill) "
        "with a data_level='RED' flag. The /estimate endpoint will display a "
        "freshness warning to the user.",
        "Database insert failures are wrapped in try/except with Airflow task "
        "failure logging. A daily data quality check task verifies row counts "
        "in all tables match expected ranges.",
    ])


# ── Section 6: Diagram Consistency Checks ─────────────────────────────────────
def section6(pdf):
    pdf.add_page()
    pdf.h1("6. Cross-Diagram Consistency and Validation")
    pdf.para(
        "The four diagrams in this document must remain consistent with each other "
        "and with the O4 Step 1 architecture and O4 Step 2 database schema. "
        "The following checklist must be verified by the research team before "
        "the O6 build begins."
    )
    cv = [8, PAGE_W - 8]
    pdf.thead(["", "Consistency Check"], cv)
    checks = [
        ("[ ]", "DFD Level 0 external entities match O4 Step 1 Table 3 "
         "(External Integration Points). No entity in Level 0 is absent from "
         "the Step 1 integration table."),
        ("[ ]", "DFD Level 1 data stores (D1, D2, D3) match the three storage "
         "layers in O4 Step 1: Supabase PostgreSQL, Cloudflare R2, MLflow."),
        ("[ ]", "DFD Level 1 Process 2.0 (Cost Estimation) reads features from D1 "
         "tables defined in O4 Step 2 schema (macro_fx, macro_cpi, etc.)."),
        ("[ ]", "Pipeline Flow DAG table targets (Table 5) match the table names "
         "in O4 Step 2 schema (04_schema.sql). No DAG writes to a non-existent table."),
        ("[ ]", "User Journey satisfaction scores for data freshness warnings "
         "are consistent with the data_level field in O4 Step 2 schema tables."),
        ("[ ]", "nhces_retrain_weekly DAG task sequence matches the ML model "
         "family defined in Section 7.7 of PROJECT_CONTEXT.md "
         "(Ridge/Lasso, RF/XGB/LGB, MLP, SVR, Stacking Ensemble)."),
        ("[ ]", "PSI threshold values (0.1, 0.2) in Section 5.3 are consistent "
         "with the O5 SHAP analysis feature importance ranking (top-4 features "
         "monitored: NGN/USD, CPI, NGN/EUR, Brent crude)."),
        ("[ ]", "All four .mmd files render correctly in mermaid.live "
         "without syntax errors."),
        ("[ ]", "Diagram files committed to Git and present in "
         "04_conceptual_models/ directory."),
    ]
    for i, (chk, check) in enumerate(checks):
        pdf.mrow([chk, check], cv, fill=(i % 2 == 1))
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 6: Cross-diagram consistency checklist. "
        "All items must be ticked before O4 Step 4 and before O6 implementation begins."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)

    pdf.info_box(
        "DATA SOURCE: AMBER -- These diagrams are AI-authored conceptual models "
        "derived from O3 SRS requirements, O4 Step 1 architecture, and O4 Step 2 "
        "database schema. They represent intended system behaviour, not observed "
        "behaviour. The research team must validate all diagrams against the "
        "O3 Delphi consensus items and SRS requirements before proceeding to O6. "
        "In particular: confirm that all 36 Delphi consensus items are traceable "
        "to at least one process in DFD Level 1."
    )


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    out = os.path.join(OUT_DIR, 'O4_03_Data_Flow_Diagrams.pdf')
    pdf = DfdPDF()

    make_cover(pdf)
    _ds_page(pdf, 'amber',
        "DATA SOURCE: AMBER -- AI-AUTHORED DFDs DERIVED FROM O3 SRS + O4 STEPS 1-2",
        (
            "WHAT IS REAL IN THIS DOCUMENT:\n"
            "  * Diagram structures and data flows are derived from O3 Delphi consensus "
            "(36 items), SRS IEEE 830 (O3_07), O4 Step 1 architecture, and "
            "O4 Step 2 database schema. These are real design decisions.\n"
            "  * DAG schedule cron expressions are real Airflow syntax.\n"
            "  * PSI drift thresholds (0.1 / 0.2) are standard MLOps values.\n"
            "  * User journey stages and touchpoints reflect real system design.\n\n"
            "WHAT IS AI-GENERATED / UNVALIDATED:\n"
            "  * All narrative descriptions, process flow details, and design "
            "recommendations were drafted by Claude Code. Review before sign-off.\n"
            "  * User journey satisfaction scores (1-5) are estimated by AI "
            "from UX principles, not from real user testing.\n"
            "  * Diagram Mermaid source code may need refinement for publication-quality "
            "figures (font size, layout direction, node spacing).\n\n"
            "REQUIRED BEFORE O6 BUILD:\n"
            "  1. Render all four .mmd files in mermaid.live -- fix any syntax errors\n"
            "  2. Verify cross-diagram consistency (Table 6 checklist)\n"
            "  3. Confirm all 36 O3 Delphi consensus items are traceable to DFD Level 1\n"
            "  4. Research team sign-off on user journey touchpoints and pain points\n"
            "  5. Proceed to O4 Step 4: Chapter 4 Conceptual Models write-up"
        )
    )

    section1(pdf)
    section2(pdf)
    section3(pdf)
    section4(pdf)
    section5(pdf)
    section6(pdf)

    pdf.output(out)
    print(f"[OK]  O4_03_Data_Flow_Diagrams.pdf  saved -> {out}")
    print(f"      Pages: {pdf.page}")
    print("      DATA SOURCE: AMBER")
    print("      .mmd files: DFD_Level0 | DFD_Level1 | User_Journey | Pipeline_Flow")
    print("      Next: O4 Step 4 -- Chapter 4 Conceptual Models write-up")


if __name__ == "__main__":
    main()
