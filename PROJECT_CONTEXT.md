# iNHCES Project Context Document
**Intelligent National Housing Cost Estimating System**
TETFund NRF 2025 | Department of Quantity Surveying, ABU Zaria
**Last updated:** 2026-04-29  |  **Session:** O6 FULLY COMPLETE + DEPLOYED + REVIEW FREEZE. GitHub: https://github.com/baeconsultingeng-AI/iNHCES (master, latest: `9167a38`). System LIVE: https://i-nhces.vercel.app | https://inhces-production.up.railway.app. Post-deployment UI improvements applied (icons, 3D logo, navbar style, estimate transparency). ⛔ REVIEW FREEZE — no further code changes until research team review complete.

> **Purpose:** This document is the single source of truth for resuming development after any session interruption.
> When starting a new session (Copilot Chat, Claude extension, or Claude Code CLI), read this file first.

---

## ⚠️ GOVERNING FRAMEWORK — READ THIS BEFORE ANY WORK

**Every session, every output, every decision in this project is governed by the S2RF Governing Preamble:**

> 📄 `Research_Documents/00_S2RF_Governing_Preamble_iNHCES.pdf`
> Generator: `01_literature_review/generate_intro_document.py`

### What this means in practice

| Rule | Obligation |
|------|------------|
| **This is a simulation** | All current outputs are AI-assisted first-pass drafts. No output is final research until validated by the human team with real data. |
| **DATA SOURCE banners are mandatory** | Every PDF must have a DATA SOURCE DECLARATION page (GREEN / AMBER / RED) immediately after the cover. No exceptions. |
| **RED data must never be published** | Any PDF with a RED banner contains synthetic/hypothetical data. It MUST be replaced with real collected data before any publication, grant report, or public presentation. |
| **No AI-generated citations** | Never use a citation from an AI output without independently verifying it in Scopus, Web of Science, or the primary source. |
| **Disclose AI assistance** | Every published paper must include the standard AI Disclosure Statement (see Section 9 of the preamble document). |
| **Human sign-off required** | No simulated output advances to the next pipeline stage without review and approval by a named human researcher. |
| **AI is a tool, not an author** | AI (Claude / GitHub Copilot) does not qualify as an author. Human researchers bear full accountability for all outputs. |

### DATA SOURCE Colour Key (applies to all PDFs in this project)
| Colour | Meaning |
|--------|---------|
| 🟢 GREEN | Live data from a real API or official database. Cite the original source. |
| 🟡 AMBER | AI-authored template or framework. Researcher must validate and own before publication. |
| 🔴 RED | Synthetic / simulated data (NumPy seed or hardcoded estimates). MUST be replaced with real data. |

### When resuming any session
1. Read this file (PROJECT_CONTEXT.md) — check where we stopped
2. Review the preamble document obligations above before generating any new output
3. Apply the correct DATA SOURCE banner to every new PDF produced
4. Update this file after every completed step

---

## 1. Project Overview

| Item | Detail |
|------|--------|
| Full Name | Intelligent National Housing Cost Estimating System (iNHCES) |
| Grant | TETFund National Research Fund (NRF) 2025 |
| Institution | Department of Quantity Surveying, ABU Zaria |
| Methodology | Sequential Explanatory Mixed Methods (Creswell, 2014) |
| Research Objectives | O1 → O2 → O3 → O4 → O5 → O6 (six objectives, sequential) |

---

## 2. Technology Stack

| Layer | Technology | Hosting |
|-------|-----------|---------|
| Frontend | Next.js 14 (App Router, TypeScript, Warm Ivory design) | Vercel |
| Backend API | FastAPI (Python 3.10+) | Railway |
| Database | Supabase PostgreSQL | Supabase |
| ML Registry | MLflow Tracking Server | Railway |
| File Storage | Cloudflare R2 | Cloudflare |
| Orchestration | Apache Airflow | Railway |
| CI/CD | GitHub Actions | GitHub |

---

## 3. Project Root

```
c:\Users\MacBook\Desktop\BaeSoftIA\INHCES\iNHCES\
```

---

## 4. Complete Folder Structure

```
iNHCES/
├── CLAUDE.md                          ← Claude extension memory file (auto-read)
├── PROJECT_CONTEXT.md                 ← THIS FILE — session resumption guide
├── 01_literature_review/
│   ├── generate_intro_document.py               ← generator for S2RF Governing Preamble PDF
├── 02_macro_analysis/
│   ├── data/raw/                      ← CBN, EIA, World Bank CSVs land here
│   ├── data/processed/                ← cleaned datasets land here
│   ├── results/                       ← charts, tables from analysis
│   ├── shap_results/                  ← SHAP plots and tables
│   ├── fetch_worldbank.py             ← ✅ IMPLEMENTED (World Bank API, live data)
│   ├── fetch_eia_oil.py               ← ✅ IMPLEMENTED (EIA/FRED, synthetic fallback)
│   ├── fetch_cbn_fx.py                ← ✅ IMPLEMENTED (FRED/CBN, synthetic fallback)
│   ├── stationarity_analysis.py       ← PLACEHOLDER
│   ├── var_vecm_model.py              ← PLACEHOLDER
│   └── shap_variable_selection.py     ← PLACEHOLDER
├── 03_requirements/
│   ├── delphi/                        ← Delphi Round 1/2/3 instruments land here
│   ├── srs/                           ← SRS document lands here
│   └── use_cases/                     ← UML use cases land here
├── 04_conceptual_models/
│   ├── 04_Architecture_Diagram.mmd    ← PLACEHOLDER
│   ├── 04_DFD_Level0.mmd             ← PLACEHOLDER
│   ├── 04_DFD_Level1.mmd             ← PLACEHOLDER
│   ├── 04_Pipeline_Flow.mmd          ← PLACEHOLDER
│   ├── 04_User_Journey.mmd           ← PLACEHOLDER
│   ├── 04_rls_policies.sql           ← PLACEHOLDER
│   ├── 04_schema.sql                 ← PLACEHOLDER
│   └── 04_seed_data.sql              ← PLACEHOLDER
├── 05_ml_models/
│   ├── 05_dags/
│   │   └── nhces_retrain_weekly.py   ← PLACEHOLDER
│   ├── 05_feature_engineering.py     ← PLACEHOLDER
│   ├── 05_mlflow_config.py           ← PLACEHOLDER
│   ├── 05_model_benchmarking.py      ← PLACEHOLDER
│   ├── 05_model_promotion.py         ← PLACEHOLDER
│   └── 05_shap_analysis.py           ← PLACEHOLDER
├── nhces-backend/
│   ├── app/
│   │   ├── ml/
│   │   │   ├── explainer.py          ← PLACEHOLDER
│   │   │   ├── feature_prep.py       ← PLACEHOLDER
│   │   │   └── inference.py          ← PLACEHOLDER
│   │   ├── models/                   ← EMPTY
│   │   ├── pipeline/                 ← EMPTY
│   │   ├── routers/
│   │   │   ├── estimate.py           ← PLACEHOLDER
│   │   │   ├── macro.py              ← PLACEHOLDER
│   │   │   ├── pipeline.py           ← PLACEHOLDER
│   │   │   ├── projects.py           ← PLACEHOLDER
│   │   │   └── reports.py            ← PLACEHOLDER
│   │   ├── schemas/                  ← EMPTY
│   │   └── services/
│   │       ├── pipeline_monitor.py   ← PLACEHOLDER
│   │       ├── r2_storage.py         ← PLACEHOLDER
│   │       └── report_generator.py   ← PLACEHOLDER
│   └── tests/
│       ├── test_api.py               ← PLACEHOLDER
│       ├── test_estimate.py          ← PLACEHOLDER
│       └── test_pipeline.py          ← PLACEHOLDER
├── nhces-frontend/                   ← EMPTY (.gitkeep only)
├── .github/workflows/                ← EMPTY (.gitkeep only)
└── Research_Documents/
    ├── 00_S2RF_Governing_Preamble_iNHCES.pdf    ← ✅ S2RF GOVERNING PREAMBLE — read first
    ├── 01_S2RF_Claude_AI_Workflow_Guide_iNHCES.pdf
    ├── 03_iNHCES_Research_Publication_Portfolio.pdf
    ├── 04_iNHCES_Live_Data_Infrastructure_Guide.pdf
    ├── generate_publication_portfolio.py   ← IMPLEMENTED (working PDF generator)
    └── [other PDFs]
```

