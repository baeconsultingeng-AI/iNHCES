"""
iNHCES O6 Step 11 — Database Verification Report Generator
Deliverable: O6_11_Database_Verification.pdf
Agent 05 output — schema verification, RLS testing guide, function reference.
DATA SOURCE: AMBER
TETFund NRF 2025 | Department of Quantity Surveying, ABU Zaria
"""

import sys, os
from datetime import date

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, os.path.join(_ROOT, '01_literature_review'))

from generate_o1_pdfs import (
    DocPDF, sanitize, _ds_page,
    DARK_NAVY, GOLD, LIGHT_BLUE, WHITE, DARK_GREY, MID_GREY,
    PAGE_W, LEFT, LINE_H,
)

OUT = os.path.join(_HERE, 'O6_11_Database_Verification.pdf')


class VerifPDF(DocPDF):
    def __init__(self):
        super().__init__("O6-11 Database Verification", "O6-11")

    def header(self):
        self.set_fill_color(*DARK_NAVY)
        self.rect(0, 0, 210, 14, 'F')
        self.set_font("Helvetica", "B", 7)
        self.set_text_color(*WHITE)
        self.set_xy(5, 4)
        self.cell(PAGE_W, 6, sanitize(
            "iNHCES  |  TETFund NRF 2025  |  O6 Step 11 -- Agent 05: Database Verification"
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
            f"O6-11 Database Verification  |  ABU Zaria / TETFund NRF 2025  |  Page {self.page_no()}"
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

    def para(self, text):
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(*DARK_GREY)
        self.set_x(LEFT)
        self.multi_cell(PAGE_W, 5.2, sanitize(text))
        self.ln(1.5)

    def check_row(self, check_num, description, expected, file_ref=''):
        self.set_fill_color(245, 248, 255)
        self.set_draw_color(*MID_GREY)
        cw = [8, 8, 70, PAGE_W - 86]
        self.set_x(LEFT)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*DARK_GREY)
        self.cell(cw[0], LINE_H, sanitize(f"#{check_num}"), border=1)
        self.set_fill_color(235, 248, 235)
        self.cell(cw[1], LINE_H, "[ ]", border=1, fill=True)
        self.set_fill_color(245, 248, 255)
        self.set_font("Helvetica", "", 8)
        self.cell(cw[2], LINE_H, sanitize(f" {description}"), border=1, fill=True)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*MID_GREY)
        self.cell(cw[3], LINE_H, sanitize(f" {expected}"), border=1, fill=True)
        self.ln()
        self.set_text_color(*DARK_GREY)


def make_cover(pdf):
    pdf.add_page()
    pdf.set_fill_color(*DARK_NAVY)
    pdf.rect(0, 18, 210, 45, 'F')
    pdf.set_xy(0, 26)
    pdf.set_font("Helvetica", "B", 15)
    pdf.set_text_color(*WHITE)
    pdf.cell(210, 9, "O6 Step 11: Database Verification Report", align="C", ln=True)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(200, 215, 235)
    pdf.cell(210, 7, "Agent 05 -- Schema, RLS, Functions, Indexes", align="C", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*LIGHT_BLUE)
    pdf.cell(210, 6, "TETFund NRF 2025  |  Department of Quantity Surveying, ABU Zaria", align="C", ln=True)
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(0.8)
    pdf.line(30, 76, 180, 76)
    pdf.set_xy(LEFT, 84)
    for label, val in [
        ("Document:",  "O6_11_Database_Verification.pdf"),
        ("Agent:",     "05 -- Database Developer"),
        ("Date:",      date.today().strftime("%d %B %Y")),
        ("Files:",     "04_schema.sql | 04_rls_policies.sql | 04_seed_data.sql"),
        ("New files:", "04_db_functions.sql | 04_db_indexes.sql | 04_db_verification.sql"),
        ("Platform:",  "Supabase PostgreSQL 15"),
        ("Next:",      "O6-S12 -- Agent 06+07: QA + Code Review"),
    ]:
        pdf.set_x(LEFT)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*DARK_NAVY)
        pdf.cell(42, 6.5, sanitize(label))
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*DARK_GREY)
        pdf.cell(PAGE_W - 42, 6.5, sanitize(val), ln=True)


