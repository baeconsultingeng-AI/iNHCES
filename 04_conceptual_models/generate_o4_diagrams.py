"""
iNHCES O4 — Conceptual Diagrams Generator
Produces six publication-quality PNG diagrams + a consolidated PDF:
  1. System Architecture (7-layer stack)
  2. Entity-Relationship Diagram (ERD)
  3. DFD Level 0 — Context Diagram
  4. DFD Level 1 — Process Decomposition
  5. Airflow Pipeline Flow (9 DAGs)
  6. User Journey Map

Output: 04_conceptual_models/diagrams/*.png
        04_conceptual_models/O4_00_Conceptual_Diagrams.pdf

TETFund NRF 2025 | Department of Quantity Surveying, ABU Zaria
"""

import os, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from matplotlib.lines import Line2D
from datetime import date

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
_DIAG = os.path.join(_HERE, 'diagrams')
os.makedirs(_DIAG, exist_ok=True)

sys.path.insert(0, os.path.join(_ROOT, '01_literature_review'))
from generate_o1_pdfs import (
    DocPDF, sanitize, _ds_page,
    DARK_NAVY, GOLD, LIGHT_BLUE, WHITE, DARK_GREY, MID_GREY,
    PAGE_W, LEFT,
)

# ── Colour palette ─────────────────────────────────────────────────────────────
C_NAVY   = '#0F2850'
C_GOLD   = '#B48C1E'
C_BLUE   = '#1A5276'
C_TEAL   = '#148F77'
C_GREEN  = '#1E8449'
C_PURPLE = '#6C3483'
C_ORANGE = '#D35400'
C_RED    = '#922B21'
C_LGREY  = '#ECF0F1'
C_MGREY  = '#95A5A6'
C_WHITE  = '#FFFFFF'

DPI = 150


# ══════════════════════════════════════════════════════════════════════════════
# DIAGRAM 1 — SYSTEM ARCHITECTURE (7-layer stack)
# ══════════════════════════════════════════════════════════════════════════════
def diag_architecture():
    fig, ax = plt.subplots(figsize=(12, 9))
    ax.set_xlim(0, 12); ax.set_ylim(0, 9)
    ax.axis('off')
    fig.patch.set_facecolor(C_LGREY)

    # Title
    ax.text(6, 8.65, 'iNHCES System Architecture — Seven-Layer Design',
            ha='center', va='center', fontsize=14, fontweight='bold', color=C_NAVY)
    ax.text(6, 8.35, 'TETFund NRF 2025 | ABU Zaria | Dept. of Quantity Surveying',
            ha='center', va='center', fontsize=9, color=C_MGREY)

    layers = [
        # (y_bottom, height, colour, label, sublabel, component_text)
        (7.50, 0.55, '#D5E8D4', 'LAYER 1 — USER', '#00AA00',
         'QS Professional  |  Researcher / PI  |  System Admin', '#006600'),
        (6.70, 0.65, '#DAE8FC', 'LAYER 2 — PRESENTATION  (Vercel CDN)', '#0066CC',
         'index.html  (Cost Estimator)      dashboard.html  (Pipeline Monitor)      app.js / styles.css', '#0044AA'),
        (5.80, 0.75, '#DAEAFF', 'LAYER 3 — API  (FastAPI on Railway)', '#004499',
         'POST /estimate   GET /macro   CRUD /projects   POST /reports   GET /pipeline   JWT Auth', '#002277'),
        (4.90, 0.75, '#E1D5E7', 'LAYER 4 — ML  (MLflow on Railway)', '#6C3483',
         'Champion Model (Stacking Ensemble)   Model Registry   Experiment Tracker   Challenger Models', '#4A235A'),
        (3.80, 0.95, '#FFF2CC', 'LAYER 5 — DATA  (Supabase PostgreSQL)', '#B8860B',
         'macro_fx  macro_cpi  macro_gdp  macro_interest  macro_oil\nmaterial_cement  material_steel  material_pms\nunit_rates  market_prices  projects  predictions  reports  ml_models  users  audit_log', '#7D6008'),
        (2.90, 0.75, '#F8CECC', 'LAYER 6 — STORAGE  (Cloudflare R2)', '#C0392B',
         'PDF Reports  (per-project)      Model Artifacts  (.pkl)      Training Datasets  (versioned CSVs)', '#922B21'),
        (1.70, 1.05, '#FFE6CC', 'LAYER 7 — PIPELINE  (Apache Airflow on Railway)', '#D35400',
         'nhces_daily_fx_oil   nhces_weekly_materials   nhces_weekly_property\nnhces_monthly_macro   nhces_quarterly_niqs   nhces_worldbank_annual\nnhces_retrain_weekly   nhces_drift_monitor', '#A04000'),
    ]

    for (yb, h, fc, lbl, lc, sub, sc) in layers:
        rect = FancyBboxPatch((0.3, yb), 11.4, h,
                               boxstyle='round,pad=0.05', linewidth=1.5,
                               edgecolor=lc, facecolor=fc)
        ax.add_patch(rect)
        ax.text(0.65, yb + h - 0.17, lbl,
                ha='left', va='center', fontsize=8.5, fontweight='bold', color=lc)
        ax.text(6.0, yb + h/2 - 0.05, sub,
                ha='center', va='center', fontsize=7.5, color=sc,
                multialignment='center')

    # Arrows between layers
    arrow_props = dict(arrowstyle='->', color=C_MGREY, lw=1.5)
    for y in [7.50, 6.70, 5.80, 4.90, 3.80, 2.90]:
        ax.annotate('', xy=(6, y), xytext=(6, y - 0.04),
                    arrowprops=dict(arrowstyle='->', color=C_MGREY, lw=1.5,
                                    connectionstyle='arc3,rad=0'))

    # External sources box (right side)
    ext_rect = FancyBboxPatch((9.6, 1.70), 2.1, 5.85,
                               boxstyle='round,pad=0.05', linewidth=1.5,
                               edgecolor=C_TEAL, facecolor='#D1F2EB')
    ax.add_patch(ext_rect)
    ax.text(10.65, 7.42, 'EXTERNAL\nDATA SOURCES', ha='center', va='center',
            fontsize=8, fontweight='bold', color=C_TEAL)
    srcs = ['World Bank API', 'EIA API (Brent)', 'FRED / CBN (FX)',
            'PropertyPro', 'BusinessDay', 'NNPC / NMDPRA', 'NIQS (manual)']
    for i, s in enumerate(srcs):
        ax.text(10.65, 6.85 - i * 0.55, s, ha='center', va='center',
                fontsize=7.5, color=C_TEAL)

    # Arrow from external to pipeline
    ax.annotate('', xy=(11.7, 2.35), xytext=(11.7, 1.70),
                arrowprops=dict(arrowstyle='->', color=C_TEAL, lw=1.5))
    ax.text(11.85, 2.05, 'DAGs', fontsize=7, color=C_TEAL, rotation=90, va='center')

    # CI/CD box (bottom)
    ci_rect = FancyBboxPatch((0.3, 0.8), 4.5, 0.65,
                              boxstyle='round,pad=0.05', linewidth=1.5,
                              edgecolor=C_NAVY, facecolor='#D6EAF8')
    ax.add_patch(ci_rect)
    ax.text(2.55, 1.13, 'CI/CD — GitHub Actions\ntest.yml  |  deploy.yml',
            ha='center', va='center', fontsize=8, color=C_NAVY)

    ax.text(0.1, 0.4, f'DATA SOURCE: AMBER  |  Generated: {date.today().strftime("%d %b %Y")}  |  iNHCES O4 Step 1',
            fontsize=7, color=C_MGREY)

    path = os.path.join(_DIAG, 'diag_01_architecture.png')
    fig.savefig(path, dpi=DPI, bbox_inches='tight', facecolor=C_LGREY)
    plt.close(fig)
    print(f"  [DIAG 1] {path}")
    return path


