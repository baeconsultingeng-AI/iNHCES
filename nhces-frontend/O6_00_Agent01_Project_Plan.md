# Agent 01 — iNHCES O6 Project Plan
**Project Leader Output | Governs All O6 Agents**
TETFund NRF 2025 | Department of Quantity Surveying, ABU Zaria

> **DATA SOURCE: AMBER** — AI-authored plan from O3 SRS, O4 architecture, O5 ML outputs.
> No code exists yet. This document is the contract between agents.
> Research team must review and sign off before Agent 03/04/05 begin coding.

---

## 1. Project Summary

| Item | Value |
|------|-------|
| System | iNHCES — Intelligent National Housing Cost Estimating System |
| Objective | O6 — Build and deploy the full web system |
| Frontend | Next.js 14 (App Router) — deployed on Vercel |
| Backend | FastAPI (Python 3.10+) — deployed on Railway |
| Database | Supabase PostgreSQL (schema: 04_schema.sql, already deployed) |
| Storage | Cloudflare R2 (PDF reports + model artefacts) |
| ML Model | LightGBM champion — 05_ml_models/models/champion_model.pkl |
| CI/CD | GitHub Actions — test.yml + deploy.yml |
| Design | Warm Ivory Palette (Playfair Display + Lora + DM Sans) |
| Grant | TETFund National Research Fund 2025 |

---

## 2. Agent Team and Execution Order

```
PHASE 0 (COMPLETE):  Agent 01 — Project Plan (this document)
PHASE 1 (COMPLETE):  Agent 02 — Data Science (O5: champion_model.pkl exists)
PHASE 2 (PARALLEL):  Agent 03 — Frontend  |  Agent 04 — Backend  |  Agent 05 — Database
PHASE 3 (SEQUENTIAL): Agent 06 — QA  |  Agent 07 — Code Review  |  Agent 08 — Docs
PHASE 4 (FINAL):      Agent 09 — DevOps  |  Agent 10 — MLOps
```

| Agent | Role | Phase | Files Owned |
|-------|------|-------|-------------|
| 01 | Project Leader | 0 | This document |
| 02 | Data Scientist | DONE | 05_ml_models/ (complete) |
| 03 | Frontend Dev | 2 | nhces-frontend/ |
| 04 | Backend Dev | 2 | nhces-backend/ |
| 05 | Database Dev | 2 | nhces-backend/app/database.py, migrations/ |
| 06 | QA Engineer | 3 | nhces-backend/tests/, nhces-frontend/__tests__/ |
| 07 | Code Review | 3 | All files (review only) |
| 08 | Doc Engineer | 3 | README.md, API docs |
| 09 | DevOps | 4 | .github/workflows/, Dockerfile, railway.toml, vercel.json |
| 10 | MLOps | 4 | nhces-backend/app/ml/, 05_ml_models/05_dags/ |

---

## 3. Complete File Structure

### 3.1 Backend (nhces-backend/)
```
nhces-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                  ← FastAPI app entry, CORS, router includes
│   ├── database.py              ← Supabase async client (service_role)
│   ├── auth.py                  ← JWT middleware (Supabase GoTrue)
│   ├── config.py                ← Settings from environment variables
│   │
│   ├── ml/
│   │   ├── __init__.py
│   │   ├── inference.py         ← Load champion .pkl, predict(), cache in memory
│   │   ├── feature_prep.py      ← Assemble 14-feature vector from Supabase
│   │   └── explainer.py         ← SHAP values for /estimate response
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── estimate.py          ← POST /estimate
│   │   ├── macro.py             ← GET /macro, GET /macro/history
│   │   ├── projects.py          ← GET/POST/PUT/DELETE /projects
│   │   ├── reports.py           ← POST /reports, GET /reports
│   │   └── pipeline.py          ← GET /pipeline
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── estimate.py          ← EstimateRequest, EstimateResponse (Pydantic)
│   │   ├── project.py           ← ProjectCreate, ProjectRead, ProjectUpdate
│   │   ├── report.py            ← ReportRequest, ReportRead
│   │   └── macro.py             ← MacroSnapshot, MacroVariable
│   │
│   └── services/
│       ├── __init__.py
│       ├── r2_storage.py        ← boto3 Cloudflare R2 upload/download
│       ├── report_generator.py  ← fpdf2 PDF generation
│       └── pipeline_monitor.py  ← Airflow REST API calls
│
├── tests/
│   ├── conftest.py              ← pytest fixtures (test Supabase client)
│   ├── test_estimate.py         ← /estimate endpoint tests
│   ├── test_api.py              ← General API tests
│   └── test_pipeline.py         ← Pipeline endpoint tests
│
├── requirements.txt
├── Dockerfile
├── .env.example
├── railway.toml
└── README.md
```

