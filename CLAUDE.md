# iNHCES Project Context
# Auto-read by Claude Code on every session start

## Project
Intelligent National Housing Cost Estimating System (iNHCES)
TETFund NRF 2025 | Department of Quantity Surveying, ABU Zaria

## Governing Framework
Every session is governed by the S2RF Governing Preamble:
`Research_Documents/00_S2RF_Governing_Preamble_iNHCES.pdf`
- Apply DATA SOURCE banner (GREEN / AMBER / RED) to every PDF produced
- GREEN = live API / real instrument | AMBER = AI-authored template | RED = synthetic data
- RED-banner content MUST be replaced with real data before any publication
- No AI-generated citations — verify every reference in Scopus / Web of Science
- AI is a tool, not an author — human researchers bear full accountability

## Tech Stack
- **Frontend**: Next.js 14 (App Router, TypeScript, Warm Ivory palette) → Vercel
- **Backend**: FastAPI (Python 3.10+) → Railway
- **Database**: Supabase PostgreSQL (16 tables, RLS, seed data)
- **ML Registry**: MLflow → Railway
- **Storage**: Cloudflare R2
- **Orchestration**: Apache Airflow (9 DAGs) → Railway
- **CI/CD**: GitHub Actions (.github/workflows/deploy.yml)

## GitHub Repository
https://github.com/baeconsultingeng-AI/iNHCES
Branch: master | Latest commit: `21bef60` (April 29 2026) | CI/CD: GitHub Actions live

---

## CURRENT STATUS — ALL OBJECTIVES COMPLETE

### Research Objectives
| Objective | Status | Key Output |
|-----------|--------|-----------|
| O1 — Literature Review | ✅ Complete | 16 PDFs, PRISMA protocol, QS survey, hypothetical analysis |
| O2 — Macro Analysis | ✅ Complete | WorldBank live, EIA/FX synthetic, VAR/VECM, SHAP ranking |
| O3 — Requirements | ✅ Complete | Delphi x3 (36/40 consensus), SRS IEEE 830, UML use cases |
| O4 — Conceptual Models | ✅ Complete | 7-layer architecture, 16-table schema, 4 DFDs, Chapter 4, 6 diagrams |
| O5 — ML Models | ✅ Complete | LightGBM champion 13.66% LOO-CV MAPE, SHAP, 6-task Airflow DAG, Chapter 5 |
| O6 — Web System | ✅ Complete | 15 sessions: FastAPI + Next.js + tests + docs + CI/CD + deployment guide |

### O6 Sessions Completed
| Session | Agent | Key Deliverables |
|---------|-------|-----------------|
| S1 | 04 Backend | main.py, config.py, database.py, auth.py, requirements.txt |
| S2 | 04 Backend | app/ml/inference.py + feature_prep.py + explainer.py (LightGBM + SHAP) |
| S3 | 04 Backend | POST /estimate (4-horizon temporal projection + SHAP) |
| S4 | 04 Backend | GET /macro + /history, CRUD /projects, POST/GET /reports, GET /pipeline — 17 routes |
| S5 | 04 Backend | r2_storage.py + report_generator.py (fpdf2 4-page PDF) + pipeline_monitor.py |
| S6 | 03 Frontend | Warm Ivory GS system, all UI components, Navbar, layout |
| S7 | 03 Frontend | Landing page (2-col viewport-fill) + Estimate page (TemporalChart) |
| S8 | 03 Frontend | Dashboard (6-stat pills, 3-col grid: Macro/Model/Pipeline) |
| S9 | 03 Frontend | Projects + Reports + Macro pages |
| S10 | 03 Frontend | Login + Register + Navbar auth state (Supabase GoTrue) |
| S11 | 05 Database | 04_db_functions.sql (5 fns) + 04_db_indexes.sql (14 idx) + 04_db_verification.sql |
| S12 | 06+07 QA | 73 test assertions passing; code review checklist complete |
| S13 | 08 Docs | O6_13_API_Documentation.pdf (13pp, all 17 endpoints) |
| S14 | 09+10 DevOps | Dockerfile + railway.toml + deploy.yml + 6 Airflow DAGs + O6_14_Deployment_Guide.pdf |
| S15 | — | O6_15_Step_By_Step_Deployment.pdf (14pp, 6-phase beginner guide) |

### Additional Feature — Temporal Cost Projection
- `02_macro_analysis/forecast_macro.py` — VAR h-step forecasts
- `05_ml_models/05_temporal_projection.py` — compound inflation engine (5yr cap)
- `nhces-backend/app/ml/temporal.py` — FastAPI integration
- `nhces-frontend/components/estimate/TemporalChart.tsx` — SVG line chart + widening CI
- 4 horizons: Current / <1yr / <3yr / <5yr | 25% p.a. (real World Bank CPI)
- P3 + P5 draft papers: Section 5B added (temporal projection methodology)

---