# ══════════════════════════════════════════════════════════════════════════════
# DIAGRAM 2 — ENTITY-RELATIONSHIP DIAGRAM (ERD)
# ══════════════════════════════════════════════════════════════════════════════
def diag_erd():
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 14); ax.set_ylim(0, 10)
    ax.axis('off')
    fig.patch.set_facecolor(C_LGREY)

    ax.text(7, 9.70, 'iNHCES Entity-Relationship Diagram', ha='center', fontsize=14,
            fontweight='bold', color=C_NAVY)
    ax.text(7, 9.40, 'Supabase PostgreSQL — 16 Tables | TETFund NRF 2025 | ABU Zaria',
            ha='center', fontsize=9, color=C_MGREY)

    def draw_table(ax, x, y, w, h, name, cols, header_color, text_color='white'):
        # Header
        rect_h = FancyBboxPatch((x, y + h - 0.38), w, 0.38,
                                 boxstyle='square', linewidth=1.5,
                                 edgecolor=header_color, facecolor=header_color)
        ax.add_patch(rect_h)
        ax.text(x + w/2, y + h - 0.19, name, ha='center', va='center',
                fontsize=7.5, fontweight='bold', color=text_color)
        # Body
        rect_b = FancyBboxPatch((x, y), w, h - 0.38,
                                 boxstyle='square', linewidth=1.0,
                                 edgecolor=header_color, facecolor='white')
        ax.add_patch(rect_b)
        step = (h - 0.38) / max(len(cols), 1)
        for i, (col, is_key) in enumerate(cols):
            cy = y + h - 0.38 - (i + 0.5) * step
            prefix = '[PK] ' if is_key == 'pk' else '[FK] ' if is_key == 'fk' else '      '
            ax.text(x + 0.08, cy, prefix + col, ha='left', va='center',
                    fontsize=6.5, color=C_NAVY if is_key else '#333333',
                    fontweight='bold' if is_key else 'normal')

    def arrow(ax, x1, y1, x2, y2, label='', color=C_MGREY):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color=color, lw=1.2,
                                    connectionstyle='arc3,rad=0.1'))
        if label:
            mx, my = (x1+x2)/2, (y1+y2)/2
            ax.text(mx, my + 0.05, label, ha='center', fontsize=6, color=color)

    # ── Table definitions: (x, y, w, h, name, [(col, pk/fk/'')], color) ──
    tables = [
        # Users (centre-top)
        (5.8, 7.8, 2.4, 1.3, 'users',
         [('id (UUID)', 'pk'), ('email', ''), ('full_name', ''), ('role', ''), ('institution', '')],
         C_NAVY),
        # Projects
        (1.0, 5.5, 2.5, 2.0, 'projects',
         [('id (UUID)', 'pk'), ('user_id', 'fk'), ('title', ''), ('building_type', ''),
          ('floor_area_sqm', ''), ('location_state', ''), ('status', '')],
         C_BLUE),
        # Predictions
        (4.5, 5.2, 2.8, 2.3, 'predictions',
         [('id (UUID)', 'pk'), ('project_id', 'fk'), ('user_id', 'fk'),
          ('model_version', ''), ('predicted_cost_per_sqm', ''),
          ('feature_snapshot (JSONB)', ''), ('shap_values (JSONB)', '')],
         C_BLUE),
        # Reports
        (8.0, 5.5, 2.4, 1.8, 'reports',
         [('id (UUID)', 'pk'), ('project_id', 'fk'), ('prediction_id', 'fk'),
          ('user_id', 'fk'), ('r2_key', ''), ('file_size_bytes', '')],
         C_BLUE),
        # ml_models
        (10.8, 5.5, 2.8, 2.2, 'ml_models',
         [('id (UUID)', 'pk'), ('mlflow_run_id', ''), ('model_name', ''),
          ('stage', ''), ('mape_test', ''), ('r2_artifact_key', ''),
          ('is_champion', '')],
         C_PURPLE),
        # macro_fx
        (0.2, 2.8, 2.0, 1.5, 'macro_fx',
         [('id', 'pk'), ('date', ''), ('ngn_usd', ''), ('ngn_eur', ''),
          ('ngn_gbp', ''), ('data_level', '')],
         C_GREEN),
        # macro_cpi
        (2.5, 2.8, 2.0, 1.3, 'macro_cpi',
         [('id', 'pk'), ('date', ''), ('cpi_annual_pct', ''), ('data_level', '')],
         C_GREEN),
        # macro_gdp
        (4.8, 2.8, 2.0, 1.3, 'macro_gdp',
         [('id', 'pk'), ('date', ''), ('gdp_growth_pct', ''), ('data_level', '')],
         C_GREEN),
        # macro_oil
        (7.1, 2.8, 2.0, 1.3, 'macro_oil',
         [('id', 'pk'), ('date', ''), ('brent_usd_barrel', ''), ('data_level', '')],
         C_GREEN),
        # material_cement
        (0.2, 0.7, 2.2, 1.8, 'material_cement',
         [('id', 'pk'), ('date', ''), ('brand', ''), ('region', ''),
          ('price_ngn_50kg', ''), ('data_level', '')],
         C_ORANGE),
        # material_steel
        (2.7, 0.7, 2.2, 1.8, 'material_steel',
         [('id', 'pk'), ('date', ''), ('diameter_mm', ''), ('region', ''),
          ('price_ngn_tonne', ''), ('data_level', '')],
         C_ORANGE),
        # unit_rates
        (5.2, 0.7, 2.2, 1.8, 'unit_rates',
         [('id', 'pk'), ('quarter_date', ''), ('trade', ''), ('region', ''),
          ('building_type', ''), ('rate_ngn', '')],
         C_TEAL),
        # market_prices
        (7.7, 0.7, 2.2, 1.8, 'market_prices',
         [('id', 'pk'), ('date', ''), ('zone', ''), ('property_type', ''),
          ('price_ngn_sqm', ''), ('listing_count', '')],
         C_TEAL),
        # audit_log
        (10.5, 2.8, 2.5, 1.5, 'audit_log',
         [('id', 'pk'), ('user_id', 'fk'), ('action', ''), ('table_name', ''),
          ('new_values (JSONB)', ''), ('created_at', '')],
         C_RED),
    ]

    for (x, y, w, h, name, cols, color) in tables:
        draw_table(ax, x, y, w, h, name, cols, color)

    # ── Relationship arrows ───────────────────────────────────────────────────
    # users -> projects
    arrow(ax, 5.8, 8.45, 3.5, 7.5, '1:N', C_BLUE)
    # users -> predictions
    arrow(ax, 7.0, 8.45, 5.9, 7.5, '1:N', C_BLUE)
    # users -> reports
    arrow(ax, 7.5, 8.45, 9.2, 7.3, '1:N', C_BLUE)
    # projects -> predictions
    arrow(ax, 3.5, 5.5, 4.5, 6.5, '1:N', C_BLUE)
    # predictions -> reports
    arrow(ax, 7.3, 6.35, 8.0, 6.4, '1:1', C_BLUE)
    # users -> ml_models (promoted_by)
    arrow(ax, 8.2, 8.45, 11.6, 7.7, 'promoted_by', C_PURPLE)
    # users -> audit_log
    arrow(ax, 8.2, 8.2, 11.0, 4.3, '1:N', C_RED)

    # Legend
    legend_items = [
        (C_NAVY,   'System (users, audit_log)'),
        (C_BLUE,   'Project & Prediction Records'),
        (C_PURPLE, 'ML Model Registry'),
        (C_GREEN,  'Macroeconomic Data'),
        (C_ORANGE, 'Material Prices'),
        (C_TEAL,   'Rates & Market Prices'),
    ]
    for i, (c, lbl) in enumerate(legend_items):
        rect = FancyBboxPatch((0.2 + i * 2.3, 0.08), 0.25, 0.22,
                               boxstyle='square', facecolor=c, edgecolor=c)
        ax.add_patch(rect)
        ax.text(0.55 + i * 2.3, 0.19, lbl, va='center', fontsize=6.5, color=C_NAVY)

    ax.text(0.1, -0.05, f'DATA SOURCE: AMBER  |  Generated: {date.today().strftime("%d %b %Y")}',
            fontsize=7, color=C_MGREY)
    path = os.path.join(_DIAG, 'diag_02_erd.png')
    fig.savefig(path, dpi=DPI, bbox_inches='tight', facecolor=C_LGREY)
    plt.close(fig)
    print(f"  [DIAG 2] {path}")
    return path