def section1(pdf):
    pdf.add_page()
    pdf.h1("1. Schema Verification Checklist")
    pdf.para(
        "Run 04_db_verification.sql in the Supabase SQL Editor to verify each check. "
        "All 14 checks must pass before O6-S12 (QA) begins. "
        "Tick the [ ] box after confirming each result."
    )

    pdf.section_title("1.1 Table and View Existence")
    pdf.thead(["#", "Pass", "Check", "Expected Result"], [8, 8, 70, PAGE_W - 86])
    checks_tables = [
        (1,  "All 16 tables exist",          "16 rows in information_schema.tables"),
        (2,  "RLS enabled on all 16 tables",  "16 rows with rowsecurity=TRUE"),
        (3,  "Both helper views exist",        "2 rows: v_champion_model, v_latest_macro"),
        (4,  "5+ DB functions exist",          "handle_new_user, set_updated_at, get_*, log_*, refresh_*"),
        (5,  "7 enum types exist",             "building_type, construction_type, data_source_level, model_stage, nigeria_zone, project_status, user_role"),
        (6,  "Champion partial index exists",  "idx_ml_models_one_champion in pg_indexes"),
    ]
    for num, desc, exp in checks_tables:
        pdf.check_row(num, desc, exp)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 1: Schema existence checks. Run CHECK 1-6 queries from 04_db_verification.sql."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)

    pdf.section_title("1.2 Data and Function Checks")
    pdf.thead(["#", "Pass", "Check", "Expected Result"], [8, 8, 70, PAGE_W - 86])
    checks_data = [
        (7,  "v_latest_macro returns data",      "7 rows (one per variable) — or 0 if no seed data"),
        (8,  "Seed data row counts correct",     "macro_fx=5, material_cement=8, projects=2, ml_models=1"),
        (9,  "Exactly 1 champion model",         "1 row with is_champion=TRUE"),
        (10, "RLS policy count per table",       "Each table has >= 2 policies"),
        (11, "get_latest_macro_snapshot() works","7 rows returned by RPC call"),
        (12, "get_champion_model() works",       "1 row returned (or 0 if no seed)"),
        (13, "Auth trigger exists",              "on_auth_user_created trigger on auth.users"),
        (14, "Performance index count",          ">= 25 indexes in pg_indexes"),
    ]
    for num, desc, exp in checks_data:
        pdf.check_row(num, desc, exp)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 2: Data and function checks. Run CHECK 7-14 queries from 04_db_verification.sql."
    ))
    pdf.set_text_color(*DARK_GREY)


def section2(pdf):
    pdf.add_page()
    pdf.h1("2. RLS Policy Test Guide")
    pdf.para(
        "These tests require real Supabase JWT tokens for each role. "
        "Use the Supabase JavaScript client with the anon key and test user credentials. "
        "All 4 tests must pass before the system is production-ready."
    )

    tw = [8, 28, 50, PAGE_W - 86]
    pdf.thead(["#", "Role", "Action", "Expected Result"], tw)
    rls_tests = [
        ("T1", "anon (no JWT)",      "SELECT * FROM projects",
         "0 rows (RLS blocks unauthenticated access)"),
        ("T2", "qsprofessional JWT", "SELECT * FROM projects",
         "Only rows WHERE user_id = auth.uid()"),
        ("T3", "service_role key",   "INSERT INTO macro_fx (...)",
         "Success — service_role bypasses RLS"),
        ("T4", "qsprofessional JWT", "INSERT INTO macro_fx (...)",
         "403 Forbidden — INSERT blocked by RLS"),
        ("T5", "researcher JWT",     "SELECT * FROM projects",
         "All project rows (researcher sees aggregate data)"),
        ("T6", "admin JWT",          "SELECT * FROM audit_log",
         "All audit rows (admin-only SELECT)"),
    ]
    for num, role, action, exp in rls_tests:
        self = pdf
        pdf.set_fill_color(245, 248, 255)
        pdf.set_x(LEFT)
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(*DARK_GREY)
        pdf.cell(tw[0], LINE_H, sanitize(num), border=1)
        pdf.set_font("Helvetica", "", 8)
        pdf.cell(tw[1], LINE_H, sanitize(f" {role}"), border=1, fill=True)
        pdf.cell(tw[2], LINE_H, sanitize(f" {action}"), border=1, fill=True)
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(*MID_GREY)
        pdf.cell(tw[3], LINE_H, sanitize(f" {exp}"), border=1, fill=True)
        pdf.ln()
        pdf.set_text_color(*DARK_GREY)

    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 3: RLS policy tests. Requires test user accounts for each role "
        "created in Supabase Auth Dashboard."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)

    pdf.h2("2.1 How to Create Test JWT Tokens")
    pdf.bullet([
        "In Supabase Dashboard -> Authentication -> Users -> Add User (for each test role).",
        "Use the Supabase JS client in a browser console: "
        "const { data } = await supabase.auth.signInWithPassword({email, password}); "
        "console.log(data.session.access_token);",
        "Paste the JWT into a tool like jwt.io to verify the payload includes "
        "the correct role claim in user_metadata.",
        "Use the token in Postman or curl to test RLS: "
        "curl -H 'Authorization: Bearer <token>' https://project.supabase.co/rest/v1/projects",
    ])