### 3.2 Frontend (nhces-frontend/)
```
nhces-frontend/
├── app/                         ← Next.js 14 App Router
│   ├── layout.tsx               ← Root layout: fonts, global styles, nav
│   ├── page.tsx                 ← Landing / Home page
│   ├── estimate/
│   │   └── page.tsx             ← Cost Estimation page (core feature)
│   ├── dashboard/
│   │   └── page.tsx             ← Overview dashboard
│   ├── projects/
│   │   └── page.tsx             ← Project management
│   ├── reports/
│   │   └── page.tsx             ← Report history and downloads
│   ├── macro/
│   │   └── page.tsx             ← Macro data viewer
│   ├── login/
│   │   └── page.tsx             ← Login page
│   └── register/
│       └── page.tsx             ← Registration page
│
├── components/
│   ├── ui/                      ← Primitive components (use GS tokens)
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   ├── Input.tsx
│   │   ├── Select.tsx
│   │   ├── Badge.tsx
│   │   ├── DataSourceBadge.tsx  ← GREEN/AMBER/RED banner (iNHCES-specific)
│   │   ├── LoadingSpinner.tsx
│   │   └── Modal.tsx
│   ├── layout/
│   │   ├── Navbar.tsx           ← Sticky top nav with Warm Ivory palette
│   │   ├── Sidebar.tsx          ← Left nav for authenticated pages
│   │   └── Footer.tsx
│   ├── estimate/
│   │   ├── EstimateForm.tsx     ← Building params input form
│   │   ├── EstimateResult.tsx   ← Cost result panel with SHAP chart
│   │   └── ShapChart.tsx        ← Feature importance bar chart
│   ├── dashboard/
│   │   ├── MacroSnapshot.tsx    ← Latest macro values with data level badges
│   │   ├── ModelStatus.tsx      ← Champion model MAPE, version, date
│   │   ├── PipelineHealth.tsx   ← Airflow DAG last-run status
│   │   └── RecentPredictions.tsx
│   └── projects/
│       ├── ProjectCard.tsx
│       └── ProjectForm.tsx
│
├── lib/
│   ├── styles.ts                ← GS object (Warm Ivory palette — single source of truth)
│   ├── api.ts                   ← API client: typed fetch wrapper for FastAPI
│   ├── auth.ts                  ← Supabase Auth client
│   └── formatters.ts            ← formatNGN(), formatDate(), formatMAPE()
│
├── types/
│   └── index.ts                 ← TypeScript interfaces (mirrors Pydantic schemas)
│
├── public/
│   ├── favicon.ico
│   └── logo.svg
│
├── next.config.js
├── tsconfig.json
├── .env.local.example
└── vercel.json
```

---

## 4. Design System — iNHCES Warm Ivory

### 4.1 Colour Tokens (lib/styles.ts)
```typescript
export const COLOURS = {
  // Backgrounds
  background:    '#f5f1eb',   // warm ivory — page background
  surface:       '#ffffff',   // cards, panels, inputs
  surfaceAlt:    '#f0ece4',   // alternate rows, secondary panels

  // Borders
  border:        '#ddd8cf',   // default
  border2:       '#c9c2b8',   // input focus
  border3:       '#b8b0a4',   // hover

  // Text
  textPrimary:   '#1a1410',   // WCAG AAA
  textMuted:     '#5c4f42',   // WCAG AA
  textDim:       '#8a7d72',   // WCAG AA (large text)

  // Brand
  accent:        '#8b6400',   // dark amber — buttons, active nav
  accentBg:      'rgba(139,100,0,0.1)',
  accentBorder:  'rgba(139,100,0,0.28)',

  // Semantic (maps to DATA SOURCE Declaration System)
  green:         '#007a5e',   // GREEN data level, success
  greenLight:    'rgba(0,122,94,0.1)',
  amber:         '#b8620a',   // AMBER data level, warning
  red:           '#c0392b',   // RED data level, danger
  redLight:      'rgba(192,57,43,0.1)',
} as const;
```

