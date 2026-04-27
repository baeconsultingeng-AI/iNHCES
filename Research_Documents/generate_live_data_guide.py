"""
iNHCES Live Data Infrastructure Guide — PDF Generator
Sections 7-12: Online Data Sources Registry, Pipeline Architecture,
Web System (Objective 6), Research Timeline, Target Journals,
Final Recommendations.
Output: Research_Documents/04_iNHCES_Live_Data_Infrastructure_Guide.pdf
"""
import os, sys
from datetime import date

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, os.path.join(_ROOT, "01_literature_review"))

from generate_o1_pdfs import (
    DocPDF, sanitize, _ds_page,
    DARK_NAVY, GOLD, LIGHT_BLUE, WHITE, DARK_GREY, MID_GREY,
    PAGE_W, LEFT, LINE_H,
)

OUTPUT_PATH = os.path.join(_HERE, "04_iNHCES_Live_Data_Infrastructure_Guide.pdf")

# ── Palette ────────────────────────────────────────────────────────────────────
TEAL        = (0,  90,  100)
PALE_TEAL   = (220, 245, 248)
AMBER       = (255, 235, 185)
AMBER_BORDER= (180, 100,   0)

# ── PDF class ─────────────────────────────────────────────────────────────────
class GuidePDF(DocPDF):
    def __init__(self):
        super().__init__("04_iNHCES_Live_Data_Infrastructure_Guide.pdf",
                         "iNHCES Live Data Infrastructure Guide")
        self.set_margins(12, 18, 12)
        self.set_auto_page_break(True, margin=20)

    def header(self):
        self.set_fill_color(*DARK_NAVY)
        self.rect(0, 0, 210, 14, "F")
        self.set_font("Helvetica", "B", 7.5)
        self.set_text_color(*WHITE)
        self.set_xy(5, 4)
        self.cell(0, 6, sanitize(
            "iNHCES Live Data Infrastructure Guide  |  ABU Zaria / TETFund  |  S2RF Project"
        ))
        self.set_text_color(*DARK_GREY)
        self.ln(16)

    def footer(self):
        self.set_y(-13)
        self.set_draw_color(*GOLD)
        self.set_line_width(0.5)
        self.line(12, self.get_y(), 198, self.get_y())
        self.set_font("Helvetica", "", 7.5)
        self.set_text_color(*MID_GREY)
        self.cell(0, 6,
                  sanitize(f"iNHCES Live Data Infrastructure Guide | ABU Zaria / TETFund | "
                            f"April 2026 | S2RF Governed"),
                  align="C")

    # ── Helpers ────────────────────────────────────────────────────────────────
    def section_title(self, text):
        self.ln(4)
        self.set_fill_color(*DARK_NAVY)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*WHITE)
        self.set_x(LEFT)
        self.cell(PAGE_W, 8, sanitize(f"  {text}"), fill=True, ln=True)
        self.ln(3)

    def sub_heading(self, text):
        self.ln(3)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*TEAL)
        self.set_x(LEFT)
        self.cell(PAGE_W, 7, sanitize(text), ln=True)
        self.set_draw_color(*TEAL)
        self.set_line_width(0.4)
        self.line(LEFT, self.get_y(), LEFT + PAGE_W, self.get_y())
        self.ln(2)

    def body(self, text):
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*DARK_GREY)
        self.set_x(LEFT)
        self.multi_cell(PAGE_W, LINE_H, sanitize(text))
        self.ln(2)

    def info_box(self, text):
        self.ln(2)
        self.set_fill_color(*PALE_TEAL)
        self.set_draw_color(*TEAL)
        self.set_line_width(0.6)
        self.set_x(LEFT)
        self.set_font("Helvetica", "", 8.5)
        self.set_text_color(*DARK_GREY)
        self.multi_cell(PAGE_W, 5.5, sanitize(text), border=1, fill=True)
        self.ln(3)

    def warn_box(self, text):
        self.ln(2)
        self.set_fill_color(*AMBER)
        self.set_draw_color(*AMBER_BORDER)
        self.set_line_width(0.6)
        self.set_x(LEFT)
        self.set_font("Helvetica", "B", 8.5)
        self.set_text_color(*AMBER_BORDER)
        self.multi_cell(PAGE_W, 5.5, sanitize(text), border=1, fill=True)
        self.ln(3)

    def table_header(self, cols, widths):
        # Page-break guard: header + at least one row (12pt min)
        if self.get_y() + 19 > (297 - 22):
            self.add_page()
        self.set_fill_color(*DARK_NAVY)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*WHITE)
        self.set_x(LEFT)
        for col, w in zip(cols, widths):
            self.cell(w, 7, sanitize(col), border=1, fill=True)
        self.ln()

    def _cell_height(self, text, width, line_h=4.0, pad=1.5):
        """Estimate rendered height of a multi_cell block (doc units)."""
        self.set_font("Helvetica", "", 7.5)
        total_lines = 0
        for para in sanitize(str(text)).split("\n"):
            if not para.strip():
                total_lines += 1
                continue
            line_w = 0
            para_lines = 1
            for word in para.split():
                ww = self.get_string_width(word + " ")
                if line_w + ww > (width - pad * 2) and line_w > 0:
                    para_lines += 1
                    line_w = ww
                else:
                    line_w += ww
            total_lines += para_lines
        return max(total_lines * line_h + pad * 2, 10)

    def table_row(self, cells, widths, fill=False):
        line_h = 4.0
        pad = 1.5
        # Pre-compute row height from all cells so every cell in the row
        # uses the same height -- eliminates overlapping / scattered rows
        row_h = max(self._cell_height(str(c), w, line_h, pad)
                    for c, w in zip(cells, widths))
        # Page-break guard: add page before drawing if row won't fit
        if self.get_y() + row_h > (297 - 22):
            self.add_page()
        y_start = self.get_y()
        x_cur = LEFT
        for cell, w in zip(cells, widths):
            # Background fill (draw as rectangle so height is exact)
            if fill:
                self.set_fill_color(240, 245, 248)
                self.rect(x_cur, y_start, w, row_h, "F")
            # Border rectangle (consistent height for every cell in row)
            self.set_draw_color(170, 170, 170)
            self.set_line_width(0.2)
            self.rect(x_cur, y_start, w, row_h, "D")
            # Text content
            self.set_xy(x_cur + pad, y_start + pad)
            self.set_font("Helvetica", "", 7.5)
            self.set_text_color(*DARK_GREY)
            self.multi_cell(w - pad * 2, line_h, sanitize(str(cell)),
                            border=0, align="L")
            x_cur += w
        # Advance cursor to next row
        self.set_xy(LEFT, y_start + row_h)

    def cover(self):
        self.add_page()
        # Hero block
        self.set_fill_color(*TEAL)
        self.rect(0, 14, 210, 65, "F")
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(*WHITE)
        self.set_xy(12, 24)
        self.multi_cell(186, 9,
                        sanitize("iNHCES LIVE DATA INFRASTRUCTURE GUIDE"),
                        align="C")
        self.set_font("Helvetica", "", 12)
        self.set_xy(12, 46)
        self.multi_cell(186, 7,
                        sanitize("Sources, Pipeline & Automated ML Retraining"),
                        align="C")
        self.set_font("Helvetica", "I", 9)
        self.set_xy(12, 58)
        self.multi_cell(186, 5,
                        sanitize("ABU Zaria Research Team  |  TETFund NRF 2025  |  S2RF Governed"),
                        align="C")
        self.set_font("Helvetica", "", 8)
        self.set_xy(12, 68)
        self.set_text_color(*GOLD)
        self.multi_cell(186, 5,
                        sanitize("S2R Architect: Dr. Bello Abdullahi  |  BAE Consulting Engineers, Abuja"),
                        align="C")

        # Scope note
        self.set_text_color(*DARK_GREY)
        self.set_xy(12, 88)
        self.set_fill_color(*PALE_TEAL)
        self.set_font("Helvetica", "", 9)
        self.multi_cell(186, 6,
                        sanitize(
                            "SCOPE: This document covers Sections 7-12 of the iNHCES Research "
                            "Advisory Framework -- the data sourcing, pipeline, and system "
                            "architecture components. Research methodology (Objectives O1-O6 "
                            "workflow) is covered in: 01_S2RF_Claude_AI_Workflow_Guide_iNHCES.pdf"
                        ),
                        border=1, fill=True)

        # Contents
        self.ln(6)
        self.set_x(LEFT)
        self.set_fill_color(*DARK_NAVY)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*WHITE)
        self.cell(PAGE_W, 7, sanitize("  Contents"), fill=True, ln=True)

        contents = [
            ("7",  "Online Data Sources Registry (Tier 1 APIs, Tier 2 Portals, Tier 3 Scrapers)"),
            ("8",  "Live Data Pipeline & Automated ML Retraining Architecture"),
            ("9",  "Web System Development — Objective 6 (Updated with Pipeline Dashboard)"),
            ("10", "Research Timeline (18-24 Months)"),
            ("11", "Target Journals for Publication"),
            ("12", "Final Key Recommendations"),
        ]
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*DARK_GREY)
        for num, title in contents:
            self.set_x(LEFT + 4)
            self.cell(8, 7, sanitize(f"{num}."))
            self.cell(PAGE_W - 8, 7, sanitize(title), ln=True)

        # Metadata
        self.ln(4)
        self.set_draw_color(*GOLD)
        self.set_line_width(0.6)
        self.line(LEFT, self.get_y(), LEFT + PAGE_W, self.get_y())
        self.ln(3)
        for label, val in [
            ("Document:",     "04_iNHCES_Live_Data_Infrastructure_Guide.pdf"),
            ("Companion:",    "01_S2RF_Claude_AI_Workflow_Guide_iNHCES.pdf (O1-O6 methodology)"),
            ("Preamble:",     "00_S2RF_Governing_Preamble_iNHCES.pdf (S2RF ethics & rules)"),
            ("Grant:",        "TETFund National Research Fund (NRF) 2025"),
            ("S2R Architect:","Dr. Bello Abdullahi  |  BAE Consulting Engineers, Abuja"),
            ("Date:",         date.today().strftime("%d %B %Y")),
        ]:
            self.set_x(LEFT)
            self.set_font("Helvetica", "B", 8.5)
            self.set_text_color(*DARK_NAVY)
            self.cell(38, 6, sanitize(label))
            self.set_font("Helvetica", "", 8.5)
            self.set_text_color(*DARK_GREY)
            self.cell(PAGE_W - 38, 6, sanitize(val), ln=True)