**Legend:** PLACEHOLDER = file exists with `# PLACEHOLDER` comment only, not yet implemented.

---

## 5. Current Development Status

### ✅ COMPLETED
- [x] Full project folder structure scaffolded
- [x] CLAUDE.md created (Claude extension memory file)
- [x] PROJECT_CONTEXT.md created (this file)
- [x] Research_Documents/generate_publication_portfolio.py — working PDF generator using fpdf2
- [x] O1 Step 1 — PRISMA Protocol, Search Strings, Data Extraction Template (2026-04-23)
  ✅ DATA SOURCE: REAL RESEARCH INSTRUMENTS
  - 01_PRISMA_Protocol.pdf -- AI-authored PICO + IC/EC framework based on PRISMA 2020 (Page et al., 2021);
    no fabricated data; PROSPERO registration number is a placeholder [INSERT AFTER REGISTRATION]
  - 02_Search_Strings.pdf -- AI-designed Boolean strings; real keyword choices for this domain;
    hit count columns blank (to be filled during Phase 2 execution)
  - 03_Data_Extraction_Template.pdf -- AI-designed extraction template; no studies extracted yet;
    example entries (S001, Aibinu, A.) are illustrative placeholders only
  - DATA SOURCE PAGE added to each PDF (green banner)
- [x] O1 Step 2 -- Methodology Taxonomy Table + ML Method Comparison (2026-04-23)
  ⚠️ DATA SOURCE: AI-GENERATED TEMPLATES (not from real database search)
  - DATA SOURCE PAGE added to each PDF (amber banner) -- no change to existing content
  - `04_Methodology_Taxonomy_Table.pdf` -- structured template populated from AI training knowledge
    (Skitmore, Dania, Kim et al. citations are real papers; content is AI-synthesised, NOT PRISMA-extracted)
  - `05_ML_Method_Comparison.pdf` -- AI-synthesised model comparison from training knowledge
  - PURPOSE: Shows research team exactly what to populate with real extracted data after Phase 2 SLR execution
  - ACTION: Replace content with real extracted data after database searches are complete
- [x] O1 Step 3 -- Literature Review Draft + Gap Analysis Table + Included Studies Bibliography (2026-04-23)
  ⚠️ DATA SOURCE: AI-GENERATED TEMPLATES (not from real database search)
  - 06_Literature_Review_Draft.pdf, 07_Gap_Analysis_Table.pdf -- DATA SOURCE pages added (amber/red banners)
  - 08_Included_Studies_Bibliography.pdf -- DATA SOURCE page added (amber banner);
    '87 studies' is FABRICATED -- not from real PRISMA search
  - `06_Literature_Review_Draft.pdf` -- AI-generated draft in PRISMA style
    FABRICATED COUNTS: "1,847 screened records / 87 primary studies" -- these numbers are NOT REAL
    These must be replaced with actual counts from the live database search
  - `07_Gap_Analysis_Table.pdf` -- AI-generated gap analysis from training knowledge; references "87 studies" (fabricated)
  - `08_Included_Studies_Bibliography.pdf` -- illustrative reference list; NOT a real screened-and-included set
  - PURPOSE: Templates showing the research team the structure and content standard required
  - ACTION: All three must be regenerated with real extracted data after Phase 2 SLR execution
- [x] 01_S2RF_Claude_AI_Workflow_Guide_iNHCES.pdf regenerated with 27 "WHY THIS STEP IS REQUIRED" rationale boxes across all 6 objectives (2026-04-23)
  - Generator script: `Research_Documents/generate_claude_assistance_guide.py`
  - Output: `Research_Documents/01_S2RF_Claude_AI_Workflow_Guide_iNHCES.pdf`
- [x] O1 Step 4 -- QS Survey Instrument + SPSS Analysis Plan (2026-04-24)
  ✅ DATA SOURCE: REAL RESEARCH INSTRUMENTS
  - 09_QS_Survey_Instrument.pdf -- instrument is field-ready; no survey data collected yet;
    [RESEARCHER EMAIL] / [PI PHONE] / [DEADLINE DATE] / [INSERT REF] are placeholders to fill before printing
  - 10_SPSS_Analysis_Plan.pdf -- analysis plan is ready for SPSS execution; no data yet;
    all procedure paths reference the survey instrument (09_)
  - DATA SOURCE PAGE added to each PDF (green banner)
- [x] O1 Step 5 -- Hypothetical Survey Analysis -- O1 FULLY CLOSED (2026-04-24)
  🔴 DATA SOURCE: HYPOTHETICAL / SIMULATED DATA (NumPy seed=2025, n=60 -- NOT real responses)
  - 11_Survey_Descriptives.pdf -- demographic + practice frequencies; ALL SYNTHETIC
  - 12_RII_Parameter_Rankings.pdf -- RII values, Mann-Whitney U; ALL SYNTHETIC
  - 13_Reliability_EFA.pdf -- Cronbach alpha, KMO, factor loadings; ALL SYNTHETIC
  - 14_TAM_Analysis.pdf -- TAM path coefficients, R^2; ALL SYNTHETIC
  - 15_O1_Survey_Summary.pdf -- synthesised findings from 11-14; ALL SYNTHETIC
  - DATA SOURCE PAGE added to each PDF (red banner) with mandatory replacement notice
  - NHCES_Hypothetical_Survey_Data.csv (n=60, seed=2025) -- also synthetic
  - Replace CSV with field survey data and re-run run_o1_hypothetical_survey.py to update all 5 PDFs
- [x] PRISMA 2020 27-Item Checklist Status Document (regenerated 2026-04-25)
  - Script: `01_literature_review/generate_prisma_checklist.py`
  - Output: `01_literature_review/16_PRISMA_Checklist_Status.pdf`
  - 16 items COMPLETE | 1 PARTIAL (Item 24 PROSPERO registration) | 10 PENDING (awaiting search execution)
  - **Expanded document (v2) — new sections added:**
    - Page 2: Phase 1 vs Phase 2 explanation (what was done vs what fieldwork remains)
    - Page 3: Phase 1 summary table — 17 items with deliverable and what was done
    - Pages 4-8: Phase 2 SLR Execution Guide — Steps A through K with full instructions:
      - Step A: PROSPERO registration (prospero.york.ac.uk) — IMMEDIATE action
      - Step B: Database search in all 10 databases using 02_Search_Strings.pdf
      - Step C: Deduplication (Zotero / Rayyan)
      - Step D: Dual-reviewer title/abstract screening (Rayyan recommended)
      - Step E: Full-text retrieval (institutional access + ILL)
      - Step F: Dual-reviewer full-text screening with EC codes
      - Step G: Data extraction per 03_Data_Extraction_Template.pdf → NHCES_SLR_Extraction_Master.csv
      - Step H: CASP quality appraisal (parallel with G)
      - Step I: Narrative synthesis across RQ1-RQ4 → populate real taxonomy and gap tables
      - Step J: Complete PRISMA flow diagram with real counts
      - Step K: Write Paper P1 (Construction Management and Economics)
    - Pages 9+: Status legend, progress summary by section, full 27-item checklist with phase bands
    - Final page: 11-item action plan with SLR step cross-references
  - CRITICAL: Item 24 -- register at prospero.york.ac.uk BEFORE any database search begins

- [x] S2RF Governing Preamble Document (2026-04-25, updated 2026-04-27)
  - `Research_Documents/00_S2RF_Governing_Preamble_iNHCES.pdf` [OK]
  - `01_literature_review/generate_intro_document.py` — generator script
  - 11 sections, ~12 pages: Introduction, iNHCES overview, simulation framework, what the simulation IS and IS NOT,
    research ethics & academic integrity (COPE/ICMJE/Elsevier/Springer/UNESCO), simulation-to-research pipeline,
    team obligations, AI citation guidelines, key references
  - **This document GOVERNS all iNHCES outputs.** Every session must comply with its rules.
  - DATA SOURCE: GREEN (AI-authored policy document, not data-bearing)