# ══════════════════════════════════════════════════════════════════════════════
# DIAGRAM 3 — DFD LEVEL 0 (Context Diagram)
# ══════════════════════════════════════════════════════════════════════════════
def diag_dfd0():
    fig, ax = plt.subplots(figsize=(13, 9))
    ax.set_xlim(0, 13); ax.set_ylim(0, 9)
    ax.axis('off')
    fig.patch.set_facecolor(C_LGREY)

    ax.text(6.5, 8.7, 'DFD Level 0 — Context Diagram', ha='center', fontsize=14,
            fontweight='bold', color=C_NAVY)
    ax.text(6.5, 8.4, 'iNHCES as a single system with all external entities and data flows',
            ha='center', fontsize=9, color=C_MGREY)

    def ext_entity(ax, x, y, w, h, label, color=C_NAVY):
        rect = FancyBboxPatch((x - w/2, y - h/2), w, h,
                               boxstyle='round,pad=0.1', linewidth=2,
                               edgecolor=color, facecolor='white')
        ax.add_patch(rect)
        ax.text(x, y, label, ha='center', va='center', fontsize=8,
                fontweight='bold', color=color, multialignment='center')

    def flow(ax, x1, y1, x2, y2, label, bi=False, color=C_MGREY):
        style = '<->' if bi else '->'
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle=style, color=color, lw=1.5,
                                    connectionstyle='arc3,rad=0.05'))
        mx, my = (x1+x2)/2 + 0.1, (y1+y2)/2 + 0.1
        ax.text(mx, my, label, ha='center', fontsize=6.5, color=color,
                multialignment='center',
                bbox=dict(boxstyle='round,pad=0.1', fc='white', ec='none', alpha=0.8))

    # Central system bubble
    system = plt.Circle((6.5, 4.5), 1.6, color=C_NAVY, zorder=3)
    ax.add_patch(system)
    ax.text(6.5, 4.7, '0', ha='center', va='center', fontsize=16,
            fontweight='bold', color='white', zorder=4)
    ax.text(6.5, 4.2, 'iNHCES', ha='center', va='center', fontsize=10,
            fontweight='bold', color='white', zorder=4)

    # External entities
    # Users (left)
    ext_entity(ax, 1.2, 7.2, 2.0, 0.65, 'QS\nPROFESSIONAL', C_BLUE)
    ext_entity(ax, 1.2, 5.5, 2.0, 0.65, 'RESEARCHER\n/ PI', C_TEAL)
    ext_entity(ax, 1.2, 3.8, 2.0, 0.65, 'SYSTEM\nADMIN', C_PURPLE)

    # Data Sources (right)
    ext_entity(ax, 11.8, 7.8, 2.2, 0.55, 'World Bank\nOpen Data API', C_GREEN)
    ext_entity(ax, 11.8, 6.9, 2.2, 0.55, 'EIA API\n(Brent Crude)', C_GREEN)
    ext_entity(ax, 11.8, 6.0, 2.2, 0.55, 'FRED / CBN\n(FX Rates)', C_GREEN)
    ext_entity(ax, 11.8, 5.1, 2.2, 0.55, 'PropertyPro\n+ Scrapers', C_ORANGE)
    ext_entity(ax, 11.8, 4.2, 2.2, 0.55, 'BusinessDay\n+ Jiji.ng', C_ORANGE)
    ext_entity(ax, 11.8, 3.3, 2.2, 0.55, 'NNPC /\nNMDPRA', C_ORANGE)
    ext_entity(ax, 11.8, 2.4, 2.2, 0.55, 'NIQS\n(Manual Upload)', C_TEAL)

    # CI/CD (bottom)
    ext_entity(ax, 6.5, 1.0, 2.2, 0.55, 'GitHub\n(CI/CD)', C_NAVY)

    # Flows — Users to system
    flow(ax, 2.2, 7.2, 4.9, 5.3, 'Project details\n(type, area, location)', color=C_BLUE)
    flow(ax, 4.9, 4.9, 2.2, 6.9, 'Cost estimate\n+ PDF report', color=C_BLUE)
    flow(ax, 2.2, 5.5, 4.9, 4.8, 'Analysis queries\nModel review', color=C_TEAL)
    flow(ax, 4.9, 4.5, 2.2, 5.2, 'Data + metrics', color=C_TEAL)
    flow(ax, 2.2, 3.8, 4.9, 4.2, 'Admin commands\nNIQS CSV upload', color=C_PURPLE)
    flow(ax, 4.9, 4.1, 2.2, 3.5, 'System status\nAudit log', color=C_PURPLE)

    # Flows — Data sources to system
    flow(ax, 10.7, 7.8, 8.1, 5.1, 'GDP / CPI /\nLending rate', color=C_GREEN)
    flow(ax, 10.7, 6.9, 8.1, 4.9, 'Brent crude\nprice', color=C_GREEN)
    flow(ax, 10.7, 6.0, 8.1, 4.7, 'NGN/USD\nNGN/EUR / GBP', color=C_GREEN)
    flow(ax, 10.7, 5.1, 8.1, 4.5, 'Property\nprices/sqm', color=C_ORANGE)
    flow(ax, 10.7, 4.2, 8.1, 4.3, 'Cement + iron\nrod prices', color=C_ORANGE)
    flow(ax, 10.7, 3.3, 8.1, 4.1, 'PMS pump\nprices', color=C_ORANGE)
    flow(ax, 10.7, 2.4, 8.1, 3.9, 'Unit rates\nCSV', color=C_TEAL)

    # CI/CD
    flow(ax, 6.5, 1.28, 6.5, 2.9, 'Deploy trigger', color=C_NAVY)
    flow(ax, 6.8, 2.9, 6.8, 1.28, 'Build status', color=C_NAVY)

    ax.text(0.1, 0.2, f'DATA SOURCE: AMBER  |  Generated: {date.today().strftime("%d %b %Y")}  |  iNHCES O4 Step 3',
            fontsize=7, color=C_MGREY)

    path = os.path.join(_DIAG, 'diag_03_dfd_level0.png')
    fig.savefig(path, dpi=DPI, bbox_inches='tight', facecolor=C_LGREY)
    plt.close(fig)
    print(f"  [DIAG 3] {path}")
    return path