# ── Section builders ──────────────────────────────────────────────────────────

def section_7(pdf):
    pdf.add_page()
    pdf.section_title("7  Online Data Sources Registry")
    pdf.body(
        "This section catalogues every online data source that feeds the iNHCES ML models. "
        "Sources are organised by tier: Tier 1 (official APIs -- highest reliability), "
        "Tier 2 (institutional web portals -- requires scraping/download), and Tier 3 "
        "(market intelligence -- requires web scraping). All are integrated into the "
        "automated data pipeline described in Section 8."
    )

    pdf.sub_heading("7.1  Tier 1 -- Official APIs with Programmatic Access")
    cols = ["Source / API", "Data Provided", "Frequency", "Access & Endpoint"]
    widths = [42, 60, 22, 62]
    pdf.table_header(cols, widths)
    tier1 = [
        ("World Bank Indicators API\n(api.worldbank.org/v2)",
         "Nigeria GDP, inflation, interest rate, household income, PPP indices (16,000+ indicators; Nigeria code: NGA)",
         "Annual / Quarterly",
         "Free, no key. Python: wbdata, world_bank_data. e.g. FP.CPI.TOTL.ZG (inflation)"),
        ("CBN Statistics Database\n(statistics.cbn.gov.ng)",
         "Exchange rates (NGN/USD/EUR/GBP), money supply M1/M2/M3, lending rates, MPR, BOP data",
         "Daily / Monthly",
         "Free portal -- Excel/CSV download. Scrape or use CBN Data API. Endpoint: statistics.cbn.gov.ng/shop"),
        ("CBN Exchange Rates Portal\n(cbn.gov.ng/rates)",
         "Daily official Naira exchange rates (NFEM rate), all major currencies",
         "Daily",
         "Free web page -- scrape ExchRateByCurrency.html. Parse HTML table into time-series DB"),
        ("CBN Inflation Portal\n(cbn.gov.ng/rates/inflrates)",
         "Monthly headline inflation, core inflation, food inflation",
         "Monthly",
         "Free web page -- scrape inflrates.html and parse tabular data"),
        ("EIA API\n(api.eia.gov)",
         "Brent crude spot price (daily), WTI crude price, natural gas prices",
         "Daily",
         "Free key registration at eia.gov/opendata. Python: requests + EIA_API_KEY env var"),
        ("FRED / St. Louis Fed\n(fred.stlouisfed.org)",
         "NGN/USD, NGN/EUR, NGN/GBP exchange rates; global lending rates; CPI indices",
         "Daily / Monthly",
         "Free API key. Python: fredapi package. Series: DNGNUS (NGN/USD daily)"),
        ("Open Exchange Rates\n(openexchangerates.org)",
         "Live & historical NGN/USD, NGN/EUR, NGN/GBP with minute-level granularity",
         "Real-time",
         "Free tier (1,000 req/mo); paid from US$12/mo. Python requests or openexchangerates package"),
        ("Trading Economics API\n(tradingeconomics.com)",
         "Nigeria MPR, lending rates, government bond yields, construction PMI",
         "Daily / Monthly",
         "Free tier limited; paid from US$75/mo. Use for rates not on FRED/CBN"),
    ]
    for i, row in enumerate(tier1):
        pdf.table_row(row, widths, fill=(i % 2 == 1))

    pdf.ln(4)
    pdf.sub_heading("7.2  Tier 2 -- Institutional Portals (Scheduled Download / Scraping)")
    cols2 = ["Source / Portal", "Data Provided", "Frequency", "Access Method"]
    pdf.table_header(cols2, widths)
    tier2 = [
        ("NBS e-Library\n(nigerianstat.gov.ng/elibrary)",
         "Housing & Construction Statistics; Sectoral GDP (Real Estate & Construction); CPI Housing sub-index; Banking & Finance Statistics",
         "Quarterly / Annual",
         "Free PDF/Excel download. Automate with scheduled Selenium scraper -- monitor /elibrary/read/12 for new publications"),
        ("NBS Open Data Portal\n(open.africa/organization/nigeria-nbs)",
         "Population estimates, food prices, PMS price by state 2016-present, demographic statistics",
         "Varies",
         "Free CSV/JSON via CKAN API. Use: open.africa/api/3/action/datastore_search?resource_id=..."),
        ("NBS Microdata Portal\n(nigerianstat.gov.ng/nada)",
         "Nigeria Forced Labour Survey housing data (287 housing variables); Living Standards surveys -- 16,000+ household records with housing cost data",
         "Survey cycles",
         "Free registration required. Download DDI/CSV via NADA API. Critical for household-level housing cost data"),
        ("FMBN\n(fmbn.gov.ng)",
         "Mortgage loan data, NHF (National Housing Fund) contribution data, housing delivery statistics",
         "Quarterly",
         "Download annual reports and statistical tables. Contact FMBN Data Unit directly for machine-readable data"),
        ("FHA / State Housing Corps",
         "Completed housing project costs, specifications, location, completion dates",
         "Per project",
         "MoU required. Begin negotiations in Month 1 -- this is the highest-value real training dataset"),
        ("NGX / NSE\n(ngxgroup.com)",
         "Listed construction company financials; building materials company stock data; Lafarge, Dangote Cement",
         "Quarterly",
         "Free historical data download. Python: yfinance for NGX-listed tickers"),
        ("NIQS Schedule of Rates",
         "Bill of Quantities unit rates for all building elements (labour, materials, plant) by geopolitical zone",
         "Quarterly",
         "NIQS membership publication. Research MoU required. Most critical primary data for NHCES model training"),
        ("PropertyPro / Private Property\n(propertypro.ng)",
         "Residential property listing prices (NGN/sqm) by state, LGA, and neighbourhood",
         "Weekly",
         "Web scraping (BeautifulSoup + Scrapy). Listings include floor area + asking price -- compute NGN/sqm"),
    ]
    for i, row in enumerate(tier2):
        pdf.table_row(row, widths, fill=(i % 2 == 1))

    pdf.ln(4)
    pdf.add_page()
    pdf.sub_heading("7.3  Tier 3 -- Market Intelligence (Web Scraping)")
    cols3 = ["Source / Website", "Data Provided", "Frequency", "Scraping Approach"]
    widths3 = [40, 60, 22, 64]
    pdf.table_header(cols3, widths3)
    tier3 = [
        ("BusinessDay NG\n(businessday.ng)",
         "Construction material price reports: cement, iron rod, sand, gravel -- Lagos and Abuja market surveys",
         "Weekly",
         "Python BeautifulSoup/Scrapy. Search for 'cement price', 'iron rod price'. Parse article body into structured JSON"),
        ("Titanium Building Solutions\n(titaniumbuildingsolutions.com)",
         "Current and forecast cement price by brand (Dangote, BUA, Lafarge) and region",
         "Monthly",
         "Scrape price guide pages. Extract price ranges by brand and location. Regularly updated"),
        ("Legit.ng / Okay.ng",
         "Consumer-facing cement bag prices, iron rod per length, tiles prices -- geographically distributed",
         "Weekly",
         "Parse price articles with regex + NLP to extract price, brand, location, date"),
        ("Jiji.ng Building Materials\n(jiji.ng/building-materials)",
         "Real-time classified ads for cement, iron rods, sand, gravel, roofing sheets -- actual transaction price signals by state",
         "Daily",
         "CKAN-style endpoint scraping. Extract price, category, location, date posted. Use as market signal"),
        ("Nairametrics\n(nairametrics.com)",
         "FX rates (parallel/black market), CBN policy commentary, construction sector analysis",
         "Daily",
         "RSS feed or web scraping. Use for parallel market FX as complement to official CBN rates"),
        ("NNPC / NMDPRA\n(nnpcgroup.com)",
         "PMS (petrol) pump price by state -- directly impacts construction logistics and material costs",
         "Monthly",
         "Download price bulletin PDFs. Parse with pdfplumber. Also available via NBS open data"),
    ]
    for i, row in enumerate(tier3):
        pdf.table_row(row, widths3, fill=(i % 2 == 1))

    pdf.ln(4)
    pdf.sub_heading("7.4  Feature-to-Source Mapping (Database Table Targets)")
    pdf.body(
        "The table below maps each ML feature variable to its data source(s) and the target "
        "Supabase table. This is the canonical reference for pipeline DAG configuration."
    )
    cols4 = ["Feature / Variable", "Primary Source(s)", "Cadence", "DB Table"]
    widths4 = [50, 62, 22, 52]
    pdf.table_header(cols4, widths4)
    mapping = [
        ("Exchange rate (NGN/USD, NGN/EUR, NGN/GBP)", "CBN Exchange Rates Portal + FRED + Open Exchange Rates", "Daily", "macro_fx"),
        ("Inflation / CPI (headline + housing sub-index)", "CBN Inflation Portal + NBS e-Library", "Monthly", "macro_cpi"),
        ("Lending rate / MPR", "CBN Statistics DB + Trading Economics", "Monthly", "macro_interest"),
        ("Crude oil price (Brent)", "EIA API", "Daily / Monthly avg", "macro_oil"),
        ("GDP growth / Real Estate sector GDP", "World Bank API + NBS e-Library", "Quarterly", "macro_gdp"),
        ("Cement price by brand & region (NGN/bag)", "BusinessDay scraper + Titanium scraper", "Weekly", "material_cement"),
        ("Iron rod price by diameter & region (NGN/length)", "BusinessDay scraper + Jiji.ng scraper", "Weekly", "material_steel"),
        ("PMS (petrol) price by state (NGN/litre)", "NNPC/NMDPRA + NBS open data", "Monthly", "material_pms"),
        ("NIQS unit rates (labour, materials, plant)", "NIQS Quarterly Schedule of Rates", "Quarterly", "unit_rates"),
        ("Housing project completed cost + attributes", "FHA, State Housing Corps, NIQS firms (MoU)", "Per project", "projects"),
        ("Property listing prices (NGN/sqm by zone)", "PropertyPro + Private Property scrapers", "Weekly", "market_prices"),
    ]
    for i, row in enumerate(mapping):
        pdf.table_row(row, widths4, fill=(i % 2 == 1))

    pdf.warn_box(
        "DATA ACCESS NOTE: NIQS Schedule of Rates and FHA project records are the highest-value "
        "training data and require MoU negotiations. Begin institutional outreach in Month 1 -- "
        "these datasets take the longest to access. Without real NIQS rates and FHA project data, "
        "all ML model outputs carry RED-banner (synthetic) status until replaced."
    )