- [x] O2 Step 1 -- Data Collection Scripts (2026-04-24)
  - `02_macro_analysis/fetch_worldbank.py` [OK]
    - World Bank public API (no key) -- GDP growth, CPI inflation, lending rate for Nigeria 2000-2024
    - Raw: `data/raw/worldbank_nigeria.csv` | Processed: `data/processed/worldbank_nigeria_processed.csv`
    - PDF: `O2_01_WorldBank_Macro_Nigeria.pdf` (live data -- World Bank API)
  - `02_macro_analysis/fetch_eia_oil.py` [OK]
    - Three-tier: EIA API (EIA_API_KEY env var) > FRED API (FRED_API_KEY env var) > Synthetic fallback
    - Currently using: SYNTHETIC fallback (hardcoded EIA/BP historical values, annual 2000-2024)
    - Raw: `data/raw/eia_brent_oil.csv` | Processed: `data/processed/eia_brent_oil_processed.csv`
    - PDF: `O2_02_Brent_Oil_Prices.pdf` (SYNTHETIC DATA banner displayed)
  - `02_macro_analysis/fetch_cbn_fx.py` [OK]
    - Two-tier: FRED API (FRED_API_KEY env var) > Synthetic fallback
    - Currently using: SYNTHETIC fallback (CBN/IMF/WB historical values, annual 2000-2024)
    - NGN/USD direct; NGN/EUR and NGN/GBP as cross-rates via FRED DEXUSEU, DEXUSGB
    - Raw: `data/raw/cbn_fx_rates.csv` | Processed: `data/processed/cbn_fx_rates_processed.csv`
    - PDF: `O2_03_NGN_Exchange_Rates.pdf` (SYNTHETIC DATA banner displayed)
  - To replace synthetic with live data: set `EIA_API_KEY` and/or `FRED_API_KEY` env vars and re-run scripts

- [x] O2 Step 2 -- Stationarity Analysis (2026-04-26)
  - `02_macro_analysis/stationarity_analysis.py` [OK]
  - ADF + KPSS unit root tests on all 7 macro variables at levels and first differences
  - Integration orders: GDP growth I(1), CPI I(1), lending rate I(1), Brent I(1); NGN/USD/EUR/GBP I(2)*
  - Output: `O2_04_Stationarity_Analysis.pdf` (AMBER DATA SOURCE banner)
  - CSV: `data/processed/stationarity_results.csv` (14 columns per variable incl. ADF/KPSS stats)

- [x] O2 Step 3 -- VAR/VECM Models (2026-04-26)
  - `02_macro_analysis/var_vecm_model.py` [OK]
  - Johansen trace test: cointegration rank = 0 (no long-run equilibrium at 5% level, synthetic data)
  - Model selected: VAR(diff, lag=1) on first-differenced I(1) variables
  - IRF and FEVD charts generated for first 3 variables
  - Output: `O2_05_VAR_VECM_Models.pdf` (AMBER DATA SOURCE banner)
  - CSV: `results/var_vecm_results.csv`

- [x] O2 Step 4 -- SHAP Variable Selection (2026-04-26)
  - `02_macro_analysis/shap_variable_selection.py` [OK]
  - XGBoost (n=200, depth=3, lr=0.05) + SHAP TreeExplainer on synthetic housing cost proxy
  - SHAP ranking: NGN/USD (45%) > CPI (25.5%) > NGN/EUR (11.6%) > Brent (10.9%) > NGN/GBP > GDP > lending
  - Proxy range: NGN 67,927 -- NGN 311,676 / sqm (synthetic -- pipeline validation only)
  - Output: `O2_06_SHAP_Variable_Selection.pdf` (RED DATA SOURCE banner -- fully synthetic proxy)
  - CSV: `shap_results/shap_importance.csv`

### ✅ DRAFT PAPERS — P1, P2, P3, P4, P5, P6, P9 Created
- **P1** `Draft AI Papers/P1_PRISMA_SLR_Draft.pdf` — PRISMA SLR (AMBER). Target: CME.
- **P2** `Draft AI Papers/P2_Delphi_Requirements_Draft.pdf` — Delphi requirements (RED/AMBER). Target: ECAM.
- **P3** `Draft AI Papers/P3_Macroeconomic_Determinants_Draft.pdf` — Macro determinants (AMBER/RED). Target: CME.
- **P4** `Draft AI Papers/P4_Data_Pipeline_Draft.pdf` — Cloud-native data pipeline (AMBER/RED, 10pp). Target: Scientific Data.
- **P5** `Draft AI Papers/P5_ML_Benchmarking_Draft.pdf` — ML benchmarking with live results table (RED, 10pp). Target: ASCE JCEM.
- **P6** `Draft AI Papers/P6_MLOps_Architecture_Draft.pdf` — MLOps champion-challenger + PSI drift (AMBER, 12pp). Target: Expert Systems with Applications.
- **P9** `Draft AI Papers/P9_AI_Research_Simulation_Draft.pdf` — AI research simulation framework (AMBER, 27pp). Target: Computers & Education | IETI.
  - Documents the Simulation-to-Publication Framework (S2PF) applied in iNHCES.
  - Sections: Abstract, Intro, Background, iNHCES Context, S2PF Design (4 rules), **Section 4.5 Environment Setup** (Tables 7-9: system requirements, package list, 11-item verification checklist; Steps 1-6: VS Code, Claude Code CLI, Copilot, Python venv, directory init, first session), Implementation Walkthrough (O1-O3), Ethics Compliance Table, Pedagogical Workshop Design, Discussion, Conclusions, AI Disclosure, References, Appendices A-C + **Appendix D** (full replication guide: Windows install sequence, CLAUDE.md template, SESSION_START prompt, PROJECT_CONTEXT.md template, macOS/Linux equivalents).
  - **PLACEHOLDER before submission**: ABU Zaria pilot workshop (n>=20 PG students) + pre/post survey data + IRB approval.
  - **Unique contribution**: First published account of a full-scale, ethics-compliant AI research simulation pipeline for a nationally funded system development project, with complete environment replication guide.
- Generated by: `Draft AI Papers/generate_p1_slr_draft.py`, `generate_p2_delphi_draft.py`, `generate_p3_macro_draft.py`, `generate_p9_ai_simulation_draft.py`

### ✅ O3 COMPLETE — Requirements Modelling
| Deliverable | File | Data Source | Status |
|-------------|------|-------------|--------|
| Stakeholder Register | `03_requirements/O3_01_Stakeholder_Register.pdf` | GREEN | Complete |
| Delphi Round 1 Instrument | `03_requirements/O3_02_Delphi_Round1_Instrument.pdf` | AMBER | Complete |
| Delphi Round 2 Instrument | `03_requirements/O3_03_Delphi_Round2_Instrument.pdf` | AMBER | Complete |
| Delphi Round 2 Analysis | `03_requirements/O3_04_Delphi_Round2_Analysis.pdf` | RED (synthetic) | Complete |
| Delphi Round 3 Instrument | `03_requirements/O3_05_Delphi_Round3_Instrument.pdf` | AMBER | Complete |
| Delphi Final Consensus | `03_requirements/O3_06_Delphi_Final_Consensus.pdf` | RED (synthetic) | Complete |
| SRS IEEE 830 | `03_requirements/O3_07_SRS_IEEE830.pdf` | AMBER | Complete |
| UML Use Cases | `03_requirements/O3_08_UML_Use_Cases.pdf` | GREEN | Complete |
| Delphi CSV | `03_requirements/delphi/delphi_results.csv` | RED (synthetic) | Complete |
| Round1/2/3 MD | `03_requirements/delphi/Round1/2/3.md` | AMBER | Complete |
| SRS MD | `03_requirements/srs/03_SRS_NHCES_IEEE830.md` | AMBER | Complete |
| Use Cases MD | `03_requirements/use_cases/03_UML_Use_Cases.md` | GREEN | Complete |

**Delphi simulation**: n=20 experts (synthetic, seed=42), 38 items, 36/40 consensus.
**Excluded items**: B6 (procurement method), C6 (stacking ensemble mandate), E5 (mobile usability), G2 (sensitivity analysis).
**Generator script**: `03_requirements/generate_o3_pdfs.py`

- [x] O4 Step 1 — System Architecture (2026-04-26)
  ⚠️ DATA SOURCE: AMBER (AI-designed from O3 Delphi consensus + Research Advisory Framework)
  - `04_conceptual_models/04_Architecture_Diagram.mmd` — Mermaid source (7-layer architecture)
  - `04_conceptual_models/O4_01_System_Architecture.pdf` — 13-page architecture document
  - `04_conceptual_models/generate_o4_step1.py` — generator script
  - Covers: 7-layer summary table, layer-by-layer descriptions (Users → Presentation → API → ML → Data → Storage → Pipeline), 6 design decisions (Vanilla JS, FastAPI, Supabase, MLflow, R2, Airflow), security architecture (JWT + RLS + 3 roles), external integrations (10 sources), env vars reference (17 vars), deployment topology, CI/CD, Mermaid source appendix
  - VALIDATE before O6 build: platform tiers, NIQS MoU, scraper ToS, Delphi item coverage