def section3(pdf):
    pdf.add_page()
    pdf.h1("3. New DB Functions Reference")
    pdf.para(
        "Five new PostgreSQL functions were added in O6 Step 11 (04_db_functions.sql). "
        "These supplement the existing trigger functions (handle_new_user, set_updated_at) "
        "already in 04_schema.sql."
    )

    fw = [45, PAGE_W - 45]
    pdf.thead(["Function", "Purpose and Usage"], fw)
    funcs = [
        ("get_latest_macro_snapshot()",
         "Returns 7 rows (one per macro variable) with latest value, source, and data_level. "
         "Used by FastAPI GET /macro endpoint. Replaces v_latest_macro view for complex queries."),
        ("get_user_project_summary(user_id)",
         "Returns all projects for a user with latest prediction cost and prediction count. "
         "Used by FastAPI GET /projects for enriched project list display."),
        ("get_champion_model()",
         "Returns current Production champion ML model metadata (mape, r2, artifact key). "
         "Guaranteed single row via partial unique index on is_champion=TRUE."),
        ("log_audit_event(user_id, action, ...)",
         "Convenience INSERT wrapper for audit_log with SECURITY DEFINER. "
         "Used by all FastAPI write endpoints."),
        ("refresh_champion_flag(run_id)",
         "Atomically demotes old champion and promotes new one in a single transaction. "
         "Called by Airflow nhces_retrain_weekly DAG promote task."),
    ]
    for i, (fn, desc) in enumerate(funcs):
        pdf.mrow([fn, desc], fw, fill=(i % 2 == 1))

    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 4: New DB functions. All granted EXECUTE to authenticated + service_role."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)

    pdf.h1("4. Additional Performance Indexes")
    pdf.para(
        "14 additional indexes were added in 04_db_indexes.sql for performance at scale. "
        "Key targets: predictions table (highest query volume), macro time-series range "
        "queries, and user-scoped project lists."
    )

    iw = [55, 35, PAGE_W - 90]
    pdf.thead(["Index Name", "Table", "Columns / Purpose"], iw)
    indexes = [
        ("idx_predictions_user_created",   "predictions",      "user_id, created_at DESC — dashboard list"),
        ("idx_predictions_project_created","predictions",      "project_id, created_at DESC — project history"),
        ("idx_predictions_feature_snapshot","predictions",     "GIN on feature_snapshot JSONB"),
        ("idx_macro_fx_date_desc",          "macro_fx",        "date DESC — latest value query"),
        ("idx_macro_cpi_date_desc",         "macro_cpi",       "date DESC, frequency"),
        ("idx_material_cement_date_brand",  "material_cement", "date DESC, brand, region"),
        ("idx_projects_user_status",        "projects",        "user_id, status, created_at DESC"),
        ("idx_ml_models_stage_mape",        "ml_models",       "stage, mape_test ASC — challenger comparison"),
        ("idx_audit_log_action_created",    "audit_log",       "action, created_at DESC — admin queries"),
    ]
    for i, row in enumerate(indexes):
        pdf.trow(list(row), iw, fill=(i % 2 == 1))
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 5: Key additional indexes. Full list in 04_db_indexes.sql."
    ))
    pdf.set_text_color(*DARK_GREY)