def section_8(pdf):
    pdf.add_page()
    pdf.section_title("8  Live Data Pipeline & Automated ML Retraining Architecture")
    pdf.body(
        "This section defines the full MLOps architecture that keeps iNHCES current. The pipeline "
        "is built on Apache Airflow (orchestration) + MLflow (experiment tracking and model "
        "registry) + Supabase PostgreSQL (data store) -- all deployed on Railway, consistent "
        "with the existing iNHCES infrastructure."
    )

    pdf.sub_heading("8.1  Pipeline Architecture Overview")
    pdf.body(
        "The iNHCES data pipeline is a five-stage continuous loop: "
        "Ingest → Validate → Transform → Store → Retrain. "
        "Each stage is implemented as an Apache Airflow DAG, scheduled independently "
        "based on source cadence."
    )

    cols = ["Stage", "Name", "Trigger", "Key Actions"]
    widths = [12, 20, 36, 118]
    pdf.table_header(cols, widths)
    stages = [
        ("1", "Ingest", "Scheduled (varies by source)",
         "Pull from APIs and scrapers. Convert raw responses to JSON. Log ingestion metadata (source, timestamp, record count, status)"),
        ("2", "Validate", "After each Ingest run",
         "Check for nulls, out-of-range values, anomalous spikes (>3σ from rolling mean). Flag records as PASS / WARN / FAIL. Alert team on FAIL"),
        ("3", "Transform", "After Validate PASS",
         "Feature engineering: compute derived ratios, rolling averages, lagged features (1, 3, 6-month lags), geopolitical zone encodings"),
        ("4", "Store", "After Transform",
         "Upsert validated features into Supabase PostgreSQL. Update feature_store table. Version-stamp each batch. Maintain full audit trail"),
        ("5", "Retrain", "Weekly (or on drift alert)",
         "Pull latest feature_store snapshot. Retrain all model family. Evaluate on hold-out test set. Register best model in MLflow. Auto-promote if MAPE improves"),
    ]
    for i, row in enumerate(stages):
        pdf.table_row(row, widths, fill=(i % 2 == 1))

    pdf.ln(3)
    pdf.sub_heading("8.2  Airflow DAG Schedule")
    cols2 = ["DAG Name", "Schedule", "Source(s)", "DB Target"]
    widths2 = [52, 28, 60, 46]
    pdf.table_header(cols2, widths2)
    dags = [
        ("nhces_daily_fx_oil", "Daily @ 06:00 WAT", "CBN FX Portal + EIA API + FRED", "macro_fx, macro_oil"),
        ("nhces_daily_property", "Daily @ 08:00 WAT", "PropertyPro + Private Property scrapers", "market_prices"),
        ("nhces_weekly_materials", "Weekly (Monday)", "BusinessDay + Titanium + Jiji.ng scrapers", "material_cement, material_steel"),
        ("nhces_monthly_macro", "Monthly (1st day)", "CBN inflation, CBN stats DB, NNPC PMS, Trading Economics", "macro_cpi, macro_interest, material_pms"),
        ("nhces_quarterly_niqs", "Quarterly (manual trigger)", "NIQS Schedule of Rates (manual upload)", "unit_rates"),
        ("nhces_quarterly_nbs", "Quarterly", "NBS e-Library (PDF parser + data extractor)", "macro_gdp (Real Estate sector)"),
        ("nhces_worldbank_annual", "Annual (January)", "World Bank API (wbdata package)", "macro_gdp (annual GDP, household income)"),
        ("nhces_retrain_weekly", "Weekly (Sunday)", "feature_store table (Supabase)", "ml_models (MLflow registry)"),
        ("nhces_drift_monitor", "Daily @ 18:00 WAT", "Prediction logs + actual project costs", "audit_log (drift alert if PSI > 0.2)"),
    ]
    for i, row in enumerate(dags):
        pdf.table_row(row, widths2, fill=(i % 2 == 1))

    pdf.ln(3)
    pdf.sub_heading("8.3  Sample Airflow DAG -- Daily FX and Oil Ingest")
    pdf.body(
        "The following Python snippet illustrates the pattern used for all Tier 1 API DAGs. "
        "The same structure applies to all nhces_daily_* and nhces_weekly_* DAGs."
    )
    pdf.set_font("Courier", "", 7.5)
    pdf.set_text_color(*DARK_NAVY)
    pdf.set_fill_color(*PALE_TEAL)
    pdf.set_x(LEFT)
    code = (
        "from airflow.decorators import dag, task\n"
        "from datetime import datetime\n"
        "import requests, pandas as pd\n\n"
        "@dag(schedule='0 6 * * *', start_date=datetime(2025,1,1), catchup=False)\n"
        "def nhces_daily_fx_oil():\n"
        "    @task\n"
        "    def fetch_cbn_fx():\n"
        "        url = 'https://www.cbn.gov.ng/rates/ExchRateByCurrency.html'\n"
        "        df = pd.read_html(url)[0]  # parse HTML table directly\n"
        "        df['fetch_date'] = datetime.today().date()\n"
        "        return df.to_dict('records')\n\n"
        "    @task\n"
        "    def fetch_eia_brent():\n"
        "        r = requests.get('https://api.eia.gov/v2/petroleum/pri/spt/data',\n"
        "            params={'api_key': EIA_KEY, 'frequency':'daily',\n"
        "                    'data[0]':'value', 'sort[0][column]':'period'})\n"
        "        return r.json()['response']['data']\n\n"
        "    @task\n"
        "    def validate_and_store(fx_data, oil_data):\n"
        "        # Validate: check nulls + >3-sigma spikes vs rolling mean\n"
        "        # Upsert to Supabase macro_fx and macro_oil tables\n"
        "        pass\n\n"
        "    fx = fetch_cbn_fx()\n"
        "    oil = fetch_eia_brent()\n"
        "    validate_and_store(fx, oil)\n\n"
        "nhces_daily_fx_oil()"
    )
    pdf.multi_cell(PAGE_W, 4.5, sanitize(code), border=1, fill=True)
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(3)

    pdf.sub_heading("8.4  MLflow Model Registry and Automated Deployment")
    cols3 = ["MLflow Concept", "Role in iNHCES"]
    widths3 = [48, 138]
    pdf.table_header(cols3, widths3)
    mlflow_rows = [
        ("Experiment Tracking",
         "Log every training run: hyperparameters, MAE, RMSE, MAPE, R², training data snapshot date"),
        ("Model Registry",
         "Store all model versions with stage labels: Staging → Production → Archived"),
        ("Model Versioning",
         "Every weekly retrain produces a new versioned model. Old versions retained for rollback"),
        ("Automated Promotion",
         "If new model MAPE ≤ current production MAPE + 1pp, auto-promote to Production and update FastAPI serving endpoint"),
        ("Model Serving",
         "FastAPI loads model from MLflow Registry at startup. Reload endpoint triggered on new production registration"),
        ("Drift Detection",
         "Compare prediction distribution (PSI metric) weekly. If PSI > 0.2, trigger emergency retrain DAG"),
    ]
    for i, row in enumerate(mlflow_rows):
        pdf.table_row(row, widths3, fill=(i % 2 == 1))

    pdf.ln(3)
    pdf.sub_heading("8.5  Automated Retraining -- Champion-Challenger Decision Logic")
    pdf.body(
        "The weekly retrain DAG follows a champion-challenger pattern:"
    )
    steps = [
        "Pull latest feature_store snapshot from Supabase (all features, all valid records)",
        "Split: 80% train / 10% validation / 10% hold-out test (stratified by geopolitical zone and year)",
        "Retrain all model family (MLR, RF, XGBoost, LightGBM, DNN, Stacking ensemble) with Optuna hyperparameter tuning",
        "Evaluate all models on hold-out test set. Select best model (lowest MAPE)",
        "Compare challenger MAPE against current production model MAPE on same test set",
        "If challenger MAPE < production MAPE + 1pp: promote challenger to Production in MLflow Registry",
        "If challenger is worse: retain current production model. Log result and alert team",
        "FastAPI serving layer picks up new production model automatically at next request",
    ]
    for i, step in enumerate(steps, 1):
        pdf.set_x(LEFT + 4)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*DARK_GREY)
        pdf.cell(6, LINE_H, sanitize(f"{i}."))
        pdf.multi_cell(PAGE_W - 6, LINE_H, sanitize(step))

    pdf.ln(3)
    pdf.sub_heading("8.6  Pipeline Infrastructure Stack")
    cols4 = ["Component", "Tool / Service", "Role"]
    widths4 = [40, 50, 96]
    pdf.table_header(cols4, widths4)
    infra = [
        ("Orchestration", "Apache Airflow (Railway)", "Schedule, monitor, and retry all DAGs"),
        ("Model Registry", "MLflow Tracking Server (Railway)", "Experiment logging, model versioning, promotion"),
        ("Feature Store", "Supabase PostgreSQL + TimescaleDB", "Time-series feature storage with efficient range queries"),
        ("Scraping Engine", "Python Scrapy + BeautifulSoup + Selenium", "Automated Tier 2 and Tier 3 data collection"),
        ("Data Validation", "Great Expectations library", "Schema validation, null checks, statistical anomaly detection"),
        ("Alert System", "Airflow email alerts + Slack webhook", "Notify team of pipeline failures, drift alerts, retrain outcomes"),
        ("Secrets Management", "Railway environment variables / .env", "Store API keys (EIA, Trading Economics, Open Exchange Rates)"),
        ("CI/CD Integration", "GitHub Actions (existing pipeline)", "Auto-deploy updated DAGs and FastAPI model server on push"),
    ]
    for i, row in enumerate(infra):
        pdf.table_row(row, widths4, fill=(i % 2 == 1))

    pdf.info_box(
        "RESEARCH NOVELTY: The iNHCES data pipeline is, to the authors' knowledge, the first "
        "fully automated, continuously-updating construction cost estimation data infrastructure "
        "designed specifically for the Nigerian built environment. This pipeline architecture is "
        "itself a publishable contribution -- suitable for Automation in Construction or "
        "Scientific Data (Springer Nature) as a Data Paper."
    )