- [x] O4 Step 2 — Database Schema (2026-04-26)
  ⚠️ DATA SOURCE: AMBER (AI-designed from O3 SRS + O4 Step 1 architecture)
  - `04_conceptual_models/04_schema.sql` — 16 tables, 7 enums, 2 views, triggers
  - `04_conceptual_models/04_rls_policies.sql` — RLS policies for all 16 tables (9 policy groups)
  - `04_conceptual_models/04_seed_data.sql` — Synthetic test data (RED): 3 users, 5 yrs macro, 8 cement, 7 steel, 7 PMS, 15 unit rates, 8 market prices, 2 projects, 1 prediction, 1 ml_model
  - `04_conceptual_models/O4_02_Database_Schema.pdf` — 16-page schema document
  - `04_conceptual_models/generate_o4_step2.py` — generator script
  - Key tables: macro_fx/cpi/gdp/interest/oil | material_cement/steel/pms | unit_rates | market_prices | projects | predictions | reports | ml_models | audit_log | users
  - Views: v_latest_macro | v_champion_model
  - VALIDATE: Run SQL files in Supabase before O6 build; replace seed user UUIDs with real auth.users IDs

- [x] O4 Step 3 — Data Flow Diagrams (2026-04-26)
  ⚠️ DATA SOURCE: AMBER (AI-authored from O3 SRS + O4 Steps 1-2)
  - `04_conceptual_models/04_DFD_Level0.mmd` — Context diagram (9 ext. entities, all data flows)
  - `04_conceptual_models/04_DFD_Level1.mmd` — Process decomposition (6 processes, 3 data stores)
  - `04_conceptual_models/04_User_Journey.mmd` — QS Professional (5 stages, 21 touchpoints) + Researcher/PI (4 stages, 9 touchpoints); satisfaction scored 1-5
  - `04_conceptual_models/04_Pipeline_Flow.mmd` — All 9 Airflow DAGs with cron schedules, sources, targets, retrain pipeline, PSI drift detection
  - `04_conceptual_models/O4_03_Data_Flow_Diagrams.pdf` — 9-page document with descriptions, flow tables, DAG schedule reference, design recommendations, consistency checklist
  - `04_conceptual_models/generate_o4_step3.py` — generator script
  - VALIDATE: render all .mmd files in mermaid.live; verify 36 Delphi items traceable to DFD Level 1 processes

- [x] O4 Step 4 — Chapter 4 Write-up (2026-04-26)
  ⚠️ DATA SOURCE: AMBER (AI-authored synthesis of O4 Steps 1-3)
  - `04_conceptual_models/04_Chapter4_Conceptual_Models.md` — Full chapter markdown
  - `04_conceptual_models/O4_04_Chapter4_Conceptual_Models.pdf` — 13-page PDF
  - `04_conceptual_models/generate_o4_step4.py` — generator script
  - Sections: Intro, Architecture (7-layer, 4 rationale boxes), DB Design (16 tables, JSONB decisions, 3NF), DFD Model (Level 0 + 1), Pipeline + UX (DAG schedule table, 3 UX pain points), Traceability Matrix (36 Delphi items -> architecture), Limitations, Chapter Summary (O4 deliverables table), References
  - Feeds into: Paper P4 (Scientific Data) + Paper P7 (Automation in Construction)

### ✅ O4 COMPLETE — Conceptual Models (4 steps, 13 files, ~51 PDF pages)

| Deliverable | File | Pages | Data Level |
|-------------|------|-------|------------|
| System Architecture | O4_01_System_Architecture.pdf | 13 | AMBER |
| Architecture Diagram | 04_Architecture_Diagram.mmd | — | AMBER |
| Database Schema | 04_schema.sql | — | AMBER |
| RLS Policies | 04_rls_policies.sql | — | AMBER |
| Seed Data | 04_seed_data.sql | — | RED |
| Database Schema Doc | O4_02_Database_Schema.pdf | 16 | AMBER |
| DFD Level 0 | 04_DFD_Level0.mmd | — | AMBER |
| DFD Level 1 | 04_DFD_Level1.mmd | — | AMBER |
| User Journey | 04_User_Journey.mmd | — | AMBER |
| Pipeline Flow | 04_Pipeline_Flow.mmd | — | AMBER |
| DFD Document | O4_03_Data_Flow_Diagrams.pdf | 9 | AMBER |
| Chapter 4 Markdown | 04_Chapter4_Conceptual_Models.md | — | AMBER |
| Chapter 4 PDF | O4_04_Chapter4_Conceptual_Models.pdf | 13 | AMBER |

- [x] O5 Step 1 — Feature Engineering (2026-04-26)
  ⚠️ DATA SOURCE: AMBER/RED — World Bank GREEN; EIA+FX RED synthetic; target RED
  - `05_ml_models/05_feature_engineering.py` — loads O2 CSVs, applies I(1)/I(2)* transforms, builds 14-feature matrix (22 rows), synthetic proxy target, saves to `05_ml_models/data/processed/`
  - `05_ml_models/O5_01_Feature_Engineering.pdf` — 3-page report (feature table, target description, train/val/test split)

- [x] O5 Step 2 — Model Benchmarking (2026-04-26)
  🔴 DATA SOURCE: RED — all metrics from synthetic proxy
  - `05_ml_models/05_model_benchmarking.py` — LOO-CV benchmarking of 9 models; champion = LightGBM (LOO-CV MAPE 13.66%); saves `champion_model.pkl` and `benchmarking_results.csv`
  - `05_ml_models/O5_02_Model_Benchmarking.pdf` — 3-page results with full comparison table
  - Champion: LightGBM (LOO-CV MAPE 13.66% — MEETS <=15% target on synthetic data)

- [x] O5 Step 3 — SHAP Analysis (2026-04-26)
  🔴 DATA SOURCE: RED — SHAP from synthetic proxy (near-zero at n=22)
  - `05_ml_models/05_shap_analysis.py` — TreeExplainer on LightGBM; bar chart + beeswarm PNG; saves `shap_importance_o5.csv`
  - `05_ml_models/O5_03_SHAP_Analysis.pdf` — 5-page report with comparison to O2 rankings

- [x] O5 Step 4 — MLOps Pipeline (2026-04-26)
  ⚠️ DATA SOURCE: AMBER — code; no data
  - `05_ml_models/05_mlflow_config.py` — MLflowLogger class, promotion decision, graceful fallback to local ./mlruns/
  - `05_ml_models/05_model_promotion.py` — ModelPromoter class (MLflow registry + Supabase is_champion update + audit_log)
  - `05_ml_models/05_dags/nhces_retrain_weekly.py` — 6-task Airflow DAG (assemble_features -> train_challengers -> train_stacking -> evaluate_compare -> promote_if_better -> audit_and_notify)

- [x] O5 Step 5 — Chapter 5 (2026-04-26)
  🔴 DATA SOURCE: RED (results) + AMBER (methodology)
  - `05_ml_models/05_Chapter5_ML_Models_Results.md` — Full chapter: feature engineering, benchmarking results table, SHAP interpretation, MLOps design, limitations, references

### ✅ O5 COMPLETE — ML Models (5 steps)

- [x] O6-S1 -- Agent 04: Backend Core (2026-04-26)
  - `nhces-backend/requirements.txt` + `.env.example` + `app/__init__.py`
  - `nhces-backend/app/config.py` -- Pydantic Settings (all env vars)
  - `nhces-backend/app/database.py` -- Supabase service_role + anon clients
  - `nhces-backend/app/auth.py` -- JWT middleware, CurrentUser, require_researcher/admin
  - `nhces-backend/app/main.py` -- FastAPI app, CORS, lifespan, GET / + GET /health
  - All modules verified: import cleanly, health routes registered

- [x] O6-S2 -- Agent 04: ML Inference Engine (2026-04-26)
  - `nhces-backend/app/ml/__init__.py`
  - `nhces-backend/app/ml/inference.py` -- load champion .pkl (R2 -> local -> synthetic fallback), predict(), confidence interval via MAPE, memory cache
  - `nhces-backend/app/ml/feature_prep.py` -- fetch 3-yr Supabase macro series, compute 14 features (diffs + returns + lags), RED fallback
  - `nhces-backend/app/ml/explainer.py` -- TreeExplainer SHAP, top-N features, get_shap_labels() for UI, uniform fallback
  - Verified: LightGBM champion loads from O5 pkl; predict() returns NGN 122,987/sqm; SHAP computed=True

