# iNHCES Project Context

## Project
Intelligent National Housing Cost Estimating System (iNHCES)
TETFund NRF 2025 | Department of Quantity Surveying, ABU Zaria

## Governing Framework
Every session is governed by the Research Simulation Preamble Document:
`01_literature_review/00_Research_Simulation_Introduction.pdf`
- Apply DATA SOURCE banner (GREEN / AMBER / RED) to every PDF produced
- GREEN = live API / real instrument | AMBER = AI-authored template | RED = synthetic data
- RED-banner content MUST be replaced with real data before any publication
- No AI-generated citations — verify every reference in Scopus / Web of Science
- AI is a tool, not an author — human researchers bear full accountability

## Tech Stack
- **Frontend**: Vanilla HTML/CSS/JS → Vercel
- **Backend**: FastAPI (Python 3.10+) → Railway
- **Database**: Supabase PostgreSQL
- **ML Registry**: MLflow → Railway
- **Storage**: Cloudflare R2
- **Orchestration**: Apache Airflow → Railway
- **CI/CD**: GitHub Actions

## Current Build Status

### ✅ Completed
- [x] Full project folder structure scaffolded
- [x] CLAUDE.md and PROJECT_CONTEXT.md created
- [x] Research Simulation Preamble Document (`01_literature_review/00_Research_Simulation_Introduction.pdf`)
- [x] O1 — All 5 steps complete (16 PDFs: PRISMA protocol, search strings, data extraction template,
      methodology taxonomy, ML comparison, literature review draft, gap analysis, bibliography,
      QS survey instrument, SPSS analysis plan, hypothetical survey analysis x5, PRISMA checklist)
      Generator: `01_literature_review/generate_o1_pdfs.py` + `run_o1_hypothetical_survey.py`
      + `generate_prisma_checklist.py`
- [x] O2 — All 4 steps complete (6 scripts, 6 PDFs, 8 CSVs)
      - fetch_worldbank.py → O2_01 (GREEN, live World Bank API)
      - fetch_eia_oil.py → O2_02 (RED, synthetic — set EIA_API_KEY to upgrade)
      - fetch_cbn_fx.py → O2_03 (RED, synthetic — set FRED_API_KEY to upgrade)
      - stationarity_analysis.py → O2_04 (AMBER, ADF+KPSS on 7 macro vars)
      - var_vecm_model.py → O2_05 (AMBER, Johansen rank=0, VAR(diff,lag=1))
      - shap_variable_selection.py → O2_06 (RED, SHAP on synthetic housing proxy)
      Integration orders: GDP/CPI/lending/Brent = I(1) | NGN/USD/EUR/GBP = I(2)*
      SHAP ranking: NGN/USD (45%) > CPI (25.5%) > NGN/EUR (11.6%) > Brent (10.9%)
- [x] O3 — All steps complete (8 PDFs, 12 support files)
      - O3_01 Stakeholder Register (GREEN)
      - O3_02/03/05 Delphi R1/R2/R3 Instruments (AMBER)
      - O3_04/06 Delphi R2 Analysis + Final Consensus (RED, synthetic n=20 seed=42)
      - O3_07 SRS IEEE 830 (AMBER) | O3_08 UML Use Cases (GREEN)
      Delphi: 38 items, 36/40 consensus. Excluded: B6, C6, E5, G2.
      Generator: `03_requirements/generate_o3_pdfs.py`
- [x] Draft Papers — P1, P2, P3, P4, P5, P6, P9 in `Draft AI Papers/`
      P4 = Cloud-native data pipeline (10pp, Scientific Data, AMBER/RED)
      P5 = ML benchmarking with live results (10pp, ASCE JCEM, RED)
      P6 = MLOps champion-challenger + PSI drift (12pp, Expert Sys. Apps., AMBER)
      P9 = AI Research Simulation Framework (27pp, AMBER, Computers & Education / IETI)
- [x] O4 Conceptual Diagrams — `04_conceptual_models/O4_00_Conceptual_Diagrams.pdf`
      6 matplotlib PNG diagrams: Architecture (7-layer) | ERD (16 tables) |
      DFD Level 0 (context) | DFD Level 1 (processes) | Pipeline (9 DAGs) | User Journey
      Generator: `04_conceptual_models/generate_o4_diagrams.py`
- [x] Research Publication Portfolio updated to 9 papers (P9 added)
      `Research_Documents/iNHCES_Research_Publication_Portfolio.pdf`

- [x] O4 Step 1 — System Architecture (2026-04-26, AMBER)
      `04_Architecture_Diagram.mmd` (Mermaid, 7-layer)
      `O4_01_System_Architecture.pdf` (13pp: layer descriptions, 6 design decisions,
      JWT+RLS security, 10 integrations, 17 env vars, deployment topology)
      Generator: `04_conceptual_models/generate_o4_step1.py`