### 4.2 Typography
```typescript
// In layout.tsx — Google Fonts import
import { Playfair_Display, Lora, DM_Sans } from 'next/font/google';

const playfair = Playfair_Display({ subsets: ['latin'], weight: ['700','900'] });
const lora     = Lora({ subsets: ['latin'], weight: ['400','500','600','700'] });
const dmSans   = DM_Sans({ subsets: ['latin'], weight: ['400','500','600'] });
```

| Font | Role | CSS variable |
|------|------|-------------|
| Playfair Display | Page titles, section headings | `--font-display` |
| Lora | Body copy, card descriptions | `--font-body` |
| DM Sans | Buttons, nav, labels, data values | `--font-ui` |

### 4.3 GS Object (Global Styles)
```typescript
export const GS = {
  app: {
    background: COLOURS.background,
    fontFamily: 'var(--font-body)',
    color: COLOURS.textPrimary,
    minHeight: '100vh',
  },
  card: {
    background: COLOURS.surface,
    border: `1px solid ${COLOURS.border}`,
    borderRadius: '12px',
    padding: '24px',
    boxShadow: '0 1px 4px rgba(26,20,16,0.06)',
  },
  btn: {
    background: COLOURS.accent,
    color: '#ffffff',
    border: 'none',
    borderRadius: '8px',
    padding: '10px 20px',
    fontFamily: 'var(--font-ui)',
    fontSize: '15px',
    fontWeight: 600,
    cursor: 'pointer',
  },
  btnGhost: {
    background: 'transparent',
    color: COLOURS.accent,
    border: `1.5px solid ${COLOURS.accentBorder}`,
    borderRadius: '8px',
    padding: '10px 20px',
    fontFamily: 'var(--font-ui)',
    fontSize: '15px',
    fontWeight: 600,
    cursor: 'pointer',
  },
  input: {
    background: COLOURS.surface,
    border: `1px solid ${COLOURS.border2}`,
    borderRadius: '8px',
    padding: '10px 14px',
    fontFamily: 'var(--font-body)',
    fontSize: '15px',
    color: COLOURS.textPrimary,
    width: '100%',
  },
  label: {
    fontFamily: 'var(--font-ui)',
    fontSize: '13px',
    fontWeight: 600,
    color: COLOURS.textMuted,
    letterSpacing: '0.04em',
    textTransform: 'uppercase' as const,
  },
  tag: {
    fontFamily: 'var(--font-ui)',
    fontSize: '13px',
    fontWeight: 500,
    padding: '3px 10px',
    borderRadius: '20px',
    display: 'inline-block',
  },
  pageTitle: {
    fontFamily: 'var(--font-display)',
    fontSize: '32px',
    fontWeight: 700,
    color: COLOURS.textPrimary,
    lineHeight: 1.25,
  },
  pageSub: {
    fontFamily: 'var(--font-body)',
    fontSize: '17px',
    color: COLOURS.textMuted,
    lineHeight: 1.6,
  },
  navBar: {
    background: COLOURS.surface,
    borderBottom: `1px solid ${COLOURS.border}`,
    position: 'sticky' as const,
    top: 0,
    zIndex: 100,
    padding: '0 24px',
    height: '60px',
    display: 'flex',
    alignItems: 'center',
  },
  navBtn: {
    fontFamily: 'var(--font-ui)',
    fontSize: '14px',
    fontWeight: 500,
    color: COLOURS.textMuted,
    padding: '6px 14px',
    borderRadius: '6px',
    border: 'none',
    background: 'transparent',
    cursor: 'pointer',
  },
  navActive: {
    background: COLOURS.accentBg,
    color: COLOURS.accent,
    fontWeight: 600,
  },
};
```

### 4.4 DataSourceBadge Component
The DATA SOURCE level must be visible on every page that shows ML predictions or macro data.