def section_9(pdf):
    pdf.add_page()
    pdf.section_title("9  Web System Development -- Objective 6 (Updated)")
    pdf.body(
        "The iNHCES web system includes a Data Pipeline Dashboard module in addition to the "
        "original six functional modules. The dashboard is admin-facing and shows pipeline "
        "health, last successful DAG run times, current production model version and MAPE, "
        "and a manual retrain trigger button."
    )
    cols = ["Module", "Description", "Status"]
    widths = [48, 110, 28]
    pdf.table_header(cols, widths)
    modules = [
        ("1. Project Input", "Building parameters, location, typology, structural system", "Original"),
        ("2. Macroeconomic Context", "Auto-fetches current macro snapshot from live feature_store", "Updated -- live"),
        ("3. ML Estimation Engine", "Runs champion ensemble model; returns point estimate + 90% confidence interval + 5-year temporal projection", "Updated"),
        ("4. Sensitivity Analysis", "SHAP-powered -- shows top 10 cost drivers for that specific estimate", "Original"),
        ("5. Report Generation", "PDF output for QS professional use, includes model version + data freshness date + DataSourceBadge", "Updated"),
        ("6. Admin / Data Feed", "Manual project data entry by NBS/NIQS; triggers pipeline validation run", "Original"),
        ("7. Pipeline Dashboard", "DAG health, last run times, production model MAPE, drift alerts, manual retrain trigger (researcher role)", "NEW"),
    ]
    for i, row in enumerate(modules):
        pdf.table_row(row, widths, fill=(i % 2 == 1))

    pdf.ln(3)
    pdf.body(
        "The DataSourceBadge component (GREEN/AMBER/RED) is rendered on every macro variable "
        "displayed in the UI, propagated from the data_source_level column in the Supabase "
        "database through the FastAPI response schema to the Next.js TypeScript interface. "
        "This ensures end users always know the provenance of every data point driving an estimate."
    )