# ══════════════════════════════════════════════════════════════════════════════
# DIAGRAM 4 — DFD LEVEL 1 (Process Decomposition)
# ══════════════════════════════════════════════════════════════════════════════
def diag_dfd1():
    fig, ax = plt.subplots(figsize=(14, 9))
    ax.set_xlim(0, 14); ax.set_ylim(0, 9)
    ax.axis('off')
    fig.patch.set_facecolor(C_LGREY)

    ax.text(7, 8.72, 'DFD Level 1 — Process Decomposition', ha='center', fontsize=14,
            fontweight='bold', color=C_NAVY)
    ax.text(7, 8.42, '6 processes, 3 data stores, 3 user roles | iNHCES O4 Step 3',
            ha='center', fontsize=9, color=C_MGREY)

    def process(ax, x, y, r, pid, name, color=C_BLUE):
        circ = plt.Circle((x, y), r, color=color, zorder=3, alpha=0.9)
        ax.add_patch(circ)
        ax.text(x, y + 0.12, pid, ha='center', va='center', fontsize=11,
                fontweight='bold', color='white', zorder=4)
        ax.text(x, y - 0.22, name, ha='center', va='center', fontsize=7.5,
                fontweight='bold', color='white', zorder=4, multialignment='center')

    def datastore(ax, x, y, w, h, name, color=C_GREEN):
        rect = FancyBboxPatch((x - w/2, y - h/2), w, h,
                               boxstyle='square', linewidth=2,
                               edgecolor=color, facecolor='#E8F8F5')
        ax.add_patch(rect)
        ax.add_line(Line2D([x - w/2, x + w/2], [y + h/2, y + h/2],
                            color=color, lw=2))
        ax.text(x, y, name, ha='center', va='center', fontsize=8.5,
                fontweight='bold', color=color)

    def entity(ax, x, y, w, h, name, color=C_NAVY):
        rect = FancyBboxPatch((x - w/2, y - h/2), w, h,
                               boxstyle='round,pad=0.05', linewidth=2,
                               edgecolor=color, facecolor='white')
        ax.add_patch(rect)
        ax.text(x, y, name, ha='center', va='center', fontsize=8,
                fontweight='bold', color=color, multialignment='center')

    def arr(ax, x1, y1, x2, y2, label='', color=C_MGREY, rad=0.0):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color=color, lw=1.3,
                                    connectionstyle=f'arc3,rad={rad}'))
        if label:
            mx, my = (x1+x2)/2, (y1+y2)/2
            ax.text(mx, my + 0.08, label, ha='center', fontsize=6, color=color,
                    bbox=dict(boxstyle='round,pad=0.05', fc='white', ec='none', alpha=0.85))

    # ── Data Stores ──────────────────────────────────────────────────────────
    datastore(ax, 7.0, 1.2, 3.2, 0.6, 'D1: Supabase PostgreSQL', C_GREEN)
    datastore(ax, 11.5, 1.2, 2.4, 0.6, 'D2: Cloudflare R2', C_ORANGE)
    datastore(ax, 11.5, 3.0, 2.4, 0.6, 'D3: MLflow Registry', C_PURPLE)

    # ── Processes ─────────────────────────────────────────────────────────────
    process(ax, 2.5, 7.0, 0.85, '1.0', 'User\nAuth', C_NAVY)
    process(ax, 5.5, 7.0, 0.85, '2.0', 'Cost\nEstimation', C_BLUE)
    process(ax, 8.5, 7.0, 0.85, '3.0', 'Data\nIngestion', C_GREEN)
    process(ax, 11.5, 7.0, 0.85, '4.0', 'ML Model\nMgmt', C_PURPLE)
    process(ax, 3.5, 4.0, 0.85, '5.0', 'Report\nGeneration', C_ORANGE)
    process(ax, 6.5, 4.0, 0.85, '6.0', 'Pipeline\nMonitor', C_TEAL)

    # ── External Entities ────────────────────────────────────────────────────
    entity(ax, 0.8, 7.0, 1.3, 0.55, 'QS Pro\n/ Admin', C_NAVY)
    entity(ax, 0.8, 4.0, 1.3, 0.55, 'Researcher\n/ Admin', C_TEAL)
    entity(ax, 9.8, 5.5, 1.5, 0.55, 'External\nData Sources', C_GREEN)
    entity(ax, 0.8, 1.4, 1.3, 0.55, 'GitHub\nCI/CD', C_NAVY)

    # ── Arrows ───────────────────────────────────────────────────────────────
    # Users -> P1 (Auth)
    arr(ax, 1.45, 7.0, 1.65, 7.0, 'credentials', C_NAVY)
    # P1 -> P2 (JWT)
    arr(ax, 3.35, 7.0, 4.65, 7.0, 'JWT token', C_NAVY)
    # QS Pro -> P2
    arr(ax, 1.45, 6.75, 4.65, 6.9, 'project params', C_BLUE)
    # P2 -> D1 (read features)
    arr(ax, 5.5, 6.15, 6.2, 1.5, 'read macro\nfeatures', C_BLUE, rad=0.15)
    # P2 -> D2 (load model)
    arr(ax, 6.35, 7.0, 10.8, 1.4, 'load .pkl', C_ORANGE, rad=-0.1)
    # P2 -> QS Pro (result)
    arr(ax, 4.65, 7.2, 1.45, 7.2, 'cost estimate\n+ SHAP', C_BLUE)
    # Ext Data -> P3
    arr(ax, 9.05, 5.5, 9.35, 6.15, 'macro/material\ndata', C_GREEN)
    # P3 -> D1
    arr(ax, 8.5, 6.15, 7.8, 1.5, 'INSERT rows', C_GREEN, rad=0.1)
    # P3 -> P4 (trigger)
    arr(ax, 9.35, 7.0, 10.65, 7.0, 'new data\ntrigger', C_PURPLE)
    # P4 -> D3 (log experiments)
    arr(ax, 11.5, 6.15, 11.5, 3.3, 'log runs', C_PURPLE)
    # P4 -> D2 (save .pkl)
    arr(ax, 12.0, 6.15, 12.0, 1.5, 'save artifact', C_ORANGE)
    # P4 -> D1 (champion flag)
    arr(ax, 10.65, 6.75, 8.6, 1.5, 'update\nis_champion', C_PURPLE, rad=-0.05)
    # P1 -> P5
    arr(ax, 2.5, 6.15, 3.5, 4.85, 'JWT', C_NAVY)
    # P5 -> D1 (read + write)
    arr(ax, 3.5, 3.15, 5.8, 1.5, 'read project\n+ write report', C_ORANGE)
    # P5 -> D2 (upload PDF)
    arr(ax, 4.35, 4.0, 10.7, 1.4, 'upload PDF', C_ORANGE, rad=-0.15)
    # P5 -> QS Pro (URL)
    arr(ax, 2.65, 3.85, 1.45, 3.75, 'presigned URL', C_ORANGE)
    # D1 -> P6 (latest features)
    arr(ax, 6.2, 1.5, 6.5, 3.15, 'latest feature\nvalues', C_TEAL)
    # D3 -> P6 (baseline)
    arr(ax, 10.3, 3.0, 7.35, 3.75, 'training\nbaseline', C_TEAL)
    # P6 -> P4 (drift alert)
    arr(ax, 7.35, 4.25, 10.65, 6.75, 'PSI>0.2:\nemergency retrain', C_RED, rad=0.1)
    # Admin -> P6
    arr(ax, 1.45, 3.75, 5.65, 4.0, 'pipeline\nstatus req.', C_TEAL)
    # P6 -> Admin
    arr(ax, 5.65, 4.2, 1.45, 4.2, 'DAG health', C_TEAL)
    # GitHub -> P1
    arr(ax, 1.45, 1.68, 2.5, 6.15, 'deploy trigger', C_NAVY, rad=0.2)

    ax.text(0.1, 0.15, f'DATA SOURCE: AMBER  |  Generated: {date.today().strftime("%d %b %Y")}',
            fontsize=7, color=C_MGREY)

    path = os.path.join(_DIAG, 'diag_04_dfd_level1.png')
    fig.savefig(path, dpi=DPI, bbox_inches='tight', facecolor=C_LGREY)
    plt.close(fig)
    print(f"  [DIAG 4] {path}")
    return path