```typescript
// components/ui/DataSourceBadge.tsx
type Level = 'GREEN' | 'AMBER' | 'RED';
const BADGE_STYLES = {
  GREEN: { background: '#007a5e', color: '#ffffff' },
  AMBER: { background: '#b8620a', color: '#ffffff' },
  RED:   { background: '#c0392b', color: '#ffffff' },
};
const BADGE_LABELS = {
  GREEN: 'Live Data',
  AMBER: 'AI Template',
  RED:   'Synthetic — Replace Before Publication',
};
```

---

## 5. API Contract

### 5.1 Base URL and Auth
```
Production:  https://nhces-api.up.railway.app
Development: http://localhost:8000

All protected endpoints require:
  Authorization: Bearer <supabase-jwt-token>
  Content-Type: application/json
```

### 5.2 POST /estimate
**Purpose:** ML cost prediction for a project.

Request body:
```json
{
  "project_id": "uuid (optional — if saving to existing project)",
  "building_type": "Residential | Commercial | Industrial | Institutional | Mixed Use",
  "construction_type": "New Build | Renovation | Extension | Fit-Out",
  "floor_area_sqm": 120.0,
  "num_floors": 1,
  "location_state": "string",
  "location_zone": "North Central | North East | North West | South East | South South | South West"
}
```

Response:
```json
{
  "prediction_id": "uuid",
  "predicted_cost_per_sqm": 182500.00,
  "total_predicted_cost_ngn": 21900000.00,
  "confidence_lower": 152000.00,
  "confidence_upper": 213000.00,
  "mape_at_prediction": 13.66,
  "model_version": "lgb-2026-04-26",
  "model_stage": "Production",
  "feature_snapshot": {
    "d_gdp_growth_pct": 0.2,
    "d_cpi_annual_pct": 7.2,
    "ret_ngn_usd": 97.3
  },
  "shap_values": {
    "ret_ngn_usd": 28450.0,
    "d_cpi_annual_pct": 15820.0
  },
  "data_freshness": "RED",
  "api_response_ms": 1240,
  "created_at": "2026-04-26T10:00:00Z"
}
```

### 5.3 GET /macro
**Purpose:** Latest macroeconomic snapshot for dashboard.

Response:
```json
{
  "variables": [
    {
      "variable": "ngn_usd",
      "label": "NGN/USD Exchange Rate",
      "value": 1480.0,
      "unit": "NGN per USD",
      "as_of_date": "2024-01-01",
      "source": "FRED API",
      "data_level": "RED"
    }
  ],
  "overall_freshness": "RED",
  "as_of": "2026-04-26T10:00:00Z"
}
```

### 5.4 GET /macro/history?variable=ngn_usd&years=5
**Purpose:** Historical series for charting.

Response: `{ "variable": "ngn_usd", "data": [{"year": 2020, "value": 381.0}, ...] }`

### 5.5 CRUD /projects
```
GET    /projects           → list user's projects (paginated)
GET    /projects/{id}      → single project
POST   /projects           → create project
PUT    /projects/{id}      → update project
DELETE /projects/{id}      → delete project
```

POST /projects request:
```json
{
  "title": "3-Bed Bungalow Kaduna",
  "building_type": "Residential",
  "construction_type": "New Build",
  "floor_area_sqm": 120.0,
  "num_floors": 1,
  "location_state": "Kaduna",
  "location_zone": "North West",
  "target_cost_ngn": null,
  "notes": ""
}
```

### 5.6 POST /reports
**Purpose:** Generate a PDF cost report.

Request: `{ "project_id": "uuid", "prediction_id": "uuid" }`

Response:
```json
{
  "report_id": "uuid",
  "r2_key": "reports/{user_id}/{project_id}/{timestamp}.pdf",
  "download_url": "https://r2-presigned-url...",
  "url_expires_at": "2026-04-27T10:00:00Z",
  "page_count": 4,
  "created_at": "2026-04-26T10:00:00Z"
}
```

### 5.7 GET /reports
Response: list of user's report records with `download_url` refresh on request.

### 5.8 GET /pipeline
**Purpose:** Airflow DAG health for dashboard.

Response:
```json
{
  "dags": [
    {
      "dag_id": "nhces_daily_fx_oil",
      "schedule": "0 5 * * *",
      "last_run_state": "success",
      "last_run_at": "2026-04-26T05:00:00Z",
      "next_run_at": "2026-04-27T05:00:00Z",
      "data_level": "RED"
    }
  ],
  "overall_health": "DEGRADED"
}
```