def section_10(pdf):
    pdf.add_page()
    pdf.section_title("10  Research Timeline (18-24 Months)")
    cols = ["Phase", "Key Activities", "Duration"]
    widths = [48, 120, 18]
    pdf.table_header(cols, widths)
    timeline = [
        ("Phase 1 -- SLR", "PRISMA SLR, gap analysis, publish P1 review paper", "Months 1-4"),
        ("Phase 2 -- Macro Analysis", "Data source MoUs, pipeline prototype for Tier 1 APIs, econometric analysis (VAR/VECM/SHAP)", "Months 3-7"),
        ("Phase 3 -- Requirements", "Delphi survey (incl. pipeline admin requirements), SRS document to IEEE 830 standard", "Months 5-9"),
        ("Phase 4 -- Conceptual Modelling", "Full architecture design incl. data pipeline and MLOps layer; ERD, DFD, UML", "Months 8-11"),
        ("Phase 5a -- Data Pipeline Build", "Build all 9 Airflow DAGs; connect Tier 1 APIs; test Tier 2/3 scrapers; populate feature_store", "Months 9-13"),
        ("Phase 5b -- ML Development", "Train initial models on historical + pipeline data; SHAP analysis; benchmarking all model families", "Months 11-16"),
        ("Phase 5c -- MLflow Integration", "Set up MLflow registry; implement champion-challenger retraining loop; PSI drift monitoring", "Months 14-17"),
        ("Phase 6 -- System Build", "FastAPI backend (17 routes) + Next.js frontend (8 pages) + Pipeline Dashboard + PDF reports + UAT", "Months 15-22"),
        ("Dissemination", "Journal papers (P1-P9): Automation in Construction, JCEM, Expert Systems, Scientific Data, Habitat International", "Throughout"),
    ]
    for i, row in enumerate(timeline):
        pdf.table_row(row, widths, fill=(i % 2 == 1))

    pdf.ln(3)
    pdf.info_box(
        "S2RF TIMELINE NOTE: The S2RF simulation-first approach compresses Phases 1-6 by "
        "allowing the research team to produce complete pipeline scaffolding (scripts, schemas, "
        "DAGs, API routes, frontend pages) before real data is collected. Real data replaces "
        "synthetic (RED) outputs phase by phase as MoUs are signed and fieldwork proceeds. "
        "The total clock time is not compressed -- but the dependency chain is broken."
    )