def section4(pdf):
    pdf.add_page()
    pdf.h1("5. Pre-Launch Checklist (Before O6-S12)")
    pdf.info_box(
        "DATA SOURCE: AMBER -- This verification document was generated by Claude Code "
        "as Agent 05 output. The SQL files are real specifications; actual verification "
        "requires running the scripts in a live Supabase instance. "
        "Tick every item below before proceeding to O6-S12."
    )
    pdf.ln(2)

    launch_checks = [
        ("Run 04_schema.sql in Supabase SQL Editor -- 0 errors",              "MANDATORY"),
        ("Run 04_rls_policies.sql -- 0 errors",                               "MANDATORY"),
        ("Run 04_db_functions.sql -- 0 errors",                               "MANDATORY"),
        ("Run 04_db_indexes.sql -- 0 errors",                                 "MANDATORY"),
        ("Run 04_db_verification.sql -- all 14 checks pass",                  "MANDATORY"),
        ("Run 04_seed_data.sql with real auth user UUIDs -- data loads OK",   "RECOMMENDED"),
        ("RLS tests T1-T6 all pass with test JWT tokens",                     "MANDATORY"),
        ("FastAPI GET /health returns {status: ok, db: {status: ok}}",        "MANDATORY"),
        ("POST /estimate returns prediction + 4 projections in < 3 seconds",  "MANDATORY"),
        ("GET /macro returns 7 variables with correct data_level badges",     "MANDATORY"),
        ("Configure SUPABASE_URL + SERVICE_KEY in Railway env vars",          "MANDATORY"),
        ("Add NEXT_PUBLIC_SUPABASE_URL + ANON_KEY to Vercel env vars",        "MANDATORY"),
        ("Set real FRED_API_KEY to upgrade FX data to GREEN level",           "RECOMMENDED"),
        ("Set real EIA_API_KEY to upgrade Brent data to GREEN level",         "RECOMMENDED"),
    ]

    lw = [8, 55, PAGE_W - 63]
    pdf.thead(["", "Check", "Priority"], lw)
    for desc, priority in launch_checks:
        fill_col = (240, 220, 220) if priority == "MANDATORY" else (220, 240, 225)
        pdf.set_fill_color(*fill_col)
        pdf.set_x(LEFT)
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(*DARK_GREY)
        pdf.cell(lw[0], LINE_H, "[ ]", border=1, fill=True)
        pdf.set_font("Helvetica", "", 8)
        pdf.cell(lw[1], LINE_H, sanitize(f" {desc}"), border=1, fill=True)
        c = (192, 57, 43) if priority == "MANDATORY" else (0, 122, 94)
        pdf.set_text_color(*c)
        pdf.set_font("Helvetica", "B", 8)
        pdf.cell(lw[2], LINE_H, sanitize(f" {priority}"), border=1, fill=True)
        pdf.ln()
        pdf.set_text_color(*DARK_GREY)

    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 6: Pre-launch checklist. All MANDATORY items must be ticked before O6-S12."
    ))


def main():
    pdf = VerifPDF()
    make_cover(pdf)
    _ds_page(pdf, 'amber',
        "DATA SOURCE: AMBER -- Agent 05 database verification document.",
        (
            "WHAT IS REAL:\n"
            "  * SQL files (04_schema.sql, 04_rls_policies.sql, 04_db_functions.sql, "
            "04_db_indexes.sql, 04_db_verification.sql) are real PostgreSQL specifications.\n"
            "  * Verification check queries are syntactically correct SQL.\n"
            "  * RLS test procedures reflect real Supabase auth patterns.\n\n"
            "WHAT REQUIRES A LIVE SUPABASE INSTANCE:\n"
            "  * All 14 verification checks must be run in the Supabase SQL Editor.\n"
            "  * RLS tests T1-T6 require real JWT tokens for each role.\n"
            "  * FastAPI health check requires the server to connect to Supabase.\n\n"
            "ACTION: Run all SQL files in the correct order in Supabase before O6-S12."
        )
    )
    section1(pdf)
    section2(pdf)
    section3(pdf)
    section4(pdf)
    pdf.output(OUT)
    print(f"[OK] O6_11_Database_Verification.pdf ({pdf.page} pages) -> {OUT}")


if __name__ == "__main__":
    main()