## Draft Papers Status (9 papers)
| # | Title | File | Pages | Data Level |
|---|-------|------|-------|-----------|
| P1 | PRISMA SLR | P1_PRISMA_SLR_Draft.pdf | — | AMBER (placeholder counts) |
| P2 | Delphi Requirements | P2_Delphi_Requirements_Draft.pdf | — | RED/AMBER (n=20 synthetic) |
| P3 | Macro Determinants | P3_Macroeconomic_Determinants_Draft.pdf | — | AMBER/RED + Section 5B |
| P4 | Data Pipeline | P4_Data_Pipeline_Draft.pdf | 10pp | AMBER/RED (scrapers pending) |
| P5 | ML Benchmarking | P5_ML_Benchmarking_Draft.pdf | 11pp | RED + Section 5B |
| P6 | MLOps Architecture | P6_MLOps_Architecture_Draft.pdf | 12pp | AMBER |
| P7 | Full iNHCES System | `generate_p7_full_system_draft.py` (updated Apr 29) | ~12pp | AMBER (generator updated: transparency panels, 3D logo, deployment section) |
| P8 | Housing Policy | Post-deployment | — | Not started |
| P9 | AI Research Simulation | P9_AI_Research_Simulation_Draft.pdf | 27pp | AMBER (O1-O5 walkthrough) |

All draft papers in: `Draft AI Papers/`
Research Publication Portfolio: `Research_Documents/iNHCES_Research_Publication_Portfolio.pdf`

---

## SYSTEM STATUS — LIVE & DEPLOYED
Frontend: https://i-nhces.vercel.app | Backend: https://inhces-production.up.railway.app
Last confirmed healthy: `{"status":"ok","db":{"status":"ok"},"ml_model":"loaded"}`

| Phase | Action | Status |
|-------|--------|--------|
| 1 | GitHub — repo created, code pushed | ✅ Done |
| 2 | Supabase — project created, 4 SQL files run, credentials set | ✅ Done |
| 3 | Cloudflare R2 — bucket nhces-storage, champion_model.pkl uploaded | ✅ Done |
| 4 | Railway — GitHub connected, 11 env vars set, /health confirmed OK | ✅ Done |
| 5 | Vercel — repo imported, 3 env vars set (SUPABASE_URL, ANON_KEY, API_URL) | ✅ Done |
| 6 | GitHub Actions — 5 secrets set, CI/CD pipeline live | ✅ Done |

---

## Post-Deployment UI Improvements (April 29 2026)
| Commit | Change |
|--------|--------|
| `fc6ae51` | `lucide-react` icons on all Navbar items (Calculator, LayoutDashboard, FolderOpen, FileText, TrendingUp, LogIn, LogOut, UserPlus) |
| `4dbcab1` | iNHCES 3D isometric logo (house + i-dot + ascending bars) — `Logo.tsx`, `public/logo.svg`, `app/icon.svg` (auto-favicon) |
| `b321af2` | Navbar font size +10% (14→15 px), color → accent gold `#8b6400` |
| latest | **Estimate page transparency** — Part A: Macro Context panel (7 raw macro values, collapsible, below form); Part B: Feature Snapshot panel (all 14 derived model inputs with human-readable labels, collapsible, below SHAP). No backend changes required (`feature_snapshot` was already in `EstimateResponse`). |
| `21bef60` | P7 generator updated (transparency panels documented in Section 7.2 + 7.3); CLAUDE.md + PROJECT_CONTEXT.md updated; REVIEW FREEZE applied |

## ⛔ REVIEW FREEZE
All code changes are frozen pending a complete review by the research team.
Do not implement further changes until the freeze is lifted.

---

## Key Technical Facts (for new sessions)
- **Champion model**: LightGBM | LOO-CV MAPE 13.66% | `05_ml_models/models/champion_model.pkl`
- **17 FastAPI routes**: GET /, GET /health, POST /estimate, GET /macro, GET /macro/history, GET/POST/PUT/DELETE /projects, POST/GET /reports, GET /pipeline
- **8 frontend pages**: /, /estimate, /dashboard, /projects, /reports, /macro, /login, /register
- **Design**: Warm Ivory palette (#f5f1eb bg, #8b6400 accent) | Playfair Display + Lora + DM Sans
- **Dev commands**:
  - Backend: `cd nhces-backend && python -m uvicorn app.main:app --port 8000`
  - Frontend: `cd nhces-frontend && npm run dev`
  - Backend needs: `.env` file (copy from `.env.example`, fill in Supabase credentials)
  - Frontend needs: `.env.local` (copy from `.env.local.example`, fill in Supabase + API URL)

## Data Still Needed Before Publication (RED items)
| Item | What's needed | Action |
|------|--------------|--------|
| Brent crude price | Real EIA API data | Set EIA_API_KEY, re-run fetch_eia_oil.py |
| NGN/FX rates | Real CBN/FRED data | Set FRED_API_KEY, re-run fetch_cbn_fx.py |
| cost_per_sqm target | Real NIQS unit rates | Conduct O4 fieldwork, replace synthetic proxy |
| Delphi (n=20) | Real expert panel | Conduct 3-round Delphi with Nigerian QS experts + IRB |
| Survey (n=60) | Real QS responses | Conduct practitioner survey + IRB approval |

## Research Workflow — What Remains (Post-Simulation)
1. **PROSPERO registration** before any database search (SLR Phase 2)
2. **ABU Zaria IRB approval** before Delphi or survey fieldwork
3. **Real data collection** to replace all RED-banner synthetic content
4. **Human validation** of all AI-generated outputs before publication
5. **Deploy iNHCES** live → collect real project cost predictions → update ML model
6. **Write P7 + P8** after live deployment produces real system results

## O6 Development Workflow Rules (if resuming O6 work)
1. Seek approval before every session
2. Show every new frontend page in browser before proceeding to next session