# ══════════════════════════════════════════════════════════════════════════════
# DIAGRAM 5 — AIRFLOW PIPELINE FLOW
# ══════════════════════════════════════════════════════════════════════════════
def diag_pipeline():
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 14); ax.set_ylim(0, 8)
    ax.axis('off')
    fig.patch.set_facecolor(C_LGREY)

    ax.text(7, 7.72, 'Airflow Pipeline Flow — 9 DAGs', ha='center', fontsize=14,
            fontweight='bold', color=C_NAVY)
    ax.text(7, 7.42, 'Data ingestion cadences, ML retrain, and drift detection | iNHCES O4 Step 3',
            ha='center', fontsize=9, color=C_MGREY)

    def dag_box(ax, x, y, w, h, name, schedule, color):
        rect = FancyBboxPatch((x, y), w, h,
                               boxstyle='round,pad=0.05', linewidth=1.5,
                               edgecolor=color, facecolor=color + '22')
        ax.add_patch(rect)
        ax.text(x + w/2, y + h - 0.18, name, ha='center', va='top',
                fontsize=7.5, fontweight='bold', color=color)
        ax.text(x + w/2, y + 0.18, schedule, ha='center', va='bottom',
                fontsize=6.5, color='#555555', style='italic')

    def src_box(ax, x, y, w, h, name, color):
        rect = FancyBboxPatch((x, y), w, h,
                               boxstyle='round,pad=0.05', linewidth=1.5,
                               edgecolor=color, facecolor='white')
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, name, ha='center', va='center',
                fontsize=7, color=color, fontweight='bold', multialignment='center')

    def db_box(ax, x, y, w, h, name, color):
        rect = FancyBboxPatch((x, y), w, h,
                               boxstyle='round,pad=0.05', linewidth=2,
                               edgecolor=color, facecolor='#E8F8F5')
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, name, ha='center', va='center',
                fontsize=8, fontweight='bold', color=color, multialignment='center')

    def arr(ax, x1, y1, x2, y2, label='', color=C_MGREY):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color=color, lw=1.2,
                                    connectionstyle='arc3,rad=0.05'))
        if label:
            mx, my = (x1+x2)/2, (y1+y2)/2
            ax.text(mx + 0.05, my + 0.07, label, fontsize=6, color=color,
                    bbox=dict(boxstyle='round,pad=0.05', fc='white', ec='none', alpha=0.85))

    # ── External sources (left column) ───────────────────────────────────────
    srcs = [
        (0.1, 6.4, 1.6, 0.5, 'World Bank\nOpen Data API', C_GREEN),
        (0.1, 5.6, 1.6, 0.5, 'EIA API\n(Brent Crude)', C_GREEN),
        (0.1, 4.8, 1.6, 0.5, 'FRED / CBN\n(FX Rates)', C_GREEN),
        (0.1, 4.0, 1.6, 0.5, 'BusinessDay\n+ Jiji.ng', C_ORANGE),
        (0.1, 3.2, 1.6, 0.5, 'PropertyPro\n+ PrivateProp.', C_ORANGE),
        (0.1, 2.4, 1.6, 0.5, 'NNPC /\nNMDPRA', C_ORANGE),
        (0.1, 1.6, 1.6, 0.5, 'NIQS\n(Manual CSV)', C_TEAL),
    ]
    for args in srcs:
        src_box(ax, *args)

    # ── Ingestion DAGs (middle-left) ──────────────────────────────────────────
    dags_ingest = [
        (2.0, 6.2, 3.2, 0.7, 'nhces_daily_fx_oil',      '@ 06:00 WAT daily', C_GREEN),
        (2.0, 5.4, 3.2, 0.7, 'nhces_weekly_materials',   '@ Monday', C_ORANGE),
        (2.0, 4.6, 3.2, 0.7, 'nhces_weekly_property',    '@ Tuesday', C_ORANGE),
        (2.0, 3.8, 3.2, 0.7, 'nhces_monthly_macro',      '@ 1st of month', C_GREEN),
        (2.0, 3.0, 3.2, 0.7, 'nhces_quarterly_niqs',     '@ Manual trigger', C_TEAL),
        (2.0, 2.2, 3.2, 0.7, 'nhces_quarterly_nbs',      '@ Quarterly', C_TEAL),
        (2.0, 1.4, 3.2, 0.7, 'nhces_worldbank_annual',   '@ 2 Jan annually', C_GREEN),
    ]
    for args in dags_ingest:
        dag_box(ax, *args)

    # Source -> DAG arrows
    arr(ax, 1.7, 6.65, 2.0, 6.65, '', C_GREEN)   # WB -> monthly
    arr(ax, 1.7, 5.85, 2.0, 6.35, '', C_GREEN)   # EIA -> daily
    arr(ax, 1.7, 5.10, 2.0, 6.25, '', C_GREEN)   # FRED -> daily
    arr(ax, 1.7, 4.35, 2.0, 5.65, '', C_ORANGE)  # BizDay -> materials
    arr(ax, 1.7, 3.55, 2.0, 4.85, '', C_ORANGE)  # PropPro -> property
    arr(ax, 1.7, 2.75, 2.0, 4.05, '', C_ORANGE)  # NNPC -> monthly
    arr(ax, 1.7, 1.95, 2.0, 3.35, '', C_TEAL)    # NIQS -> quarterly

    # ── Supabase DB (centre) ──────────────────────────────────────────────────
    db_box(ax, 5.5, 2.0, 2.8, 4.8, 'Supabase\nPostgreSQL\n\nmacro_fx / cpi / gdp\nmacro_interest / oil\nmaterial_cement / steel\nmaterial_pms\nunit_rates\nmarket_prices', C_GREEN)

    # DAG -> DB arrows
    for y in [6.55, 5.75, 4.95, 4.15, 3.35, 2.55, 1.75]:
        arr(ax, 5.2, y, 5.5, min(y, 6.7), 'INSERT', C_GREEN)

    # ── ML DAGs (right side) ──────────────────────────────────────────────────
    dag_box(ax, 9.0, 5.5, 3.5, 1.2, 'nhces_retrain_weekly',
            '@ Sunday 02:00 WAT', C_PURPLE)
    dag_box(ax, 9.0, 3.8, 3.5, 1.2, 'nhces_drift_monitor',
            '@ 18:00 WAT daily', C_RED)

    # DB -> ML DAGs
    arr(ax, 8.3, 5.5, 9.0, 6.0, 'feature matrix', C_PURPLE)
    arr(ax, 8.3, 4.5, 9.0, 4.3, 'latest features', C_RED)

    # ── MLflow + R2 (far right) ───────────────────────────────────────────────
    db_box(ax, 12.8, 5.5, 1.0, 1.2, 'MLflow\nRegistry', C_PURPLE)
    db_box(ax, 12.8, 3.8, 1.0, 1.2, 'Cloud-\nflare R2', C_ORANGE)

    arr(ax, 12.5, 6.1, 12.8, 6.1, 'log runs\n+ metrics', C_PURPLE)
    arr(ax, 12.5, 5.7, 12.8, 5.7, 'save .pkl', C_ORANGE)
    arr(ax, 12.5, 4.2, 12.8, 4.2, 'PSI scores', C_RED)

    # Drift -> Retrain
    arr(ax, 10.75, 5.5, 10.75, 5.0, 'PSI > 0.2:\nemergency\nretrain', C_RED)

    # FastAPI
    fa_box = FancyBboxPatch((9.0, 1.5), 3.5, 0.9,
                             boxstyle='round,pad=0.05', linewidth=2,
                             edgecolor=C_BLUE, facecolor='#D6EAF8')
    ax.add_patch(fa_box)
    ax.text(10.75, 1.95, 'FastAPI  POST /estimate\n(loads champion from R2)', ha='center',
            va='center', fontsize=8, fontweight='bold', color=C_BLUE)
    arr(ax, 12.8, 3.8, 12.3, 2.4, 'champion\n.pkl', C_ORANGE)
    arr(ax, 12.3, 2.1, 12.5, 1.95, '', C_ORANGE)

    ax.text(0.1, 0.7, f'DATA SOURCE: AMBER  |  Generated: {date.today().strftime("%d %b %Y")}',
            fontsize=7, color=C_MGREY)

    path = os.path.join(_DIAG, 'diag_05_pipeline.png')
    fig.savefig(path, dpi=DPI, bbox_inches='tight', facecolor=C_LGREY)
    plt.close(fig)
    print(f"  [DIAG 5] {path}")
    return path