- [x] O6-S3 -- Agent 04: /estimate endpoint (2026-04-26)
  - `nhces-backend/app/schemas/__init__.py` + `app/schemas/estimate.py`
    - EstimateRequest (BuildingType, ConstructionType, NigeriaZone enums; floor_area, location fields)
    - EstimateResponse (prediction_id, cost_per_sqm, total_cost, CI, SHAP items, freshness, is_synthetic)
    - ShapItem model for frontend ShapChart
  - `nhces-backend/app/routers/estimate.py` -- POST /estimate: feature_prep -> inference -> SHAP -> Supabase log -> response
  - `nhces-backend/app/main.py` updated: estimate router wired and registered at /estimate
  - Verified: /estimate route registered; EstimateRequest validates; all imports clean

- [x] O6-S4 -- Agent 04: Remaining endpoints (2026-04-26)
  - Schemas: `app/schemas/macro.py`, `app/schemas/project.py`, `app/schemas/report.py`
  - `app/routers/macro.py` -- GET /macro (snapshot with data_level per var), GET /macro/history?variable=&years=
  - `app/routers/projects.py` -- GET/POST/PUT/DELETE /projects (RLS via user_id filter, pagination)
  - `app/routers/reports.py` -- POST /reports (PDF gen + R2 upload + presigned URL), GET /reports (list with fresh URLs)
  - `app/routers/pipeline.py` -- GET /pipeline (Airflow REST API with graceful fallback; requires researcher role)
  - All 5 routers wired in main.py; 17 routes verified

- [x] O6-S5 -- Agent 04: Services (2026-04-26)
  - `nhces-backend/app/services/__init__.py`
  - `nhces-backend/app/services/r2_storage.py` -- upload_bytes, download_bytes, generate_presigned_url, delete_object; graceful fallback when R2 not configured
  - `nhces-backend/app/services/report_generator.py` -- fpdf2 4-page PDF with Warm Ivory palette (cover, cost summary, SHAP bar chart, disclaimers); build_report_pdf() returns (bytes, page_count)
  - `nhces-backend/app/services/pipeline_monitor.py` -- Airflow REST API queries (DAG list, last run, trigger); get_overall_health(); graceful fallback
  - Verified: test_report.pdf generated (6,375 bytes, 4 pages); R2 dev fallback works; health logic correct

### ✅ O6 BACKEND COMPLETE (Agent 04 -- Sessions S1-S5)

- [x] O6-S6 -- Agent 03: Frontend Design System (2026-04-26)
  - package.json, tsconfig.json, next.config.js, .env.local.example, vercel.json
  - `lib/styles.ts` -- GS object + COLOURS + FONTS + DATA_SOURCE_CONFIG + ANIMATION_CSS (Warm Ivory)
  - `lib/api.ts` -- typed fetch wrapper, all 8 endpoints, TypeScript interfaces
  - `lib/formatters.ts` -- formatNGN, formatNGNPerSqm, formatMAPE, formatDate, formatSqm
  - `lib/auth.ts` -- Supabase SSR browser client, getSession, signOut
  - `app/layout.tsx` -- root layout with Playfair Display + Lora + DM Sans (next/font/google)
  - `components/ui/` -- Button, Card, Input/Select/Textarea, Badge, DataSourceBadge, LoadingSpinner
  - `components/layout/` -- Navbar (sticky, active links), Footer
  - `app/page.tsx` -- placeholder home page
  - Build: 0 errors. Dev server confirmed running at http://localhost:3000

- [x] O6-S7 -- Agent 03: Landing + Estimate pages (2026-04-26)
  - `app/page.tsx` -- full landing page: hero (Playfair 52px), stats strip (4 numbers), How it Works (3 cards), Data Quality (3 DataSourceBadge), CTA
  - `app/estimate/page.tsx` -- EstimateForm (7 fields) + EstimateResult (cost figure, total box, model info, DataSourceBadge, ShapChart horizontal bars)
  - DataSourceBadge re-exports DataSourceLevel type
  - Build: 0 errors. Routes: / and /estimate both compile.

- [x] O6-S8 -- Agent 03: Dashboard page (2026-04-26)
  - `components/dashboard/MacroSnapshot.tsx` -- 7 macro variables with DataSourceBadge per row, live /macro fetch, graceful error state
  - `components/dashboard/ModelStatus.tsx` -- champion model card (LightGBM, 13.66% MAPE, O5 facts), target met badge
  - `components/dashboard/PipelineHealth.tsx` -- 9 DAGs with state icons (tick/cross/dash), schedule, data level; graceful Airflow error
  - `components/dashboard/RecentPredictions.tsx` -- empty state with CTA to /estimate
  - `app/dashboard/page.tsx` -- 4-stat header row + 2-column macro/model grid + 2-column pipeline/predictions grid
  - Build: 0 errors. Routes: /, /estimate, /dashboard all compile.

- [x] O6-UI-POLISH -- Agent 03: Single-page UI redesign (2026-04-26)
  - Landing page: 2-column viewport-fill layout (hero left, step cards + badges right), stats strip, footer nav bar -- no scroll
  - Dashboard: header strip + 6 stat pills + 3-column grid (Macro|Model|Pipeline+Recent) -- no scroll
  - Estimate page: always-two-column centred (max-width 1100px), compact 3-row form, placeholder panel -> result panel -- no scroll
  - All dashboard cards made compact (tight padding, smaller fonts, overflow-y: auto within cards)
  - USER APPROVED all three pages

- [x] O6-S9 -- Agent 03: Projects + Reports + Macro pages (2026-04-26)
  - `app/projects/page.tsx` -- project card grid, NewProjectModal (7-field form), delete with confirm, empty state, graceful backend error
  - `app/reports/page.tsx` -- report table (project ID, date, size, expiry status), Download PDF button opens presigned URL, empty state CTA
  - `app/macro/page.tsx` -- variable selector sidebar (7 variables with DataSourceBadge), current value card (large accent number), SVG line chart (10-year trend), graceful backend error
  - Build: 0 TypeScript errors. All 6 routes compile: /, /estimate, /dashboard, /projects, /reports, /macro

- [x] O6-S10 -- Agent 03: Login + Register pages (2026-04-27)
  - lib/auth.ts: signIn(), signUp(), signOut(), getCurrentUser() added
  - app/login/page.tsx: centred card, email+password, Supabase signIn, redirect to /dashboard
  - app/register/page.tsx: full name, email, password x2, institution, role picker (QS/Researcher), email verification flow
  - Navbar.tsx: live auth state (useEffect + onAuthStateChange); user avatar badge + Log Out when authenticated
  - Build: 0 errors. All 8 routes compile.

### ✅ O6 FRONTEND COMPLETE -- Agent 03 (S6-S10, all 8 pages)

- [x] O6-S11 -- Agent 05: Database Verification (2026-04-27)
  - `04_conceptual_models/04_db_functions.sql` -- 5 new DB functions: get_latest_macro_snapshot(), get_user_project_summary(), get_champion_model(), log_audit_event(), refresh_champion_flag()
  - `04_conceptual_models/04_db_indexes.sql` -- 14 additional performance indexes (predictions JSONB GIN, macro time-series, projects user-scoped)
  - `04_conceptual_models/04_db_verification.sql` -- 14 SQL verification checks + 6 RLS policy tests
  - `nhces-backend/app/database.py` -- updated: health_check(), verify_schema(), get_macro_snapshot_from_db(), get_champion_from_db(), promote_champion_in_db()
  - `04_conceptual_models/O6_11_Database_Verification.pdf` -- 6-page verification report (checklists, RLS guide, function reference, pre-launch checklist)

- [x] O6-S12 -- Agents 06+07: Tests + Code Review (2026-04-27)
  - `nhces-backend/tests/test_api.py` -- health, estimate, macro, projects, reports, pipeline (73 assertions)
  - `nhces-backend/tests/test_estimate.py` -- feature_prep mocking, SHAP fallback, CI calculation, Supabase logging
  - `nhces-backend/tests/test_pipeline.py` -- Airflow REST mocking, health aggregation, graceful fallback
  - All 73 tests PASSING (pytest 9.0.3)
  - Code review checklist: auth guards, SQL injection prevention (parameterised queries), CORS origins, RLS enforcement, R2 presigned URL expiry, secret rotation guide