### 5.9 Auth Endpoints (Supabase handles these — no FastAPI code needed)
```
POST /auth/v1/signup   → Supabase GoTrue
POST /auth/v1/token    → Supabase GoTrue (login)
POST /auth/v1/logout   → Supabase GoTrue
```

---

## 6. Frontend Pages — Component Specifications

### 6.1 Home / Landing Page (app/page.tsx)
**Purpose:** First impression for QS Professionals and Researchers.

Sections:
1. **Hero** — Playfair Display 44px headline: "Intelligent Housing Cost Estimation for Nigeria". Subheading in Lora. Two CTA buttons: "Get an Estimate" (accent filled) + "View Dashboard" (ghost). Warm ivory background with subtle SVG pattern.
2. **Stats strip** — 4 numbers: "7 Macroeconomic Variables | 9 Data Pipelines | 22 Training Observations | 13.66% LOO-CV MAPE". DM Sans, amber accent.
3. **How it Works** — 3 cards (Enter Project → AI Predicts → Download Report). Card component with Lora body.
4. **Data Quality** — Explain GREEN/AMBER/RED system. One DataSourceBadge for each level with explanation.
5. **CTA** — "Start Estimating" button linking to /estimate.

### 6.2 Estimate Page (app/estimate/page.tsx)
**Purpose:** Core product feature — cost estimation form and result.

Layout: Two-column (form left, result right on desktop; stacked on mobile).

Left — EstimateForm:
- Section: "Project Details" — Title input, Building Type select, Construction Type select
- Section: "Location" — State input, Zone select
- Section: "Building Parameters" — Floor area (sqm) number input, Number of floors
- Section: "Optional" — Target cost (NGN) input, Notes textarea
- Submit button: "Calculate Cost" (accent filled, full width)
- Loading state: spinner with "Consulting champion model..."

Right — EstimateResult (renders after API response):
- Header: "Estimated Cost" in Playfair Display
- Primary result: large NGN/sqm figure (DM Sans 36px, accent colour)
- Total cost: NGN total in Lora 24px
- Confidence band: lower – upper range with amber styling
- DataSourceBadge showing `data_freshness` from response
- Model info: version, MAPE, stage
- ShapChart: horizontal bar chart (top 5 SHAP features, warm ivory background)
- "Generate PDF Report" button (ghost btn)
- "Save to Project" button (ghost btn)

### 6.3 Dashboard Page (app/dashboard/page.tsx)
**Purpose:** Overview for authenticated users — macro data, model status, pipeline health.

Layout: Grid (3 columns on desktop).

Components:
- **MacroSnapshot** — Card showing 5 latest macro values (ngn_usd, cpi, gdp, lending_rate, brent). Each row has: label (DM Sans), value (DM Sans bold), DataSourceBadge.
- **ModelStatus** — Card: champion model name, MAPE, R2, training date, is_champion badge (green).
- **PipelineHealth** — Card: 9 DAGs listed with last_run_state (green tick / red cross / amber clock) and last_run_at.
- **RecentPredictions** — Table: last 5 predictions with project name, cost/sqm, date.

### 6.4 Projects Page (app/projects/page.tsx)
**Purpose:** CRUD project management.

Layout: List + side panel (or modal for create/edit).

Features:
- Project list (cards): title, location, floor area, building type, status badge, "Estimate" button.
- "New Project" button (accent filled, top right).
- ProjectForm modal: all fields from POST /projects.
- Delete with confirmation dialog.

### 6.5 Reports Page (app/reports/page.tsx)
**Purpose:** Report history and download.

Layout: Table view.

Columns: Project name, Date, PDF size, Download button (ghost, triggers presigned URL refresh).

### 6.6 Macro Data Page (app/macro/page.tsx)
**Purpose:** Historical macro data visualisation for researchers.

Features:
- Variable selector (dropdown): ngn_usd, cpi_annual_pct, gdp_growth_pct, lending_rate_pct, brent_usd_barrel.
- Line chart (recharts): historical series, x-axis = year, y-axis = value.
- DataSourceBadge per variable.
- Summary table: all latest values.