def section_11(pdf):
    pdf.add_page()
    pdf.section_title("11  Target Journals for Publication")
    cols = ["Priority", "Journal", "Publisher / Ranking", "Best Paper Topic"]
    widths = [14, 56, 50, 66]
    pdf.table_header(cols, widths)
    journals = [
        ("1st", "Automation in Construction", "Elsevier Q1 (IF ~9.6)", "Full iNHCES system + pipeline (P7)"),
        ("2nd", "Journal of Construction Engineering & Management", "ASCE Q1", "ML model benchmarking (P5)"),
        ("3rd", "Construction Management and Economics", "Taylor & Francis Q1", "Macroeconomic variable analysis (P3)"),
        ("4th", "Expert Systems with Applications", "Elsevier", "MLOps architecture + champion-challenger (P6)"),
        ("5th", "Scientific Data", "Springer Nature", "Automated Nigerian data pipeline -- Data Paper (P4)"),
        ("6th", "Habitat International", "Elsevier", "Nigerian housing policy implications (P8)"),
        ("7th", "Engineering, Construction & Architectural Management", "Emerald", "PRISMA SLR (P1) or Delphi requirements (P2)"),
        ("8th", "Computers & Education / IETI", "Various", "S2RF AI research simulation framework (P9)"),
    ]
    for i, row in enumerate(journals):
        pdf.table_row(row, widths, fill=(i % 2 == 1))

    pdf.ln(3)
    pdf.body(
        "All paper assignments above are indicative. Final journal selection must be confirmed "
        "by the research team based on scope fit, current impact factors, and submission "
        "guidelines at time of writing. Verify all journal details in Scopus / Web of Science "
        "before submission. No AI-generated citation should be submitted without independent "
        "verification -- this is a S2RF obligation (Human Validation Gate)."
    )