- [x] O6-S13 -- Agent 08: API Documentation (2026-04-27)
  - `nhces-backend/generate_o6_s13_api_docs.py` -- generator script
  - `nhces-backend/O6_13_API_Documentation.pdf` -- 13pp, AMBER
  - Covers all 17 endpoints with full request/response schemas, error codes, SHAP item structure, feature vector reference, JWT auth guide

- [x] O6-S14 -- Agents 09+10: Deployment Infrastructure (2026-04-27)
  - `nhces-backend/Dockerfile` -- 2-stage build (builder: python:3.12-slim + build-essential; runtime: python:3.12-slim + libgomp1), non-root user nhces, HEALTHCHECK on /health
  - `nhces-backend/.dockerignore` -- excludes .env, tests/, models/*.pkl, PDFs, generate_*.py
  - `nhces-backend/railway.toml` -- DOCKERFILE builder, healthcheckPath=/health, 20 env var declarations
  - `.github/workflows/deploy.yml` -- 4-job CI/CD: backend-tests → frontend-build → deploy-backend (Railway) → deploy-frontend (Vercel)
  - `05_ml_models/05_dags/nhces_daily_fx_oil.py` -- Daily 04:00 UTC, NGN/USD/EUR/GBP + Brent
  - `05_ml_models/05_dags/nhces_weekly_materials.py` -- Monday 04:00 UTC, cement + iron rod by zone
  - `05_ml_models/05_dags/nhces_weekly_property.py` -- Tuesday 04:00 UTC, property listing prices
  - `05_ml_models/05_dags/nhces_monthly_macro.py` -- 1st of month 04:00 UTC, CPI + lending rate
  - `05_ml_models/05_dags/nhces_worldbank_annual.py` -- 2nd Jan 04:00 UTC, 30-yr GDP + CPI bulk refresh
  - `05_ml_models/05_dags/nhces_drift_monitor.py` -- Daily 16:00 UTC, PSI drift detection, auto-retrain trigger
  - `05_ml_models/05_dags/nhces_connections.json` -- 6 Airflow connection templates
  - `05_ml_models/05_dags/nhces_variables.json` -- 14 Airflow variable templates
  - `nhces-backend/generate_o6_s14_deployment.py` + `O6_14_Deployment_Guide.pdf` -- 10pp, AMBER, 8 sections + 29-item pre-launch checklist

- [x] O6-S15 -- Beginner Deployment Guide (2026-04-27)
  - `nhces-backend/generate_o6_s15_beginner_guide.py` -- generator script
  - `nhces-backend/O6_15_Step_By_Step_Deployment.pdf` -- 14pp, beginner-friendly 6-phase guide
  - Phase 1: GitHub (5 steps: create repo, git init/add/commit/push)
  - Phase 2: Supabase (7 steps: project setup, credentials, run 4 SQL files)
  - Phase 3: Cloudflare R2 (5 steps: create bucket nhces-storage, API tokens, upload champion_model.pkl)
  - Phase 4: Railway backend (6 steps: connect repo, 11 env vars, test /health)
  - Phase 5: Vercel frontend (7 steps: import repo, 3 env vars, update vercel.json)
  - Phase 6: GitHub Actions (6 steps: 5 secrets, push to trigger CI/CD)
  - Final: 14-item launch checklist + 6 common problems/solutions

### ✅ O6 FULLY COMPLETE — ALL 15 SESSIONS DONE

---

## 6. Full Build Sequence (All Remaining Work)

### O1 — Evaluate Cost Estimation Methodologies (01_literature_review/)

#### Phase 1 — Protocol Design (COMPLETE — all generated by Python scripts)
| Step | Deliverables | Data Source | Status |
|------|-------------|-------------|--------|
| 1 — PRISMA Protocol | 01_PRISMA_Protocol.pdf, 02_Search_Strings.pdf, 03_Data_Extraction_Template.pdf | ✅ Real research design | ✅ Complete |
| 2 — Taxonomy Table | 04_Methodology_Taxonomy_Table.pdf, 05_ML_Method_Comparison.pdf | ⚠️ AI-generated template | ⚠️ Template only — replace after Phase 2 |
| 3 — Gap Analysis | 06_Literature_Review_Draft.pdf, 07_Gap_Analysis_Table.pdf, 08_Included_Studies_Bibliography.pdf | ⚠️ AI-generated template (counts fabricated) | ⚠️ Template only — replace after Phase 2 |
| 4 — Survey Instrument | 09_QS_Survey_Instrument.pdf, 10_SPSS_Analysis_Plan.pdf | ✅ Real research design | ✅ Complete |
| 5 — Hypothetical Survey Analysis | 11_ through 15_.pdf + CSV | ⚠️ Hypothetical (n=60, seed=2025) | ⚠️ Replace when field data available |
| — | 16_PRISMA_Checklist_Status.pdf | ✅ Real compliance tracking | ✅ Complete |

#### Phase 2 — SLR Execution (RESEARCH TEAM FIELDWORK — cannot be done by script)
| Step | Action | Trigger | Who |
|------|--------|---------|-----|
| A | Register on PROSPERO (prospero.york.ac.uk) | IMMEDIATE — before any search | PI / Lead Researcher |
| B | Run search strings (02_Search_Strings.pdf) in all 10 databases | After PROSPERO ID confirmed | Research team |
| C | Import to Zotero, deduplicate | After all database searches done | Research team |
| D | Dual-reviewer title/abstract screening | After deduplication | Two reviewers independently |
| E | Dual-reviewer full-text screening (IC/EC from Section 4 of Protocol) | After abstract screening | Two reviewers independently |
| F | Data extraction using 03_Data_Extraction_Template.pdf | After full-text screening | Both reviewers + consensus |
| G | CASP quality appraisal per included study | Parallel with Step F | Both reviewers |
| H | Replace AI-generated content in 04_, 06_, 07_ with real extracted data | After Steps F and G | Research team + Copilot/Claude |
| I | Write Paper P1 (Construction Management and Economics) | After synthesis complete | PI + Copilot/Claude |

### O2 — Macroeconomic Variable Analysis (02_macro_analysis/)
| Step | Deliverables | Status |
|------|-------------|--------|
| 1 — Data Collection Scripts | fetch_worldbank.py → O2_01_.pdf (GREEN, live) | fetch_eia_oil.py → O2_02_.pdf (RED, synthetic) | fetch_cbn_fx.py → O2_03_.pdf (RED, synthetic) | ✅ Complete |
| 2 — Stationarity Analysis | stationarity_analysis.py → O2_04_Stationarity_Analysis.pdf (AMBER) | ✅ Complete |
| 3 — VAR/VECM Models | var_vecm_model.py → O2_05_VAR_VECM_Models.pdf (AMBER) | ✅ Complete |
| 4 — SHAP Variable Selection | shap_variable_selection.py → O2_06_SHAP_Variable_Selection.pdf (RED) | ✅ Complete |

### O3 — Requirements Modelling (03_requirements/)
| Step | Deliverables | Status |
|------|-------------|--------|
| 1 — Stakeholder Analysis | O3_01_Stakeholder_Register.pdf (GREEN) | ✅ Complete |
| 2 — Delphi Instruments | O3_02/03/05 Round 1/2/3 Instruments (AMBER) + delphi/Round1/2/3.md | ✅ Complete |
| 3 — Delphi Analysis | O3_04 Round2 Analysis + O3_06 Final Consensus (RED, n=20 seed=42) + delphi_results.csv | ✅ Complete |
| 4 — SRS + Use Cases | O3_07_SRS_IEEE830.pdf (AMBER) + O3_08_UML_Use_Cases.pdf (GREEN) + srs/03_SRS_NHCES_IEEE830.md + use_cases/03_UML_Use_Cases.md | ✅ Complete |

### O4 — Conceptual Models (04_conceptual_models/)
| Step | Deliverables | Status |
|------|-------------|--------|
| 1 — System Architecture | 04_Architecture_Diagram.mmd, O4_01_System_Architecture.pdf | ✅ Complete (AMBER, 13pp) |
| 2 — Database Schema | 04_schema.sql, 04_rls_policies.sql, 04_seed_data.sql, O4_02_Database_Schema.pdf | ✅ Complete (AMBER, 16pp, 16 tables) |
| 3 — DFDs | 04_DFD_Level0.mmd, 04_DFD_Level1.mmd, 04_User_Journey.mmd, 04_Pipeline_Flow.mmd, O4_03_Data_Flow_Diagrams.pdf | ✅ Complete (AMBER, 9pp) |
| 4 — Chapter 4 | 04_Chapter4_Conceptual_Models.md + O4_04_Chapter4_Conceptual_Models.pdf | ✅ Complete (AMBER, 13pp) |

### O5 — ML Models (05_ml_models/)
| Step | Deliverables | Status |
|------|-------------|--------|
| 1 — Feature Engineering | 05_feature_engineering.py + O5_01 PDF | ✅ Complete (AMBER/RED, 22 rows x 14 features) |
| 2 — Model Benchmarking | 05_model_benchmarking.py + O5_02 PDF | ✅ Complete (RED, champion=LightGBM LOO-CV MAPE 13.66%) |
| 3 — SHAP Analysis | 05_shap_analysis.py + O5_03 PDF | ✅ Complete (RED, near-zero SHAP at n=22 — pipeline validation only) |
| 4 — Retrain DAG | 05_mlflow_config.py + 05_model_promotion.py + 05_dags/nhces_retrain_weekly.py | ✅ Complete (AMBER, 6-task Airflow DAG) |
| 5 — Chapter 5 | 05_Chapter5_ML_Models_Results.md | ✅ Complete (RED/AMBER) |

### O6 — Web System (nhces-backend/ + nhces-frontend/)
| Session | Agent | Deliverables | Status |
|---------|-------|-------------|--------|
| S1 | 04 | main.py, config.py, database.py, auth.py, requirements.txt, .env.example | ✅ Complete |
| S2 | 04 | app/ml/inference.py, feature_prep.py, explainer.py | ✅ Complete |
| S3 | 04 | schemas/estimate.py + routers/estimate.py (POST /estimate) | ✅ Complete |
| S4 | 04 | schemas (macro, project, report) + routers (macro, projects, reports, pipeline) | ✅ Complete |
| S5 | 04 | services/r2_storage.py, report_generator.py, pipeline_monitor.py | ✅ Complete |
| S6 | 03 | package.json, lib/styles.ts (GS+Warm Ivory), lib/api.ts, lib/formatters.ts, lib/auth.ts, app/layout.tsx, components/ui/*, components/layout/Navbar+Footer | ✅ Complete |
| S7 | 03 | app/page.tsx (landing: hero+stats+steps+badges+CTA), app/estimate/page.tsx (form+result+ShapChart) | ✅ Complete |
| S8 | 03 | app/dashboard/page.tsx + components/dashboard/* (MacroSnapshot, ModelStatus, PipelineHealth, RecentPredictions) | ✅ Complete |
| S9 | 03 | app/projects, app/reports, app/macro pages | ✅ Complete |
| S10 | 03 | app/login, app/register pages | ✅ Complete |
| S11 | 05 | Supabase verification, RLS testing, DB functions | ✅ Complete |
| S12 | 06+07 | Tests (73/73 pass) + code review checklist | ✅ Complete |
| S13 | 08 | API Documentation PDF (13pp) | ✅ Complete |
| S14 | 09+10 | Dockerfile, railway.toml, deploy.yml, 6 Airflow DAGs, deployment guide | ✅ Complete |
| S15 | — | Beginner deployment guide (14pp, 6-phase step-by-step) | ✅ Complete |

---

## 7. Key Variables Reference

### ML Target Variable
`cost_per_sqm` — Nigerian housing construction cost per square metre (NGN)

### Macroeconomic Features (from Research Advisory Section 7.4)
| Feature Group | Sources | Supabase Table |
|--------------|---------|---------------|
| Exchange rate (NGN/USD, EUR, GBP) | CBN FX Portal + Open Exchange Rates | macro_fx |
| Inflation / CPI | CBN Inflation Portal + NBS | macro_cpi |
| Lending / MPR interest rate | CBN Statistics DB + Trading Economics | macro_interest |
| Crude oil price (Brent) | EIA API | macro_oil |
| GDP growth / Real Estate GDP | World Bank API + NBS | macro_gdp |
| Cement price by brand & region | BusinessDay + Titanium scrapers | material_cement |
| Iron rod price by diameter & region | BusinessDay + Jiji.ng scrapers | material_steel |
| PMS (petrol) price by state | NNPC/NMDPRA + NBS | material_pms |
| NIQS unit rates | NIQS Quarterly Schedule | unit_rates |
| Housing project completed cost | FHA, State corps (MoU) | projects |
| Property listing prices (NGN/sqm) | PropertyPro + Private Property scrapers | market_prices |

### ML Model Family
| Category | Models |
|----------|--------|
| Baseline | Ridge, Lasso, ElasticNet |
| Primary | Random Forest, XGBoost, LightGBM, Gradient Boosting |
| Neural | MLP (256→128→64) |
| Other | SVR |
| Champion | Stacking Ensemble (XGBoost + LightGBM + RF → Ridge meta-learner) |

### Performance Targets
- MAPE ≤ 15%
- R² ≥ 0.90
- API response < 3 seconds

---

## 8. Airflow DAG Schedule (9 DAGs)

| DAG Name | Schedule | Purpose |
|----------|----------|---------|
| nhces_daily_fx_oil | Daily @ 06:00 WAT | CBN FX + EIA oil prices |
| nhces_weekly_materials | Weekly (Monday) | Cement, iron rod, building material scrapers |
| nhces_weekly_property | Weekly (Tuesday) | PropertyPro + Private Property scrapers |
| nhces_monthly_macro | Monthly (1st) | CBN inflation, stats DB, NNPC PMS |
| nhces_quarterly_niqs | Quarterly | NIQS unit rates (manual upload trigger) |
| nhces_quarterly_nbs | Quarterly | NBS Housing/Construction statistics |
| nhces_worldbank_annual | Annual (January) | World Bank GDP, household income |
| nhces_retrain_weekly | Weekly (Sunday) | Champion-challenger ML retrain + MLflow |
| nhces_drift_monitor | Daily @ 18:00 WAT | PSI drift detection, emergency retrain |

---

## 9. Publication Portfolio (9 Papers)

| Paper | Journal | Objective | Target Month | Draft Status |
|-------|---------|-----------|-------------|-------------|
| P1 — PRISMA SLR | Construction Mgmt & Economics | O1 Steps 1-3 | Months 3-5 | ✅ Draft PDF |
| P2 — Delphi Requirements | Eng., Const. & Arch. Mgmt | O1-Step4 + O3 | Months 8-10 | ✅ Draft PDF |
| P3 — Macroeconomic Determinants | Construction Mgmt & Economics | O2 Steps 2-4 | Months 6-8 | ✅ Draft PDF |
| P4 | Automated Data Pipeline | Scientific Data | O2-Step1+O4+O5a | Months 12-14 | ✅ Draft PDF (AMBER/RED, 10pp) |
| P5 | ML Benchmarking | J. Const. Eng. & Mgmt (ASCE) | O5 Steps 1-3 | Months 15-17 | ✅ Draft PDF (RED, 11pp) |
| P6 | MLOps Architecture | Expert Systems with Applications | O5 Steps 4-5 | Months 16-18 | ✅ Draft PDF (AMBER, 12pp) |
| P7 | Full iNHCES System (FLAGSHIP) | Automation in Construction (IF ~9.6) | O6 All Steps | Months 21-24 | ✅ Generator updated (Apr 29) — transparency + deployment sections |
| P8 | Housing Policy | Habitat International | Post O6 | Months 23-26 | ⏳ Post-deployment |
| **P9 — AI Research Simulation Framework** | **Computers & Education / IETI / AI & Society** | **Meta: O1-O6 process** | **Months 24-26** | **✅ Draft PDF (AMBER, 26pp)** |

### P9 — Key Details
- **Title:** Responsible AI Integration in Academic Research Workflows: A Simulation-to-Publication Framework for Postgraduate Training -- Evidence from the iNHCES System Development Project
- **Contribution:** Documents the S2PF (Simulation-to-Publication Framework) — the DATA SOURCE Declaration System, Replacement Obligation, Human Validation Gate, Governing Preamble, and complete AI tool environment setup guide — as a replicable, ethics-compliant AI research simulation methodology for postgraduate training.
- **Draft generator:** `Draft AI Papers/generate_p9_ai_simulation_draft.py`
- **Draft PDF:** `Draft AI Papers/P9_AI_Research_Simulation_Draft.pdf` (26 pages, AMBER)
- **Key addition (2026-04-26):** Section 4.5 — Environment Setup (VS Code + Claude Code CLI + GitHub Copilot + Python venv; Tables 7-9; Steps 1-6; 11-item checklist). Appendix D — Full Replication Guide (Windows + macOS/Linux commands, CLAUDE.md template, SESSION_START prompt, PROJECT_CONTEXT.md template).
- **Pre-submission requirement:** ABU Zaria pilot workshop with n>=20 PG students; pre/post survey; IRB approval; complete O4-O6 walkthrough (Section 5.4).

---

## 10. Post-Deployment UI Improvements (April 29 2026)

| Commit | Change | Files |
|--------|--------|-------|
| `fc6ae51` | `lucide-react` icons on all Navbar items | `Navbar.tsx`, `package.json` |
| `4dbcab1` | iNHCES 3D isometric logo (house + i-dot + ascending bars) | `Logo.tsx`, `public/logo.svg`, `app/icon.svg` |
| `b321af2` | Navbar font size +10% (14→15 px), color → accent gold `#8b6400` | `lib/styles.ts` |
| `21bef60` | Estimate page transparency: Part A Macro Context panel + Part B Feature Snapshot panel | `app/estimate/page.tsx` |
| `1c5d777` | CLAUDE.md + PROJECT_CONTEXT.md updated (system live, paper status, CORS issue, review freeze) | `CLAUDE.md`, `PROJECT_CONTEXT.md` |
| `9167a38` | Macro Context panel: `maxHeight: 260px` + `overflowY: auto` — all variables now scrollable | `app/estimate/page.tsx` |

### Estimate Page Transparency Design (commit `21bef60`)
- **Part A — Macro Context panel** (left column, below form): 7 raw macro values (CPI, GDP growth, lending rate, Brent crude, NGN/USD/EUR/GBP) auto-fetched from `GET /macro` at page load. Collapsible. DataSourceBadge (GREEN/AMBER/RED). Link to `/macro` page for updates.
- **Part B — Feature Snapshot panel** (right column, below SHAP chart): all 14 derived model inputs (first differences and % returns) fed to LightGBM, with human-readable labels and sign-coded values. Collapsible. Already available in `EstimateResponse.feature_snapshot` — zero backend changes needed.
- **Form heading** now reads `A. User-provided project inputs` to mirror the `B.` macro panel label — making the two-group transparency structure explicit.

## ⛔ REVIEW FREEZE (as of April 29 2026)
All code changes frozen pending research team review. No new implementation until freeze is lifted.

**What to review:**
1. Live system: https://i-nhces.vercel.app — all 8 pages, Navbar icons, logo, font/colour
2. Estimate page: transparency panels (Part A + Part B)
3. Draft papers: P1–P9 in `Draft AI Papers/` — verify DATA SOURCE banners, content accuracy
4. CLAUDE.md + PROJECT_CONTEXT.md — verify accuracy of status entries
5. GitHub repo: https://github.com/baeconsultingeng-AI/iNHCES — verify CI/CD, test coverage

---

## 11. How to Resume Development

### In Copilot Chat (GitHub Copilot)
1. Open this project in VS Code
2. Read this file (PROJECT_CONTEXT.md) — note the GOVERNING FRAMEWORK section at the top
3. Confirm you are operating under the obligations of `00_S2RF_Governing_Preamble_iNHCES.pdf`
4. Say: *"I'm continuing iNHCES. Read PROJECT_CONTEXT.md. We stopped at O3 Step 1. Continue from there."*
5. Attach only the PDFs needed for the current step (max ~30 pages per session to avoid the 100-page limit)

### In Claude Extension (VS Code)
1. Open this project — Claude auto-reads CLAUDE.md
2. Say: *"Read PROJECT_CONTEXT.md and continue the iNHCES build from O1 Step 1"*

### In Claude Code CLI
```bash
cd "c:\Users\MacBook\Desktop\BaeSoftIA\INHCES\iNHCES"
claude
# Then say: "Read PROJECT_CONTEXT.md and continue from O1 Step 1"
```

### After completing any step — update this file
Change the status emoji in Section 6:
- 🔴 = currently stopped here (only ONE at a time)
- ✅ = completed
- ⬜ = not yet started

---

## 12. Known Issues / Session Error Log

| Date | Error | Cause | Resolution |
|------|-------|-------|-----------|
| 2026-04-23 | `400 {"message":"A maximum of 100 PDF pages may be provided."}` | Previous session attached all 3 research PDFs (>100 pages combined) in one request | Attach only 1-2 relevant PDFs per session. The 3 research documents combined exceed 100 pages. Attach only the section relevant to the current objective. |
| 2026-04-29 | CORS policy: No 'Access-Control-Allow-Origin' header on all API calls | Railway backend was crashing at startup before CORS middleware could register. Root cause: Supabase `Invalid API key` — env vars in Railway were wrong (Service Role key used in SUPABASE_ANON_KEY slot) | Fixed by setting correct SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_KEY, SUPABASE_JWT_SECRET in Railway Variables dashboard. Supabase renamed the key tabs — use the **Legacy** `anon / service_role` tab which has clearly labelled keys. |

---

## 13. Research Documents Reference

All in `Research_Documents/`:

| Document | Location | Use When |
|----------|----------|----------|
| `00_S2RF_Governing_Preamble_iNHCES.pdf` | `Research_Documents/` | **ALWAYS** — S2RF governing preamble, ethics framework, DATA SOURCE rules |
| `04_iNHCES_Live_Data_Infrastructure_Guide.pdf` | `Research_Documents/` | Live data sources, pipeline architecture, ML retraining (Sections 7-12) |
| `01_S2RF_Claude_AI_Workflow_Guide_iNHCES.pdf` | `Research_Documents/` | Exact prompts + expected outputs for each O/Step (O1-O6) |
| `03_iNHCES_Research_Publication_Portfolio.pdf` | `Research_Documents/` | Publication planning, paper content mapping |

> **PDF Attachment Rule:** Never attach all four Research_Documents PDFs in the same session. The Governing Preamble (12pp) + Claude Workflow Guide (~30pp) alone = ~42 pages, which is fine. The Live Data Infrastructure Guide (~25pp) can be added for pipeline/architecture sessions. Adding the Publication Portfolio (12pp) brings the total to ~67 pages — attach selectively based on session focus. All other PDFs should NOT be attached simultaneously.

---

---

## 14. Standing AI Ethics & Integrity Rules

Derived from `00_S2RF_Governing_Preamble_iNHCES.pdf` (Section 6). Apply to every session and every output.

1. **Full transparency of AI involvement** — this preamble document exists; every PDF has a DATA SOURCE page; no AI involvement is hidden.
2. **No AI-generated citations** — independently verify every reference in Scopus / Web of Science before use in any publication.
3. **Synthetic data replacement obligation** — every RED-banner document contains synthetic data that MUST be replaced before any publication or grant report use.
4. **Human validation at every stage** — no AI output advances to the next pipeline stage without review and approval by a named researcher.
5. **Disclosure in all publications** — include the standard AI Disclosure Statement (preamble Section 9.2) in every paper, thesis chapter, and conference submission.
6. **Ethics board compliance** — obtain ABU Zaria IRB approval before any human-subjects data collection (Delphi surveys, practitioner questionnaires).
7. **Open science** — publish all non-sensitive datasets, trained models, and code to open repositories (GitHub / Zenodo) on publication.

---

*Last updated: 2026-04-27 | ✅ ALL O6 SESSIONS COMPLETE (S1-S15) | Research_Documents suite finalised: 00_S2RF_Governing_Preamble_iNHCES.pdf + 01_S2RF_Claude_AI_Workflow_Guide_iNHCES.pdf + 03_iNHCES_Research_Publication_Portfolio.pdf + 04_iNHCES_Live_Data_Infrastructure_Guide.pdf (tables rebuilt, S2RF-named) | O6-S15: O6_15_Step_By_Step_Deployment.pdf (14pp, beginner 6-phase guide) | O6-S14: Dockerfile + .dockerignore + railway.toml + deploy.yml (4-job CI/CD) + 6 Airflow DAGs | O6-S13: O6_13_API_Documentation.pdf (13pp, 17 endpoints) | O6-S12: 73/73 tests pass (pytest 9.0.3) | O6 FRONTEND COMPLETE (S6-S10) | O6 BACKEND COMPLETE (S1-S5) | O1-O5 ALL COMPLETE | NEXT ACTION: Deploy using O6_15_Step_By_Step_Deployment.pdf*