# ══════════════════════════════════════════════════════════════════════════════
# DIAGRAM 6 — USER JOURNEY MAP
# ══════════════════════════════════════════════════════════════════════════════
def diag_user_journey():
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.set_xlim(0, 14); ax.set_ylim(0, 6)
    ax.axis('off')
    fig.patch.set_facecolor(C_LGREY)

    ax.text(7, 5.75, 'User Journey Map — QS Professional (Primary Persona)',
            ha='center', fontsize=13, fontweight='bold', color=C_NAVY)
    ax.text(7, 5.45, 'Satisfaction score 1-5 (red=pain point, green=delight) | iNHCES O4 Step 3',
            ha='center', fontsize=9, color=C_MGREY)

    stages = [
        ('DISCOVERY\n& ONBOARDING', 0.4, 3.0, [
            ('Visit landing\npage', 4),
            ('Register &\nverify email', 3),
            ('Log in\n(JWT)', 5),
        ]),
        ('PROJECT\nSETUP', 3.0, 2.8, [
            ('New Project\nform', 5),
            ('Enter area\n& location', 5),
            ('Save to\nSupabase', 5),
        ]),
        ('COST\nESTIMATION', 5.8, 2.8, [
            ('Click\nEstimate', 5),
            ('View result\n+ SHAP', 5),
            ('Freshness\nwarning?', 3),
        ]),
        ('REPORT\nGENERATION', 8.6, 2.8, [
            ('Generate\nPDF', 5),
            ('Download\n(24hr URL)', 4),
            ('Share with\nclient', 4),
        ]),
        ('ONGOING\nUSE', 11.4, 2.8, [
            ('Return for\nnext project', 5),
            ('Check model\nMAPE', 4),
            ('RED data\nalert?', 2),
        ]),
    ]

    colours = {1: '#C0392B', 2: '#E67E22', 3: '#F1C40F', 4: '#52BE80', 5: '#1E8449'}
    stage_colours = [C_TEAL, C_BLUE, C_PURPLE, C_ORANGE, C_NAVY]

    # Draw stage headers
    for i, (stage, sx, w, steps) in enumerate(stages):
        col = stage_colours[i]
        rect = FancyBboxPatch((sx, 3.9), w - 0.1, 1.3,
                               boxstyle='round,pad=0.05', linewidth=2,
                               edgecolor=col, facecolor=col)
        ax.add_patch(rect)
        ax.text(sx + (w-0.1)/2, 4.55, stage, ha='center', va='center',
                fontsize=8.5, fontweight='bold', color='white', multialignment='center')

        # Draw step boxes
        sw = (w - 0.1) / len(steps)
        for j, (step_lbl, score) in enumerate(steps):
            sx_s = sx + j * sw
            s_col = colours[score]
            box = FancyBboxPatch((sx_s + 0.05, 0.5), sw - 0.1, 3.0,
                                  boxstyle='round,pad=0.05', linewidth=1.5,
                                  edgecolor=s_col, facecolor=s_col + '33')
            ax.add_patch(box)
            ax.text(sx_s + sw/2, 2.5, step_lbl, ha='center', va='center',
                    fontsize=7.5, color=C_NAVY, multialignment='center')
            # Score circle
            circ = plt.Circle((sx_s + sw/2, 0.9), 0.28, color=s_col, zorder=5)
            ax.add_patch(circ)
            ax.text(sx_s + sw/2, 0.9, str(score), ha='center', va='center',
                    fontsize=9, fontweight='bold', color='white', zorder=6)

    # Journey line (connect step midpoints at y=3.9)
    prev_x = None
    for i, (stage, sx, w, steps) in enumerate(stages):
        sw = (w - 0.1) / len(steps)
        for j, (_, score) in enumerate(steps):
            cx = sx + j * sw + sw/2
            ax.plot(cx, 3.88, 'o', color=colours[score], markersize=7, zorder=7)
            if prev_x is not None:
                ax.plot([prev_x, cx], [3.88, 3.88], color=C_MGREY, lw=1.5, zorder=6)
            prev_x = cx

    # Legend
    for score, col in colours.items():
        circ = plt.Circle((0.4 + (score-1)*1.2, 0.2), 0.14, color=col)
        ax.add_patch(circ)
        lbl = {1:'Very poor',2:'Poor',3:'Neutral',4:'Good',5:'Excellent'}[score]
        ax.text(0.65 + (score-1)*1.2, 0.2, f'{score} = {lbl}', va='center', fontsize=7, color=C_NAVY)

    ax.text(12.5, 0.2, f'Generated: {date.today().strftime("%d %b %Y")}',
            fontsize=7, color=C_MGREY, ha='right')

    path = os.path.join(_DIAG, 'diag_06_user_journey.png')
    fig.savefig(path, dpi=DPI, bbox_inches='tight', facecolor=C_LGREY)
    plt.close(fig)
    print(f"  [DIAG 6] {path}")
    return path