def section_12(pdf):
    pdf.add_page()
    pdf.section_title("12  Final Key Recommendations")

    recs = [
        ("Recommendation 1: Treat Nigerian Data Scarcity as a Contribution",
         "Your data curation methodology -- combining official APIs, institutional MoUs, and "
         "automated scraping into a unified Nigerian construction cost data infrastructure -- is "
         "itself a research contribution no prior study has achieved at this scale. Document the "
         "pipeline as a standalone Data Paper (Scientific Data or Data in Brief) and cite it "
         "in all papers that use the resulting dataset."),
        ("Recommendation 2: Build Explainability (SHAP) from Day One",
         "Professional QS adoption requires transparency. Design SHAP waterfall charts and "
         "feature importance plots into the iNHCES UI from the first prototype. A system that "
         "explains its reasoning will be used; a black box will be ignored. SHAP also satisfies "
         "reviewer expectations in high-impact journals for construction ML papers."),
        ("Recommendation 3: Design for National Scalability",
         "Structure state-level sub-models (Lagos, Abuja, Kano, Katsina have different cost "
         "structures). Each state model trains on local data but contributes to the national "
         "ensemble. The pipeline supports this natively via geopolitical zone partitioning "
         "already embedded in the Supabase schema."),
        ("Recommendation 4: Formalise Data Sharing Agreements Early",
         "Begin MoU discussions with NIQS, FHA, and state housing corporations in Month 1 -- "
         "not Month 9. NIQS Schedule of Rates and FHA project records are your highest-value "
         "training data and take the longest to access. Pipeline infrastructure is worthless "
         "without the institutional data to flow through it."),
        ("Recommendation 5: Publish the Pipeline as a Standalone Contribution",
         "The automated data pipeline connecting CBN, NBS, EIA, World Bank, NGX, and web "
         "scrapers into a unified Nigerian construction cost intelligence system is -- to the "
         "authors' knowledge -- unprecedented in the literature. Publish it as a Data Paper in "
         "Scientific Data (Springer Nature) or Data in Brief (Elsevier) as a citable dataset."),
        ("Recommendation 6: Plan for Post-TETFund Sustainability",
         "Design iNHCES from day one for institutional handover to NBS or NIQS after the grant "
         "period. This means: fully documented DAGs, a system administrator training programme, "
         "and a lightweight maintenance mode where only monthly DAGs run (low server cost). "
         "A system that outlives its grant is a system that achieved its purpose."),
        ("Recommendation 7: Apply S2RF to All Future Outputs",
         "Every deliverable produced under TETFund NRF 2025 must carry a DATA SOURCE banner "
         "(GREEN/AMBER/RED) as required by the Governing Preamble "
         "(00_S2RF_Governing_Preamble_iNHCES.pdf). RED-banner content must be replaced with "
         "real data before any publication, grant report, or policy brief. Human Validation "
         "Gate sign-off is required before any output advances to the next pipeline stage."),
    ]

    for title, body in recs:
        pdf.sub_heading(title)
        pdf.body(body)

    pdf.info_box(
        "This document is governed by the Simulation to Research Framework (S2RF). "
        "S2R Architect: Dr. Bello Abdullahi | BAE Consulting Engineers, Abuja. "
        "Companion documents: 00_S2RF_Governing_Preamble_iNHCES.pdf (ethics & rules) | "
        "01_S2RF_Claude_AI_Workflow_Guide_iNHCES.pdf (O1-O6 methodology workflow). "
        f"Generated: {date.today().strftime('%d %B %Y')}."
    )