### 6.7 Auth Pages (app/login/page.tsx, app/register/page.tsx)
Centred card layout. Logo. Email + Password inputs. Submit button. Supabase Auth client.

---

## 7. Backend — Key Implementation Notes

### 7.1 ML Model Loading (app/ml/inference.py)
```python
# Champion model is loaded ONCE at FastAPI startup and cached in memory.
# Re-loaded only when champion changes (via background task on promotion).
import pickle
from pathlib import Path

_champion = None  # module-level cache

def get_champion():
    global _champion
    if _champion is None:
        # Load from Cloudflare R2 (or local fallback for development)
        _champion = load_from_r2_or_local()
    return _champion
```

### 7.2 Feature Preparation (app/ml/feature_prep.py)
Queries Supabase `v_latest_macro` view, applies the same transformations as `05_feature_engineering.py`:
- I(1) → first differences
- I(2)* → percentage returns
- Lag-1 features

Returns a numpy array of shape (1, 14) matching the champion model's expected input.

### 7.3 FastAPI App Structure (app/main.py)
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import estimate, macro, projects, reports, pipeline

app = FastAPI(title="iNHCES API", version="1.0.0")

app.add_middleware(CORSMiddleware,
    allow_origins=["https://nhces.vercel.app", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(estimate.router,  prefix="/estimate",  tags=["estimate"])
app.include_router(macro.router,     prefix="/macro",     tags=["macro"])
app.include_router(projects.router,  prefix="/projects",  tags=["projects"])
app.include_router(reports.router,   prefix="/reports",   tags=["reports"])
app.include_router(pipeline.router,  prefix="/pipeline",  tags=["pipeline"])
```

### 7.4 requirements.txt (key packages)
```
fastapi==0.110.0
uvicorn==0.29.0
pydantic==2.6.0
supabase==2.4.0
lightgbm==4.3.0
scikit-learn==1.4.0
shap==0.45.0
numpy==1.26.0
pandas==2.2.0
fpdf2==2.7.9
boto3==1.34.0
httpx==0.27.0
python-jose==3.3.0
python-multipart==0.0.9
```

---

## 8. Database Integration (Agent 05 Scope)

The Supabase schema from O4 Step 2 is already deployed. Agent 05 is responsible for:

1. **Verifying** all 16 tables exist in the Supabase production instance.
2. **Running** any pending migrations (add `updated_at` triggers if missing).
3. **Creating** the following database functions for complex queries:
   - `get_latest_macro_snapshot()` — returns v_latest_macro view data
   - `get_user_project_summary(user_id)` — projects + latest prediction per project
4. **Optimising** indexes for the `predictions` table (most queried at scale).
5. **Testing** RLS policies with test JWT tokens for all 3 roles.

---

## 9. Environment Variables

### Backend (.env / Railway)
```bash
# Supabase
SUPABASE_URL=https://[project].supabase.co
SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_KEY=eyJ...
SUPABASE_JWT_SECRET=...

# Cloudflare R2
CLOUDFLARE_R2_ENDPOINT=https://[account].r2.cloudflarestorage.com
CLOUDFLARE_R2_ACCESS_KEY=...
CLOUDFLARE_R2_SECRET_KEY=...
CLOUDFLARE_R2_BUCKET=nhces-storage

# MLflow
MLFLOW_TRACKING_URI=http://[railway-mlflow]:5000
MLFLOW_EXPERIMENT=nhces_cost_estimation

# Airflow
AIRFLOW_API_URL=http://[railway-airflow]:8080/api/v1
AIRFLOW_USERNAME=admin
AIRFLOW_PASSWORD=...

# App
SECRET_KEY=[32-byte hex]
ENVIRONMENT=production
ALLOWED_ORIGINS=https://nhces.vercel.app
```

### Frontend (.env.local / Vercel)
```bash
# Supabase (public — safe for frontend)
NEXT_PUBLIC_SUPABASE_URL=https://[project].supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...

# Backend API
NEXT_PUBLIC_API_URL=https://nhces-api.up.railway.app
```

---

## 10. Agent Acceptance Criteria

### Agent 03 (Frontend) — Done when:
- [ ] All 7 pages render correctly on desktop (1280px) and mobile (375px)
- [ ] Warm Ivory palette applied throughout (no hardcoded colours)
- [ ] Playfair Display / Lora / DM Sans loaded from Google Fonts
- [ ] `POST /estimate` integration working end-to-end
- [ ] `GET /macro` data displayed with DataSourceBadge
- [ ] Project CRUD (create, list, delete) working
- [ ] Auth (login, register, protected routes) working
- [ ] DataSourceBadge component renders GREEN/AMBER/RED correctly
- [ ] Report download button working

### Agent 04 (Backend) — Done when:
- [ ] All 5 router modules implemented and responding
- [ ] `/estimate` returns prediction in < 3 seconds
- [ ] `/estimate` logs prediction to Supabase predictions table
- [ ] Auth middleware validates Supabase JWT on all protected endpoints
- [ ] PDF report generated by fpdf2 and uploaded to Cloudflare R2
- [ ] `/pipeline` returns Airflow DAG status
- [ ] All Pydantic schemas validated (no 422 errors on valid input)

### Agent 05 (Database) — Done when:
- [ ] All 16 tables verified in Supabase production
- [ ] RLS policies tested for all 3 roles
- [ ] v_latest_macro view returns correct data
- [ ] v_champion_model view returns champion model

### Agent 06 (QA) — Done when:
- [ ] test_estimate.py passes (happy path + error cases)
- [ ] test_api.py passes (auth, 401/403/404 cases)
- [ ] Frontend renders without console errors on all 7 pages

### Agent 07 (Code Review) — Done when:
- [ ] No hardcoded credentials in any file
- [ ] No console.log() in production frontend code
- [ ] All API responses have proper error handling
- [ ] CORS configured for production domain only

### Agent 08 (Docs) — Done when:
- [ ] README.md: setup instructions for both frontend and backend
- [ ] API docs auto-generated at /docs (FastAPI OpenAPI — automatic)

### Agent 09 (DevOps) — Done when:
- [ ] Backend deployed on Railway (health check: GET / → 200)
- [ ] Frontend deployed on Vercel (health check: page loads in < 3s)
- [ ] GitHub Actions test.yml passes on every PR
- [ ] GitHub Actions deploy.yml deploys on merge to main

### Agent 10 (MLOps) — Done when:
- [ ] Champion model loaded from Cloudflare R2 on FastAPI startup
- [ ] `/estimate` SHAP values computed and returned
- [ ] nhces_retrain_weekly DAG configured and scheduled in Airflow

---

## 11. Development Sequence for Claude Code Sessions

| Session | Agent | Deliverables | Estimated Time |
|---------|-------|-------------|----------------|
| O6-S1 | 04 | main.py, config.py, database.py, auth.py | 1 session |
| O6-S2 | 04 | app/ml/inference.py, feature_prep.py, explainer.py | 1 session |
| O6-S3 | 04 | routers/estimate.py + schemas/estimate.py | 1 session |
| O6-S4 | 04 | routers/macro.py, projects.py, reports.py, pipeline.py | 1 session |
| O6-S5 | 04 | services/r2_storage.py, report_generator.py, pipeline_monitor.py | 1 session |
| O6-S6 | 03 | layout.tsx, lib/styles.ts, lib/api.ts, components/ui/* | 1 session |
| O6-S7 | 03 | app/page.tsx (landing), app/estimate/page.tsx | 1 session |
| O6-S8 | 03 | app/dashboard/page.tsx, components/dashboard/* | 1 session |
| O6-S9 | 03 | app/projects/page.tsx, app/reports/page.tsx, app/macro/page.tsx | 1 session |
| O6-S10 | 03 | app/login/page.tsx, app/register/page.tsx, auth middleware | 1 session |
| O6-S11 | 05 | DB verification, RLS testing, migrations | 1 session |
| O6-S12 | 06+07 | tests/, code review | 1 session |
| O6-S13 | 08 | README.md, API docs | 1 session |
| O6-S14 | 09+10 | Dockerfile, railway.toml, vercel.json, deploy.yml | 1 session |

---

*Document: O6_00_Agent01_Project_Plan.md*
*Version: 1.0 — Agent 01 Output*
*DATA SOURCE: AMBER — AI-authored from O3/O4/O5 specifications*
*TETFund NRF 2025 | Department of Quantity Surveying, ABU Zaria*
*All agents must read this document before beginning their work.*