# ══════════════════════════════════════════════════════════════════════════════
# CONSOLIDATED PDF
# ══════════════════════════════════════════════════════════════════════════════
def generate_consolidated_pdf(paths):
    out = os.path.join(_HERE, 'O4_00_Conceptual_Diagrams.pdf')

    class DiagPDF(DocPDF):
        def header(self):
            self.set_fill_color(*DARK_NAVY)
            self.rect(0, 0, 210, 14, 'F')
            self.set_font("Helvetica", "B", 7)
            self.set_text_color(255,255,255)
            self.set_xy(5, 4)
            self.cell(PAGE_W, 6, sanitize(
                "iNHCES  |  TETFund NRF 2025  |  O4 Conceptual Diagrams  |  All Six Diagrams"
            ))
            self.set_text_color(60,60,60)
            self.ln(16)
        def footer(self):
            self.set_y(-13)
            self.set_draw_color(*GOLD)
            self.set_line_width(0.4)
            self.line(LEFT, self.get_y(), 198, self.get_y())
            self.set_font("Helvetica", "I", 7.5)
            self.set_text_color(120,120,120)
            self.cell(0, 8, sanitize(f"O4 Conceptual Diagrams  |  ABU Zaria / TETFund NRF 2025  |  Page {self.page_no()}"), align="C")

    pdf = DiagPDF("O4_00_Conceptual_Diagrams.pdf", "O4-00")

    # Cover
    pdf.add_page()
    pdf.set_fill_color(*DARK_NAVY)
    pdf.rect(0, 18, 210, 45, 'F')
    pdf.set_xy(0, 26)
    pdf.set_font("Helvetica", "B", 15)
    pdf.set_text_color(255,255,255)
    pdf.cell(210, 9, "O4 Conceptual Diagrams", align="C", ln=True)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(200,215,235)
    pdf.cell(210, 7, "iNHCES System Architecture, ERD, DFDs, Pipeline Flow, User Journey", align="C", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(220,230,245)
    pdf.cell(210, 6, "TETFund NRF 2025  |  Department of Quantity Surveying, ABU Zaria", align="C", ln=True)
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(0.8)
    pdf.line(30, 76, 180, 76)
    pdf.set_xy(LEFT, 84)
    for label, val in [
        ("Objective:", "O4 — Conceptual Models"),
        ("Content:",   "Six publication-quality diagrams for all O4 design artefacts"),
        ("Diagrams:",  "Architecture | ERD | DFD Level 0 | DFD Level 1 | Pipeline | User Journey"),
        ("Date:",      date.today().strftime("%d %B %Y")),
        ("Purpose:",   "Visual companion to O4_01 through O4_04 documents"),
        ("Note:",      "All diagrams are AMBER — AI-authored from O3 SRS and O4 design decisions"),
    ]:
        pdf.set_x(LEFT)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(15,40,80)
        pdf.cell(40, 6.5, sanitize(label))
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(60,60,60)
        pdf.cell(PAGE_W-40, 6.5, sanitize(val), ln=True)

    _ds_page(pdf, 'amber',
        "DATA SOURCE: AMBER -- AI-authored conceptual diagrams. "
        "Validate all diagrams against O3 SRS before O6 build.",
        "All six diagrams were generated programmatically (matplotlib) by Claude Code "
        "from the iNHCES design specifications in O4 Steps 1-3. "
        "They represent intended system design, not implemented behaviour.\n\n"
        "Render the Mermaid .mmd files in mermaid.live for alternative views "
        "of the same concepts. These PNG diagrams are optimised for PDF embedding "
        "and paper figures."
    )

    diag_meta = [
        ("Diagram 1 — System Architecture",
         "Seven-layer architecture showing all components, hosting platforms, "
         "and data flow directions between the User, Presentation, API, ML, "
         "Data, Storage, and Pipeline layers.", paths[0]),
        ("Diagram 2 — Entity-Relationship Diagram (ERD)",
         "All 16 Supabase PostgreSQL tables with primary keys (PK), foreign keys (FK), "
         "key columns, and 1:N / 1:1 relationship lines. "
         "Colour-coded by functional group.", paths[1]),
        ("Diagram 3 — DFD Level 0 (Context Diagram)",
         "iNHCES as a single system bubble (Process 0) with all 11 external entities "
         "(3 user roles + 7 data sources + GitHub CI/CD) and all "
         "inbound/outbound data flows labelled.", paths[2]),
        ("Diagram 4 — DFD Level 1 (Process Decomposition)",
         "System decomposed into 6 processes (Auth, Cost Estimation, Data Ingestion, "
         "ML Management, Report Generation, Pipeline Monitor), 3 data stores "
         "(Supabase, R2, MLflow), and all inter-process data flows.", paths[3]),
        ("Diagram 5 — Airflow Pipeline Flow",
         "All 9 Airflow DAGs with cron schedules, external data source connections, "
         "Supabase table targets, ML retrain pipeline (6-task sequence), "
         "drift detection, and FastAPI inference link.", paths[4]),
        ("Diagram 6 — User Journey Map",
         "QS Professional primary persona: 5 stages, 15 touchpoints scored 1-5. "
         "Pain points highlighted in red/amber. Delight points in green.", paths[5]),
    ]

    for title, desc, img_path in diag_meta:
        pdf.add_page()
        pdf.section_title(title)
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(60,60,60)
        pdf.set_x(LEFT)
        pdf.multi_cell(PAGE_W, 5.2, sanitize(desc))
        pdf.ln(2)
        if os.path.exists(img_path):
            pdf.image(img_path, x=LEFT, w=PAGE_W)
        else:
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_x(LEFT)
            pdf.cell(PAGE_W, 8, sanitize(f"[Image not found: {img_path}]"))
        pdf.ln(1)
        pdf.set_font("Helvetica", "I", 7.5)
        pdf.set_text_color(120,120,120)
        pdf.set_x(LEFT)
        pdf.cell(PAGE_W, 5, sanitize(
            f"DATA SOURCE: AMBER  |  {os.path.basename(img_path)}  |  "
            f"iNHCES O4 | ABU Zaria / TETFund NRF 2025"
        ))

    pdf.output(out)
    print(f"\n[PDF] O4_00_Conceptual_Diagrams.pdf -> {out}  ({pdf.page} pages)")
    return out


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    print("\n=== O4 Conceptual Diagrams Generator ===")
    p1 = diag_architecture()
    p2 = diag_erd()
    p3 = diag_dfd0()
    p4 = diag_dfd1()
    p5 = diag_pipeline()
    p6 = diag_user_journey()
    pdf_path = generate_consolidated_pdf([p1, p2, p3, p4, p5, p6])
    print(f"\n[OK] 6 diagrams + consolidated PDF generated")
    print(f"     PNGs in: {_DIAG}")
    print(f"     PDF: O4_00_Conceptual_Diagrams.pdf")
    return [p1, p2, p3, p4, p5, p6]


if __name__ == "__main__":
    main()