# ── Main ──────────────────────────────────────────────────────────────────────
def build():
    pdf = GuidePDF()
    pdf.set_author("ABU Zaria Research Team / Dr. Bello Abdullahi")
    pdf.set_title("iNHCES Live Data Infrastructure Guide: Sources, Pipeline & Automated ML Retraining")

    pdf.cover()

    _ds_page(pdf, "amber",
        "DATA SOURCE: AMBER -- AI-AUTHORED TECHNICAL REFERENCE DOCUMENT",
        (
            "WHAT IS REAL:\n"
            "  * All API endpoints, scraping targets, and data source URLs are real and verified "
            "as of April 2026.\n"
            "  * The Airflow DAG architecture, MLflow registry design, and Supabase schema "
            "column references reflect the actual iNHCES system built in O6.\n"
            "  * The NIQS / FHA MoU requirement and data scarcity analysis are real constraints.\n\n"
            "WHAT REQUIRES VERIFICATION:\n"
            "  * API pricing tiers and free-tier limits may have changed -- verify at source before use.\n"
            "  * CBN web portal HTML structure may change -- scraper code requires maintenance.\n"
            "  * NIQS Schedule of Rates access terms -- confirm with NIQS directly.\n\n"
            "RED-BANNER ITEMS (must be replaced before publication):\n"
            "  * All ML model performance metrics (MAPE, R²) reflect synthetic training data.\n"
            "  * Replace with real metrics once NIQS data and FHA project records are obtained.\n"
            "  * Research timeline durations are estimates -- update with actual project dates."
        )
    )

    section_7(pdf)
    section_8(pdf)
    section_9(pdf)
    section_10(pdf)
    section_11(pdf)
    section_12(pdf)

    pdf.output(OUTPUT_PATH)
    print(f"[OK] 04_iNHCES_Live_Data_Infrastructure_Guide.pdf  saved -> {OUTPUT_PATH}")


if __name__ == "__main__":
    build()