- [x] O4 Step 2 — Database Schema (2026-04-26, AMBER)
      `04_schema.sql` (16 tables: macro x5, material x3, unit_rates, market_prices,
      users, projects, predictions, reports, ml_models, audit_log; 7 enums; 2 views)
      `04_rls_policies.sql` (9 policy groups, 36 policies; service_role for Airflow/API)
      `04_seed_data.sql` (synthetic RED seed: 3 users, 5-yr macro, materials, 2 projects)
      `O4_02_Database_Schema.pdf` (16pp AMBER, full column definitions + setup guide)
      Generator: `04_conceptual_models/generate_o4_step2.py`

- [x] O4 Step 3 — Data Flow Diagrams (2026-04-26, AMBER)
      `04_DFD_Level0.mmd` (context: 9 ext. entities, all data flows)
      `04_DFD_Level1.mmd` (6 processes: Auth/Estimate/Ingest/ML/Report/Monitor; 3 data stores: Supabase/R2/MLflow)
      `04_User_Journey.mmd` (QS Professional 5 stages + Researcher 4 stages; scored 1-5)
      `04_Pipeline_Flow.mmd` (9 DAGs with cron schedules, sources, DB targets, retrain + PSI drift)
      `O4_03_Data_Flow_Diagrams.pdf` (9pp AMBER, DAG schedule table, design recommendations, consistency checklist)
      Generator: `04_conceptual_models/generate_o4_step3.py`

- [x] O4 Step 4 — Chapter 4 Write-up (2026-04-26, AMBER)
      `04_Chapter4_Conceptual_Models.md` + `O4_04_Chapter4_Conceptual_Models.pdf` (13pp)
      Sections 4.1-4.8: Intro, 7-layer architecture, DB design decisions, DFD model,
      pipeline + UX, Delphi traceability matrix (36 items), limitations, summary table

### ✅ O4 COMPLETE — 4 steps, 13 files, ~51 PDF pages

- [x] O5 COMPLETE — ML Model Benchmarking (2026-04-26)
      Step 1: 05_feature_engineering.py — 22 rows x 14 features; I(1)/I(2)* transforms; synthetic proxy (RED)
      Step 2: 05_model_benchmarking.py — 9 models; champion=LightGBM LOO-CV MAPE 13.66%; champion_model.pkl saved
      Step 3: 05_shap_analysis.py — TreeExplainer; near-zero SHAP (expected at n=22); bar + beeswarm PNGs
      Step 4: 05_mlflow_config.py + 05_model_promotion.py + 05_dags/nhces_retrain_weekly.py (6-task Airflow DAG)
      Step 5: 05_Chapter5_ML_Models_Results.md — benchmarking table, SHAP interpretation, MLOps design, limitations

- [x] O6 Agent 01 -- Project Plan (2026-04-26, AMBER)
      `nhces-frontend/O6_00_Agent01_Project_Plan.pdf` (14pp) + .md + generator
      Stack: Next.js 14 + FastAPI + Supabase + Railway + Vercel
      Design: Warm Ivory palette (Playfair Display + Lora + DM Sans)

### ✅ O6 BACKEND COMPLETE — Agent 04 (S1-S5)
- [x] S1: main.py + config.py + database.py + auth.py + requirements.txt + .env.example
- [x] S2: app/ml/inference.py (champion load/predict/CI) + feature_prep.py (14-feature vector) + explainer.py (SHAP)
- [x] S3: schemas/estimate.py + routers/estimate.py (POST /estimate: feature->predict->SHAP->Supabase->response)
- [x] S4: schemas (macro/project/report) + routers (GET /macro + /macro/history + CRUD /projects + POST+GET /reports + GET /pipeline) -- 17 routes total
- [x] S5: services/r2_storage.py + report_generator.py (fpdf2 4-page Warm Ivory PDF) + pipeline_monitor.py (Airflow REST)

