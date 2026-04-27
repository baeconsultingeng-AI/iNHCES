"""
iNHCES O4 Step 2 — Database Schema Document Generator
Deliverable: O4_02_Database_Schema.pdf
DATA SOURCE: AMBER — AI-designed schema based on O3 SRS and O4 Step 1 architecture.
             Schema must be validated and tested in Supabase before O6 build.

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
DOC_ID    = "O4-02"
DOC_TITLE = "iNHCES Database Schema Document"
DOC_SUBTITLE = "Supabase PostgreSQL — 16 Tables, RLS Policies, Seed Data"

GREEN_DB = (0, 110, 50)
RED_DB   = (160, 30, 30)
AMBER_DB = (160, 90, 0)


class SchemaPDF(DocPDF):
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
            "  |  O4 Step 2 — Database Schema"
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

    def table_header_box(self, table_name, description, data_level, group):
        """Coloured header for each table definition block."""
        colour_map = {
            'GREEN': GREEN_DB, 'AMBER': (140, 80, 0), 'RED': RED_DB
        }
        colour = colour_map.get(data_level, DARK_NAVY)
        self.ln(3)
        self.set_fill_color(*colour)
        self.set_draw_color(*GOLD)
        self.set_line_width(0.5)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*WHITE)
        self.set_x(LEFT)
        self.cell(PAGE_W, 7,
                  sanitize(f"  TABLE: {table_name}   [{data_level}]   Group: {group}"),
                  border=1, fill=True, ln=True)
        self.set_font("Helvetica", "I", 8.5)
        self.set_fill_color(245, 248, 255)
        self.set_text_color(*DARK_GREY)
        self.set_x(LEFT)
        self.multi_cell(PAGE_W, 5, sanitize(f"  {description}"), border="LBR", fill=True)
        self.ln(1)

    def col_table(self, rows):
        """Render a column definition table."""
        cw = [40, 28, 12, PAGE_W - 80]
        self.thead(["Column", "Type / Constraint", "PK/FK", "Description / Notes"], cw)
        for i, (col, typ, pkfk, desc) in enumerate(rows):
            self.mrow([col, typ, pkfk, desc], cw, fill=(i % 2 == 1))
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
        ("Step:",        "2 — Database Schema, RLS Policies, Seed Data"),
        ("Document ID:", DOC_ID),
        ("Version:",     "1.0 — Initial AI-Assisted Draft"),
        ("Date:",        date.today().strftime("%d %B %Y")),
        ("Grant:",       "TETFund National Research Fund (NRF) 2025"),
        ("SQL Files:",   "04_schema.sql  |  04_rls_policies.sql  |  04_seed_data.sql"),
        ("Next Step:",   "O4 Step 3 — Data Flow Diagrams (Mermaid .mmd files)"),
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
    pdf.h1("1. Schema Overview")
    pdf.para(
        "The iNHCES database is a single Supabase PostgreSQL schema (`public`) "
        "comprising 16 tables, 2 helper views, 1 enum type set (7 enums), "
        "and an audit trigger. Tables are organised into 5 functional groups: "
        "macroeconomic data, material prices, unit rates and market prices, "
        "project and prediction records, and system management. All tables "
        "have Row Level Security (RLS) enabled."
    )

    pdf.h2("1.1 Table Inventory")
    tw = [38, 28, 18, PAGE_W - 84]
    pdf.thead(["Table", "Group", "Data Level", "Primary Purpose"], tw)
    tables = [
        ("users",           "System",    "—",     "User profiles (extends Supabase auth.users)"),
        ("macro_fx",        "Macro",     "RED*",  "Daily NGN exchange rates (USD/EUR/GBP)"),
        ("macro_cpi",       "Macro",     "GREEN", "Annual/monthly CPI inflation (World Bank)"),
        ("macro_gdp",       "Macro",     "GREEN", "Annual GDP growth (World Bank)"),
        ("macro_interest",  "Macro",     "GREEN", "Lending rate and CBN MPR"),
        ("macro_oil",       "Macro",     "RED*",  "Brent crude price (EIA API)"),
        ("material_cement", "Materials", "RED*",  "Cement prices by brand and region"),
        ("material_steel",  "Materials", "RED*",  "Iron rod prices by diameter and region"),
        ("material_pms",    "Materials", "RED*",  "PMS (petrol) pump prices by state"),
        ("unit_rates",      "Rates",     "RED*",  "NIQS quarterly unit rates by trade"),
        ("market_prices",   "Rates",     "RED*",  "Property listing prices (NGN/sqm)"),
        ("projects",        "Projects",  "User",  "Cost estimation project records"),
        ("predictions",     "Projects",  "User",  "ML prediction log (/estimate calls)"),
        ("reports",         "Projects",  "User",  "PDF report records (R2 key + metadata)"),
        ("ml_models",       "System",    "System","ML model registry (mirrors MLflow)"),
        ("audit_log",       "System",    "System","Append-only system audit trail"),
    ]
    for i, row in enumerate(tables):
        pdf.trow(list(row), tw, fill=(i % 2 == 1))
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 1: iNHCES table inventory. "
        "RED* = synthetic in prototype (upgrade by configuring API keys). "
        "GREEN = live World Bank data. User = user-owned, RLS enforced."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)

    pdf.h2("1.2 Enum Types")
    pdf.bullet([
        "user_role: qsprofessional | researcher | admin",
        "project_status: active | completed | archived",
        "building_type: Residential | Commercial | Industrial | Institutional | Mixed Use",
        "construction_type: New Build | Renovation | Extension | Fit-Out",
        "model_stage: Production | Staging | Archived",
        "data_source_level: GREEN | AMBER | RED",
        "nigeria_zone: North Central | North East | North West | South East | South South | South West",
    ])

    pdf.h2("1.3 Helper Views")
    pdf.bullet([
        "v_latest_macro: Single-row-per-variable latest macro snapshot. "
        "Used by FastAPI GET /macro endpoint. Returns ngn_usd, cpi_annual_pct, "
        "gdp_growth_pct, lending_rate_pct, brent_usd_barrel with source and data_level.",
        "v_champion_model: Single-row view of the current Production ML model "
        "(is_champion=TRUE). Used by FastAPI /estimate endpoint to load model metadata.",
    ])


# ── Section 2: Table Definitions ──────────────────────────────────────────────
def section2_users(pdf):
    pdf.add_page()
    pdf.h1("2. Table Definitions — System Tables")
    pdf.table_header_box("users", "User profiles. Extends Supabase auth.users via trigger.", "AMBER", "System")
    pdf.col_table([
        ("id",          "UUID PK",              "PK / FK",  "References auth.users(id). Set by Supabase on registration."),
        ("email",       "TEXT UNIQUE NOT NULL",  "—",        "User email. Synced from auth.users."),
        ("full_name",   "TEXT",                  "—",        "Display name. Set from registration metadata."),
        ("role",        "user_role DEFAULT 'qsprofessional'","—","Access control role. Change via admin dashboard only."),
        ("institution", "TEXT",                  "—",        "University/firm affiliation. Optional."),
        ("phone",       "TEXT",                  "—",        "Optional contact number."),
        ("created_at",  "TIMESTAMPTZ DEFAULT NOW()","—",     "Auto-set on insert."),
        ("updated_at",  "TIMESTAMPTZ DEFAULT NOW()","—",     "Auto-updated by set_updated_at() trigger."),
    ])

    pdf.table_header_box("ml_models", "ML model registry. Mirrors MLflow Model Registry.", "AMBER", "System")
    pdf.col_table([
        ("id",               "UUID PK",              "PK",  "gen_random_uuid()"),
        ("mlflow_run_id",    "TEXT UNIQUE NOT NULL",  "—",   "MLflow experiment run ID. Used to retrieve artifact."),
        ("model_name",       "TEXT NOT NULL",         "—",   "stacking_ensemble | xgboost | rf | lightgbm | mlp | svr | ridge"),
        ("stage",            "model_stage DEFAULT 'Staging'","—","Production = champion. Staging = challenger. Archived = retired."),
        ("mape_test",        "NUMERIC(8,4)",           "—",   "% MAPE on holdout test set. Target: <= 15%."),
        ("r2_test",          "NUMERIC(8,4)",           "—",   "R2 on holdout test set. Target: >= 0.90."),
        ("mae_test",         "NUMERIC(12,2)",          "—",   "Mean Absolute Error in NGN/sqm."),
        ("training_date",    "DATE",                   "—",   "Date of training run."),
        ("feature_count",    "INTEGER",                "—",   "Number of input features."),
        ("training_rows",    "INTEGER",                "—",   "Number of training samples."),
        ("r2_artifact_key",  "TEXT",                   "—",   "Cloudflare R2 path to .pkl model file."),
        ("hyperparameters",  "JSONB",                  "—",   "Model hyperparameters as JSON."),
        ("feature_importance","JSONB",                 "—",   "SHAP importance per feature as JSON {feature: pct}."),
        ("is_champion",      "BOOLEAN DEFAULT FALSE",  "—",   "TRUE for current Production model. Unique index enforces one champion."),
        ("promoted_by",      "UUID",                   "FK",  "References users(id). Admin who promoted to Production."),
        ("promoted_at",      "TIMESTAMPTZ",            "—",   "When promoted to Production."),
        ("created_at",       "TIMESTAMPTZ DEFAULT NOW()","—", "Auto-set on insert."),
    ])

    pdf.table_header_box("audit_log", "Append-only system audit trail. INSERT only — no UPDATE or DELETE.", "AMBER", "System")
    pdf.col_table([
        ("id",         "BIGSERIAL PK",           "PK",  "Auto-increment."),
        ("user_id",    "UUID",                    "FK",  "References users(id). NULL for system actions."),
        ("action",     "TEXT NOT NULL",           "—",   "login | predict | export_report | promote_model | admin_action | seed_data_loaded"),
        ("table_name", "TEXT",                    "—",   "Affected table name (if applicable)."),
        ("record_id",  "TEXT",                    "—",   "String representation of affected record PK."),
        ("old_values", "JSONB",                   "—",   "Previous values (for UPDATE actions)."),
        ("new_values", "JSONB",                   "—",   "New values."),
        ("ip_address", "INET",                    "—",   "Client IP address."),
        ("user_agent", "TEXT",                    "—",   "Browser/client user agent string."),
        ("created_at", "TIMESTAMPTZ DEFAULT NOW()","—",  "Auto-set. Indexed DESC for performance."),
    ])


def section2_macro(pdf):
    pdf.add_page()
    pdf.h1("2 (cont). Table Definitions — Macroeconomic Tables")

    pdf.table_header_box("macro_fx", "Daily NGN exchange rates. Source: FRED API (CBN proxy).", "RED", "Macro")
    pdf.col_table([
        ("id",         "BIGSERIAL PK",             "PK", "Auto-increment."),
        ("date",       "DATE NOT NULL UNIQUE",      "—",  "Observation date. UNIQUE constraint — one row per day."),
        ("ngn_usd",    "NUMERIC(12,4) NOT NULL",    "—",  "NGN per 1 USD. Key feature for ML model."),
        ("ngn_eur",    "NUMERIC(12,4)",              "—",  "NGN per 1 EUR (FRED cross-rate)."),
        ("ngn_gbp",    "NUMERIC(12,4)",              "—",  "NGN per 1 GBP (FRED cross-rate)."),
        ("source",     "TEXT DEFAULT 'FRED'",        "—",  "Data source: FRED | CBN | synthetic"),
        ("data_level", "data_source_level DEFAULT 'RED'","—","RED until FRED_API_KEY configured; then GREEN."),
        ("created_at", "TIMESTAMPTZ DEFAULT NOW()",  "—",  "Insert timestamp."),
    ])

    pdf.table_header_box("macro_cpi", "CPI inflation (annual or monthly). Source: World Bank.", "GREEN", "Macro")
    pdf.col_table([
        ("id",             "BIGSERIAL PK",           "PK", "Auto-increment."),
        ("date",           "DATE NOT NULL",           "—",  "Period start date. UNIQUE with frequency."),
        ("frequency",      "TEXT DEFAULT 'annual'",   "—",  "annual | monthly"),
        ("cpi_annual_pct", "NUMERIC(8,4) NOT NULL",   "—",  "Annual % change in CPI. Key ML feature."),
        ("source",         "TEXT DEFAULT 'World Bank'","—", "World Bank Open Data (FP.CPI.TOTL.ZG)."),
        ("data_level",     "data_source_level DEFAULT 'GREEN'","—","GREEN — live World Bank API."),
        ("created_at",     "TIMESTAMPTZ DEFAULT NOW()","—", "Insert timestamp."),
    ])

    pdf.table_header_box("macro_gdp", "Annual GDP growth. Source: World Bank.", "GREEN", "Macro")
    pdf.col_table([
        ("id",                 "BIGSERIAL PK",         "PK", "Auto-increment."),
        ("date",               "DATE NOT NULL UNIQUE",  "—",  "Year start (YYYY-01-01)."),
        ("gdp_growth_pct",     "NUMERIC(8,4) NOT NULL", "—",  "Real GDP growth % (annual). ML feature."),
        ("gdp_per_capita_usd", "NUMERIC(12,2)",         "—",  "GDP per capita USD. Optional enrichment."),
        ("source",             "TEXT DEFAULT 'World Bank'","—","World Bank (NY.GDP.MKTP.KD.ZG)."),
        ("data_level",         "data_source_level DEFAULT 'GREEN'","—","GREEN."),
        ("created_at",         "TIMESTAMPTZ DEFAULT NOW()","—","Insert timestamp."),
    ])

    pdf.table_header_box("macro_interest", "Lending rate and MPR. Source: World Bank + CBN.", "GREEN", "Macro")
    pdf.col_table([
        ("id",               "BIGSERIAL PK",         "PK", "Auto-increment."),
        ("date",             "DATE NOT NULL",         "—",  "Period start. UNIQUE with frequency."),
        ("frequency",        "TEXT DEFAULT 'annual'", "—",  "annual | monthly"),
        ("lending_rate_pct", "NUMERIC(8,4) NOT NULL", "—",  "Commercial lending rate %. ML feature."),
        ("mpr_pct",          "NUMERIC(8,4)",          "—",  "CBN Monetary Policy Rate %. Optional."),
        ("source",           "TEXT DEFAULT 'World Bank'","—","World Bank (FR.INR.LEND) + CBN."),
        ("data_level",       "data_source_level DEFAULT 'GREEN'","—","GREEN."),
        ("created_at",       "TIMESTAMPTZ DEFAULT NOW()","—","Insert timestamp."),
    ])

    pdf.table_header_box("macro_oil", "Brent crude oil price. Source: EIA API.", "RED", "Macro")
    pdf.col_table([
        ("id",                "BIGSERIAL PK",         "PK", "Auto-increment."),
        ("date",              "DATE NOT NULL",         "—",  "Period start. UNIQUE with frequency."),
        ("frequency",         "TEXT DEFAULT 'annual'", "—",  "annual | monthly | daily"),
        ("brent_usd_barrel",  "NUMERIC(10,4) NOT NULL","—",  "Brent crude USD/barrel. ML feature."),
        ("source",            "TEXT DEFAULT 'EIA'",    "—",  "EIA API (PET.RBRTE.A)."),
        ("data_level",        "data_source_level DEFAULT 'RED'","—","RED until EIA_API_KEY configured."),
        ("created_at",        "TIMESTAMPTZ DEFAULT NOW()","—","Insert timestamp."),
    ])


def section2_materials(pdf):
    pdf.add_page()
    pdf.h1("2 (cont). Table Definitions — Material Price Tables")

    pdf.table_header_box("material_cement", "Weekly cement prices by brand and region.", "RED", "Materials")
    pdf.col_table([
        ("id",             "BIGSERIAL PK",          "PK", "Auto-increment."),
        ("date",           "DATE NOT NULL",          "—",  "Observation date. UNIQUE with brand + region."),
        ("brand",          "TEXT NOT NULL",          "—",  "Dangote | BUA | Lafarge | UNICEM | Ibeto"),
        ("region",         "TEXT NOT NULL",          "—",  "North | South-West | South-East | South-South"),
        ("state",          "TEXT",                   "—",  "Optional (more granular than region)."),
        ("price_ngn_50kg", "NUMERIC(10,2) NOT NULL", "—",  "Price per 50kg bag in NGN."),
        ("source",         "TEXT DEFAULT 'BusinessDay'","—","BusinessDay scraper."),
        ("data_level",     "data_source_level DEFAULT 'RED'","—","RED — scraper data (replace with live when scraper operational)."),
        ("created_at",     "TIMESTAMPTZ DEFAULT NOW()","—", "Insert timestamp."),
    ])

    pdf.table_header_box("material_steel", "Weekly iron rod prices by diameter and region.", "RED", "Materials")
    pdf.col_table([
        ("id",               "BIGSERIAL PK",         "PK", "Auto-increment."),
        ("date",             "DATE NOT NULL",         "—",  "Observation date. UNIQUE with diameter + region."),
        ("diameter_mm",      "INTEGER NOT NULL",      "—",  "CHECK IN (8,10,12,16,20,25,32) — standard Nigerian bar sizes."),
        ("region",           "TEXT NOT NULL",         "—",  "North | South-West | South-East | South-South"),
        ("state",            "TEXT",                  "—",  "Optional."),
        ("price_ngn_tonne",  "NUMERIC(12,2) NOT NULL","—",  "Price per metric tonne in NGN."),
        ("source",           "TEXT DEFAULT 'Jiji.ng'","—",  "Jiji.ng / BuildBay scraper."),
        ("data_level",       "data_source_level DEFAULT 'RED'","—","RED."),
        ("created_at",       "TIMESTAMPTZ DEFAULT NOW()","—","Insert timestamp."),
    ])

    pdf.table_header_box("material_pms", "Monthly PMS (petrol) pump prices by state.", "RED", "Materials")
    pdf.col_table([
        ("id",               "BIGSERIAL PK",         "PK", "Auto-increment."),
        ("date",             "DATE NOT NULL",         "—",  "Month start. UNIQUE with state."),
        ("state",            "TEXT NOT NULL",         "—",  "All 36 states + FCT Abuja."),
        ("price_ngn_litre",  "NUMERIC(8,2) NOT NULL", "—",  "PMS pump price per litre in NGN."),
        ("source",           "TEXT DEFAULT 'NNPC'",   "—",  "NNPC / NMDPRA official price."),
        ("data_level",       "data_source_level DEFAULT 'RED'","—","RED — scraper/manual data."),
        ("created_at",       "TIMESTAMPTZ DEFAULT NOW()","—","Insert timestamp."),
    ])


def section2_projects(pdf):
    pdf.add_page()
    pdf.h1("2 (cont). Table Definitions — Rates and Project Tables")

    pdf.table_header_box("unit_rates", "NIQS quarterly unit rates by trade and region.", "RED", "Rates")
    pdf.col_table([
        ("id",            "BIGSERIAL PK",          "PK", "Auto-increment."),
        ("quarter_date",  "DATE NOT NULL",          "—",  "Quarter start: 2024-01-01 / 2024-04-01 / 2024-07-01 / 2024-10-01."),
        ("trade",         "TEXT NOT NULL",          "—",  "Substructure | Frame | Walling | Roofing | Finishes | M&E | External"),
        ("description",   "TEXT NOT NULL",          "—",  "Specific work item (e.g., 'RC column 300x300mm')."),
        ("unit",          "TEXT NOT NULL",          "—",  "m2 | m3 | nr | lm | item | tonne"),
        ("region",        "TEXT NOT NULL",          "—",  "North | South-West | South-East | South-South"),
        ("building_type", "building_type",          "—",  "Residential | Commercial | Industrial | Institutional"),
        ("rate_ngn",      "NUMERIC(12,2) NOT NULL", "—",  "Unit rate in NGN. Quarterly NIQS figure."),
        ("source",        "TEXT DEFAULT 'NIQS'",    "—",  "NIQS Quarterly Schedule (manual upload)."),
        ("data_level",    "data_source_level DEFAULT 'RED'","—","RED until real NIQS data uploaded."),
        ("created_at",    "TIMESTAMPTZ DEFAULT NOW()","—", "Insert timestamp."),
    ])

    pdf.table_header_box("market_prices", "Weekly property listing prices (NGN/sqm) by zone.", "RED", "Rates")
    pdf.col_table([
        ("id",              "BIGSERIAL PK",          "PK", "Auto-increment."),
        ("date",            "DATE NOT NULL",          "—",  "Observation date. UNIQUE with zone+state+type+source."),
        ("zone",            "nigeria_zone NOT NULL",  "—",  "Six geopolitical zones."),
        ("state",           "TEXT NOT NULL",          "—",  "State name."),
        ("city",            "TEXT",                   "—",  "Optional city/LGA."),
        ("property_type",   "TEXT NOT NULL",          "—",  "Bungalow | Duplex | Flat | Terrace | Detached"),
        ("price_ngn_sqm",   "NUMERIC(12,2) NOT NULL", "—",  "Listing price per sqm in NGN."),
        ("listing_count",   "INTEGER DEFAULT 1",      "—",  "Number of listings averaged for this row."),
        ("source",          "TEXT DEFAULT 'PropertyPro'","—","PropertyPro / PrivateProperty scraper."),
        ("data_level",      "data_source_level DEFAULT 'RED'","—","RED."),
        ("created_at",      "TIMESTAMPTZ DEFAULT NOW()","—", "Insert timestamp."),
    ])

    pdf.table_header_box("projects", "User cost estimation projects. RLS: users see own rows only.", "AMBER", "Projects")
    pdf.col_table([
        ("id",                "UUID PK",               "PK",   "gen_random_uuid()."),
        ("user_id",           "UUID NOT NULL",          "FK",   "References users(id) ON DELETE CASCADE."),
        ("title",             "TEXT NOT NULL",          "—",    "Project name (e.g., '3-Bed Bungalow, Kaduna')."),
        ("building_type",     "building_type",          "—",    "Residential | Commercial | Industrial | Institutional | Mixed Use"),
        ("construction_type", "construction_type",      "—",    "New Build | Renovation | Extension | Fit-Out"),
        ("floor_area_sqm",    "NUMERIC(10,2) NOT NULL", "—",    "Gross floor area in sqm. CHECK > 0."),
        ("num_floors",        "INTEGER DEFAULT 1",      "—",    "Number of floors. CHECK >= 1."),
        ("location_state",    "TEXT NOT NULL",          "—",    "Nigerian state."),
        ("location_zone",     "nigeria_zone NOT NULL",  "—",    "Geopolitical zone."),
        ("location_lga",      "TEXT",                   "—",    "Local Government Area. Optional."),
        ("target_cost_ngn",   "NUMERIC(15,2)",          "—",    "Client budget in NGN. Optional."),
        ("notes",             "TEXT",                   "—",    "Free-text notes."),
        ("status",            "project_status DEFAULT 'active'","—","active | completed | archived"),
        ("created_at",        "TIMESTAMPTZ DEFAULT NOW()","—",  "Auto-set."),
        ("updated_at",        "TIMESTAMPTZ DEFAULT NOW()","—",  "Auto-updated by trigger."),
    ])

    pdf.table_header_box("predictions", "ML prediction log. One row per /estimate call.", "AMBER", "Projects")
    pdf.col_table([
        ("id",                      "UUID PK",              "PK", "gen_random_uuid()."),
        ("project_id",              "UUID NOT NULL",         "FK", "References projects(id) ON DELETE CASCADE."),
        ("user_id",                 "UUID NOT NULL",         "FK", "References users(id). Denormalised for RLS."),
        ("model_version",           "TEXT NOT NULL",         "—",  "MLflow run_id of champion model used."),
        ("model_stage",             "model_stage",           "—",  "Production | Staging"),
        ("predicted_cost_per_sqm",  "NUMERIC(12,2) NOT NULL","—",  "ML prediction in NGN/sqm."),
        ("total_predicted_cost_ngn","NUMERIC(15,2)",         "—",  "predicted_per_sqm * floor_area_sqm."),
        ("confidence_lower",        "NUMERIC(12,2)",         "—",  "Lower bound of 90% prediction interval."),
        ("confidence_upper",        "NUMERIC(12,2)",         "—",  "Upper bound of 90% prediction interval."),
        ("mape_at_prediction",      "NUMERIC(8,4)",          "—",  "Champion model MAPE at time of this call."),
        ("feature_snapshot",        "JSONB",                 "—",  "Macro + material feature values used. Enables auditability."),
        ("shap_values",             "JSONB",                 "—",  "SHAP value per feature {feature: value}. For explainability."),
        ("api_response_ms",         "INTEGER",               "—",  "Response time of /estimate call in ms."),
        ("created_at",              "TIMESTAMPTZ DEFAULT NOW()","—","Auto-set."),
    ])

    pdf.table_header_box("reports", "PDF cost report metadata. Actual files in Cloudflare R2.", "AMBER", "Projects")
    pdf.col_table([
        ("id",              "UUID PK",               "PK", "gen_random_uuid()."),
        ("project_id",      "UUID NOT NULL",          "FK", "References projects(id) ON DELETE CASCADE."),
        ("prediction_id",   "UUID",                   "FK", "References predictions(id) ON DELETE SET NULL."),
        ("user_id",         "UUID NOT NULL",          "FK", "References users(id). For RLS."),
        ("r2_key",          "TEXT NOT NULL UNIQUE",   "—",  "Cloudflare R2 object key (path). E.g.: reports/{user_id}/{project_id}/{ts}.pdf"),
        ("file_size_bytes", "INTEGER",                "—",  "PDF file size."),
        ("page_count",      "INTEGER",                "—",  "Number of pages in the PDF report."),
        ("created_at",      "TIMESTAMPTZ DEFAULT NOW()","—","Auto-set."),
    ])


# ── Section 3: RLS Summary ─────────────────────────────────────────────────────
def section3(pdf):
    pdf.add_page()
    pdf.h1("3. Row Level Security Policy Summary")
    pdf.para(
        "All 16 tables have RLS enabled. The full policy definitions are in "
        "`04_rls_policies.sql`. The table below summarises the access matrix "
        "for the four principal access contexts."
    )
    rw = [34, 25, 25, 25, PAGE_W - 109]
    pdf.thead(["Table", "anon", "authenticated", "service_role", "Notes"], rw)
    rls_rows = [
        ("users",           "NONE",   "own row only",   "ALL",    "Admin can read/update all"),
        ("macro_fx",        "NONE",   "SELECT all",     "ALL",    "Airflow DAG inserts"),
        ("macro_cpi",       "NONE",   "SELECT all",     "ALL",    "World Bank pipeline"),
        ("macro_gdp",       "NONE",   "SELECT all",     "ALL",    "World Bank pipeline"),
        ("macro_interest",  "NONE",   "SELECT all",     "ALL",    "World Bank pipeline"),
        ("macro_oil",       "NONE",   "SELECT all",     "ALL",    "EIA pipeline"),
        ("material_cement", "NONE",   "SELECT all",     "ALL",    "Scraper DAG inserts"),
        ("material_steel",  "NONE",   "SELECT all",     "ALL",    "Scraper DAG inserts"),
        ("material_pms",    "NONE",   "SELECT all",     "ALL",    "NNPC pipeline"),
        ("unit_rates",      "NONE",   "SELECT all",     "ALL",    "Admin can DELETE"),
        ("market_prices",   "NONE",   "SELECT all",     "ALL",    "Scraper DAG inserts"),
        ("projects",        "NONE",   "own rows",       "ALL",    "Researcher: read all"),
        ("predictions",     "NONE",   "own rows",       "ALL",    "Researcher: read all"),
        ("reports",         "NONE",   "own rows",       "ALL",    "Admin: read all"),
        ("ml_models",       "NONE",   "SELECT all",     "ALL",    "Admin: UPDATE/DELETE"),
        ("audit_log",       "NONE",   "INSERT only",    "ALL",    "Admin: SELECT only"),
    ]
    for i, row in enumerate(rls_rows):
        pdf.trow(list(row), rw, fill=(i % 2 == 1))
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 2: RLS access matrix. NONE = no access. "
        "own rows = user_id = auth.uid(). "
        "service_role bypasses RLS (Airflow + FastAPI backend)."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)


# ── Section 4: Seed Data Summary ──────────────────────────────────────────────
def section4(pdf):
    pdf.add_page()
    pdf.h1("4. Seed Data Summary")
    pdf.info_box(
        "DATA SOURCE: RED -- All seed data is SYNTHETIC. "
        "Values are approximate real-world ranges for Nigerian construction "
        "costs and macroeconomic data (2020-2024 estimates). "
        "DO NOT use seed data for any published analysis or grant reporting. "
        "File: 04_conceptual_models/04_seed_data.sql"
    )
    pdf.ln(2)
    sw = [40, 12, PAGE_W - 52]
    pdf.thead(["Table", "Rows", "Description"], sw)
    seed_rows = [
        ("users",           "3",  "1 per role: qsprofessional, researcher, admin. Test UUIDs."),
        ("macro_fx",        "5",  "Annual 2020-2024. NGN/USD: 381 to 1480 (approx CBN official)."),
        ("macro_cpi",       "5",  "Annual 2020-2024. CPI: 13.2% to 31.7%."),
        ("macro_gdp",       "5",  "Annual 2020-2024. GDP growth: -1.8% to +3.4%."),
        ("macro_interest",  "5",  "Annual 2020-2024. Lending rate: 25.8% to 29.5%."),
        ("macro_oil",       "5",  "Annual 2020-2024. Brent: $42 to $99 USD/barrel."),
        ("material_cement", "8",  "Dangote/BUA/Lafarge/UNICEM x 4 regions. NGN 8,300-10,200 per 50kg."),
        ("material_steel",  "7",  "12mm and 16mm x 4 regions. NGN 580,000-680,000 per tonne."),
        ("material_pms",    "7",  "7 states. NGN 610-665 per litre (post-deregulation 2024)."),
        ("unit_rates",      "15", "Representative NIQS rates: substructure, frame, walling, roofing, finishes, M&E."),
        ("market_prices",   "8",  "8 location/type combinations. NGN 145,000-850,000/sqm."),
        ("projects",        "2",  "3-bed bungalow Kaduna (120 sqm) + 4-bed duplex Lagos (250 sqm)."),
        ("predictions",     "1",  "NGN 182,500/sqm (Kaduna bungalow). MAPE=12.4%, R2=0.934."),
        ("ml_models",       "1",  "Seed champion: stacking ensemble, MAPE=12.4%, R2=0.934."),
        ("audit_log",       "1",  "Seed load event record."),
    ]
    for i, row in enumerate(seed_rows):
        pdf.trow(list(row), sw, fill=(i % 2 == 1))
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 3: Seed data row counts and descriptions. "
        "Run 04_seed_data.sql in Supabase SQL Editor with service_role to load."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)


# ── Section 5: Setup Instructions ─────────────────────────────────────────────
def section5(pdf):
    pdf.add_page()
    pdf.h1("5. Supabase Setup Instructions")

    pdf.h2("5.1 Create Supabase Project")
    pdf.bullet([
        "Go to supabase.com -> New Project. Choose a region close to Nigeria "
        "(Europe West or US East are closest available at time of writing).",
        "Note your Project URL and anon/service_role keys from Settings -> API.",
        "Add to Railway environment variables: SUPABASE_URL, SUPABASE_ANON_KEY, "
        "SUPABASE_SERVICE_KEY, SUPABASE_JWT_SECRET.",
    ])

    pdf.h2("5.2 Run SQL Files in Order")
    pdf.code_box(
        "# In Supabase Dashboard -> SQL Editor -> New Query:\n\n"
        "# Step 1: Run the schema\n"
        "#   Paste contents of 04_schema.sql -> Run\n"
        "#   Expected: 'Success. No rows returned.' for each statement.\n\n"
        "# Step 2: Run the RLS policies\n"
        "#   Paste contents of 04_rls_policies.sql -> Run\n\n"
        "# Step 3 (optional): Load seed data\n"
        "#   Paste contents of 04_seed_data.sql -> Run\n"
        "#   Note: seed users reference auth.users UUIDs that do not exist yet.\n"
        "#   Either create test auth accounts first and replace the UUIDs,\n"
        "#   or run seed data with service_role (bypasses FK check in some versions).\n\n"
        "# Step 4: Verify\n"
        "SELECT COUNT(*) FROM public.macro_fx;        -- expect 5 (with seed)\n"
        "SELECT COUNT(*) FROM public.material_cement; -- expect 8\n"
        "SELECT is_champion FROM public.ml_models;    -- expect 1 TRUE row\n"
        "SELECT * FROM public.v_latest_macro;         -- expect 5 rows"
    )

    pdf.h2("5.3 Create Test Auth Users (for seed data)")
    pdf.bullet([
        "In Supabase Dashboard -> Authentication -> Users -> Add User:",
        "  Email: qs.professional@test.nhces.ng  |  Password: [set a test password]",
        "  Email: researcher@test.nhces.ng",
        "  Email: admin@test.nhces.ng",
        "Copy the generated auth.users UUIDs and replace the hardcoded "
        "'00000000-...' UUIDs in 04_seed_data.sql before running it.",
        "The handle_new_user trigger will automatically create rows in "
        "public.users. Then update the role column via SQL Editor for "
        "researcher and admin accounts.",
    ])

    pdf.h2("5.4 Validation Checklist Before O6 Build")
    pdf.info_box(
        "Before beginning O6 (FastAPI backend implementation), verify:\n\n"
        "  [ ] All 16 tables created without errors in Supabase\n"
        "  [ ] RLS policies active (Supabase -> Auth -> Policies shows policies per table)\n"
        "  [ ] v_latest_macro view returns 5 rows with correct variable names\n"
        "  [ ] v_champion_model view returns 1 row (after seed data loaded)\n"
        "  [ ] Test users created and roles correctly set\n"
        "  [ ] SUPABASE_URL and all keys added to Railway environment variables\n"
        "  [ ] Research team has reviewed schema design decisions against O3 SRS requirements\n"
        "  [ ] Any schema changes agreed by research team documented before O6 build begins"
    )


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    out = os.path.join(OUT_DIR, 'O4_02_Database_Schema.pdf')
    pdf = SchemaPDF()

    make_cover(pdf)

    _ds_page(pdf, 'amber',
        "DATA SOURCE: AMBER -- AI-DESIGNED SCHEMA FROM O3 SRS AND O4 STEP 1 ARCHITECTURE",
        (
            "WHAT IS REAL IN THIS DOCUMENT:\n"
            "  * Table names, column names, and data types derived from O3 Delphi "
            "consensus (36 items), SRS IEEE 830 requirements, and O4 Step 1 "
            "architecture decisions. These are real design specifications.\n"
            "  * RLS policy design follows Supabase PostgreSQL security best practices.\n"
            "  * Enum values, constraint types, and index choices are real engineering decisions.\n\n"
            "WHAT IS AI-GENERATED / UNVALIDATED:\n"
            "  * Full SQL syntax was generated by Claude Code. "
            "Must be tested in a real Supabase instance before O6 build.\n"
            "  * Seed data values are SYNTHETIC (approximate real-world ranges). "
            "All seed rows have data_level='RED'.\n"
            "  * Column descriptions and business logic notes were drafted by AI -- "
            "review against actual O3 SRS before signing off.\n\n"
            "REQUIRED BEFORE O6 BUILD:\n"
            "  1. Run 04_schema.sql in Supabase SQL Editor -- fix any syntax errors\n"
            "  2. Run 04_rls_policies.sql and verify policies appear in Supabase Auth panel\n"
            "  3. Run 04_seed_data.sql (with real auth user UUIDs) and verify row counts\n"
            "  4. Research team review of all table designs against O3 SRS requirements\n"
            "  5. Proceed to O4 Step 3: Data Flow Diagrams (04_DFD_Level0.mmd etc.)"
        )
    )

    section1(pdf)
    section2_users(pdf)
    section2_macro(pdf)
    section2_materials(pdf)
    section2_projects(pdf)
    section3(pdf)
    section4(pdf)
    section5(pdf)

    pdf.output(out)
    print(f"[OK]  O4_02_Database_Schema.pdf  saved -> {out}")
    print(f"      Pages: {pdf.page}")
    print("      DATA SOURCE: AMBER")
    print("      SQL files: 04_schema.sql | 04_rls_policies.sql | 04_seed_data.sql")
    print("      Next: O4 Step 3 -- Data Flow Diagrams")


if __name__ == "__main__":
    main()