### ✅ O6 FRONTEND S6-S8 COMPLETE — Agent 03
- [x] S6: package.json + lib/styles.ts (GS + Warm Ivory palette) + lib/api.ts (typed) + lib/auth.ts + lib/formatters.ts + app/layout.tsx (Google Fonts) + components/ui/* (Button/Card/Input/Badge/DataSourceBadge/LoadingSpinner) + Navbar + Footer
- [x] S7: app/page.tsx (full landing: hero/stats/steps/data-quality/CTA) + app/estimate/page.tsx (form + EstimateResult + ShapChart) -- USER APPROVED
- [x] S8: app/dashboard/page.tsx + components/dashboard/* (MacroSnapshot/ModelStatus/PipelineHealth/RecentPredictions) -- USER APPROVED

- [x] S9: app/projects/page.tsx + app/reports/page.tsx + app/macro/page.tsx -- USER APPROVED
- [x] UI-POLISH: Landing/Dashboard/Estimate redesigned as single-page no-scroll layouts -- USER APPROVED
- [x] Backend fix: get_optional_user; /projects+/reports return [] without auth; FastAPI running at :8000
- [x] S10: app/login/page.tsx + app/register/page.tsx + Navbar auth state (user badge + Log Out)
- [x] TEMPORAL PROJECTION (5yr cap -- <1yr, <3yr, <5yr):
      02_macro_analysis/forecast_macro.py (VAR h-step macro forecasts)
      05_ml_models/05_temporal_projection.py (compound inflation engine)
      nhces-backend/app/ml/temporal.py (FastAPI integration)
      nhces-frontend/components/estimate/TemporalChart.tsx (SVG chart + widening CI band)
      API: 4 projections returned -- 25% p.a. inflation derived from real World Bank CPI
      P3 + P5 draft papers updated with Section 5B (temporal projection methodology)

### ✅ O6 FRONTEND COMPLETE -- Agent 03 (S6-S10)
### ✅ O6-S11 COMPLETE -- Agent 05: Database Verification
- 04_db_functions.sql (5 functions: get_latest_macro_snapshot, get_user_project_summary, get_champion_model, log_audit_event, refresh_champion_flag)
- 04_db_indexes.sql (14 additional performance indexes)
- 04_db_verification.sql (14 SQL checks + 6 RLS policy tests)
- database.py updated: health_check(), get_macro_snapshot_from_db(), promote_champion_in_db()
- O6_11_Database_Verification.pdf (6pp: checklists, RLS guide, pre-launch checklist)

### 🔴 STOPPED AT -- O6-S12 (Agents 06+07: QA + Code Review)

### ⬜ O6 Remaining Sessions (3 sessions)
- [ ] O6-S12: Agents 06+07 -- Tests (nhces-backend/tests/) + Code review checklist
- [ ] O6-S13: Agent 08 -- README.md (backend + frontend) + API docs verification
- [ ] O6-S14: Agents 09+10 -- Dockerfile, railway.toml, vercel.json, deploy.yml, DAG config

### MANDATORY WORKFLOW RULES (O6)
1. Seek approval before every session
2. Show every new frontend page in browser before proceeding
- [ ] O4 Step 4: `04_Chapter4_Conceptual_Models.md` + PDF
- [ ] O5: ML model benchmarking pipeline (05_ml_models/)
- [ ] O6: FastAPI backend + Vanilla JS frontend + tests + CI/CD

## Placeholder Files Still to Implement
- `04_conceptual_models/*.sql`, `*.mmd` — O4 Steps 1-3
- `05_ml_models/*.py`, `05_dags/*.py` — O5
- `nhces-backend/app/**/*.py` — O6 backend
- `nhces-backend/tests/*.py` — O6 tests

## Key Variables
- **Target**: `cost_per_sqm` — Nigerian housing construction cost per sqm (NGN)
- **Features**: NGN/USD, NGN/EUR, NGN/GBP (exchange rates); CPI inflation; GDP growth;
  lending rate; Brent crude; cement price by region; iron rod price; PMS (petrol) price;
  NIQS unit rates; property listing prices (NGN/sqm by zone)

## ML Model Family
Ridge/Lasso (baseline) | RF/XGBoost/LightGBM (primary) | MLP (neural) | SVR
Champion: Stacking Ensemble (XGBoost + LightGBM + RF → Ridge meta-learner)
Performance targets: MAPE ≤ 15% | R² ≥ 0.90 | API response < 3 seconds

## Publication Portfolio (9 Papers)
| Paper | Target Journal | Status |
|-------|---------------|--------|
| P1 — PRISMA SLR | Construction Mgmt & Economics | ✅ Draft PDF |
| P2 — Delphi Requirements | Eng. Const. & Arch. Mgmt | ✅ Draft PDF |
| P3 — Macroeconomic Determinants | Construction Mgmt & Economics | ✅ Draft PDF |
| P4 — Automated Data Pipeline | Scientific Data | ⬜ Not started |
| P5 — ML Benchmarking | J. Const. Eng. & Mgmt (ASCE) | ⬜ Not started |
| P6 — MLOps Architecture | Expert Systems with Applications | ⬜ Not started |
| P7 — Full iNHCES System | Automation in Construction | ⬜ Not started |
| P8 — Housing Policy | Habitat International | ⬜ Not started |
| P9 — AI Research Simulation | Computers & Education / IETI | ✅ Draft PDF (26pp) |

## Session Resume Instructions
Read PROJECT_CONTEXT.md and BUILDWISE_CONTEXT.md (design system) for full detail. Then say:
"Continue the iNHCES build from O6-S12 (Agents 06+07 -- QA and Code Review)."

## O6 Backend API Summary (for Agent 03 reference)
Base URL (dev): http://localhost:8000
- POST /estimate -- ML cost prediction (returns cost_per_sqm, SHAP, data_freshness)
- GET  /macro -- Latest 7 macro variables with data_level badges
- GET  /macro/history?variable=ngn_usd&years=5 -- Historical series for charts
- GET/POST/PUT/DELETE /projects -- Project CRUD (JWT required)
- POST /reports -- Generate PDF report -> R2 -> presigned URL
- GET  /reports -- List user reports
- GET  /pipeline -- Airflow DAG health (researcher role required)
- GET  / -- Health check
