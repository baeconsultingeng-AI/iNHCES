# iNHCES Backend API

**Intelligent National Housing Cost Estimating System — FastAPI Backend**  
TETFund NRF 2025 | Department of Quantity Surveying, ABU Zaria

---

## Overview

The iNHCES backend is a FastAPI application that serves ML-based Nigerian housing construction cost estimates. It integrates a LightGBM champion model (MAPE 13.66%, R² 0.91) trained on macroeconomic indicators, provides SHAP explainability, temporal cost projections (1yr / 3yr / 5yr), and manages projects, reports, and pipeline monitoring.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | FastAPI 0.110 + Uvicorn |
| Database | Supabase (PostgreSQL + PostgREST + RLS) |
| ML Inference | LightGBM 4.3, scikit-learn 1.4, SHAP 0.45 |
| Storage | Cloudflare R2 (S3-compatible) |
| Pipeline | Apache Airflow (9 DAGs) |
| ML Tracking | MLflow |
| Auth | Supabase GoTrue JWT (HS256) |
| PDF Reports | fpdf2 |

---

## Project Structure

```
nhces-backend/
├── app/
│   ├── main.py              # FastAPI app, CORS, lifespan
│   ├── config.py            # pydantic-settings (env vars)
│   ├── database.py          # Supabase client singleton + health check
│   ├── auth.py              # JWT validation, role checks
│   ├── ml/
│   │   ├── inference.py     # Model loading (R2 → local → synthetic fallback)
│   │   ├── feature_prep.py  # 14-feature vector from Supabase macro tables
│   │   ├── explainer.py     # SHAP TreeExplainer (LightGBM)
│   │   └── temporal.py      # Compound inflation projections (1yr/3yr/5yr)
│   ├── routers/
│   │   ├── estimate.py      # POST /estimate
│   │   ├── macro.py         # GET /macro, GET /macro/history
│   │   ├── projects.py      # CRUD /projects
│   │   ├── reports.py       # POST/GET /reports
│   │   └── pipeline.py      # GET /pipeline (Airflow DAG status)
│   ├── schemas/             # Pydantic request/response models
│   ├── models/              # SQLAlchemy ORM models (reference)
│   └── services/
│       ├── r2_storage.py    # Cloudflare R2 upload/presign
│       ├── report_generator.py  # PDF report (fpdf2)
│       └── pipeline_monitor.py  # Airflow REST client
├── tests/
│   ├── conftest.py          # Shared fixtures and mock DB factory
│   ├── test_api.py          # Health, docs, CORS (16 tests)
│   ├── test_estimate.py     # /estimate endpoint (25 tests)
│   └── test_pipeline.py     # /macro, /projects, /pipeline (32 tests)
├── requirements.txt
├── .env.example
└── README.md
```

---

## Quick Start

### Prerequisites

- Python 3.10+
- A Supabase project with the iNHCES schema applied (`04_conceptual_models/04_schema.sql`)
- (Optional) Cloudflare R2 bucket for model storage and PDF reports

### 1. Clone and set up environment

```bash
cd nhces-backend
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure environment variables

```bash
cp .env.example .env
# Edit .env and fill in your Supabase URL, keys, etc.
```

Required variables:

| Variable | Description |
|----------|-------------|
| `SUPABASE_URL` | Your Supabase project URL |
| `SUPABASE_ANON_KEY` | Supabase anon/public key |
| `SUPABASE_SERVICE_KEY` | Supabase service role key (never expose to frontend) |
| `SUPABASE_JWT_SECRET` | JWT secret from Supabase dashboard → Settings → API |

Optional variables (synthetic fallback used if absent):

| Variable | Description |
|----------|-------------|
| `CLOUDFLARE_R2_ENDPOINT` | R2 endpoint URL |
| `CLOUDFLARE_R2_ACCESS_KEY` | R2 access key ID |
| `CLOUDFLARE_R2_SECRET_KEY` | R2 secret key |
| `AIRFLOW_API_URL` | Airflow REST API URL (default: `http://localhost:8080/api/v1`) |
| `EIA_API_KEY` | EIA oil price API key (upgrades Brent crude from RED to GREEN) |
| `FRED_API_KEY` | FRED API key (upgrades FX data from RED to GREEN) |

### 3. Run the development server

```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 4. Run the test suite

```bash
python -m pytest tests/ -v
# Expected: 73 passed in ~2 s
```

---

## API Endpoints

### Health

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/` | None | System info and status |
| GET | `/health` | None | DB connectivity + ML model status |

### Estimation

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/estimate` | None | Run ML cost estimation with SHAP + temporal projections |

**Request body** (`POST /estimate`):

```json
{
  "building_type":     "Residential",
  "construction_type": "New Build",
  "floor_area_sqm":    120.0,
  "num_floors":        1,
  "location_state":    "Kaduna",
  "location_zone":     "North West",
  "project_id":        null,
  "target_cost_ngn":   null
}
```

**Response** includes: `predicted_cost_per_sqm`, `total_predicted_cost_ngn`, `confidence_lower/upper`, `shap_top_features`, `projections` (4 horizons), `annual_inflation_rate`, `data_freshness`, `is_synthetic`.

### Macroeconomic Data

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/macro` | None | Latest snapshot of all 7 macro variables |
| GET | `/macro/history` | None | Historical series: `?variable=ngn_usd&years=5` |

Valid `variable` values: `ngn_usd`, `ngn_eur`, `ngn_gbp`, `cpi_annual_pct`, `gdp_growth_pct`, `lending_rate_pct`, `brent_usd_barrel`.

### Projects

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/projects` | Optional | List user projects (empty list if unauthenticated) |
| POST | `/projects` | Required | Create a new project |
| GET | `/projects/{id}` | Required | Get single project |
| PUT | `/projects/{id}` | Required | Update project |
| DELETE | `/projects/{id}` | Required | Delete project |

### Reports

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/reports` | Optional | Generate PDF report → upload to R2 → return presigned URL |
| GET | `/reports` | Optional | List user reports (empty list if unauthenticated) |

### Pipeline

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/pipeline` | None | Airflow DAG health for all 9 iNHCES DAGs |

---

## ML Model

- **Champion**: LightGBM (LOO-CV MAPE 13.66%, R² 0.91)
- **Features** (14): first differences of GDP, CPI, lending rate, Brent crude; % returns of NGN/USD, NGN/EUR, NGN/GBP; lag-1 of all 7
- **Loading priority**: Cloudflare R2 → local `05_ml_models/models/champion_model.pkl` → synthetic fallback
- **Temporal projections**: compound inflation (0.40×CPI + 0.60×FX depreciation), capped at 5 years
- **Data freshness**: GREEN (World Bank live) | AMBER (estimated) | RED (synthetic — must replace)

---

## Data Source Levels

| Level | Meaning |
|-------|---------|
| GREEN | Live API / real measured instrument |
| AMBER | AI-authored template / derived estimate |
| RED | Fully synthetic — **must replace before publication** |

---

## Airflow DAGs (9 total)

| DAG | Schedule | Description |
|-----|----------|-------------|
| `nhces_daily_fx_oil` | `0 5 * * *` | Daily FX + Brent crude |
| `nhces_weekly_materials` | `0 5 * * 1` | Weekly cement + iron rod |
| `nhces_weekly_property` | `0 5 * * 2` | Weekly property listings |
| `nhces_monthly_macro` | `0 5 1 * *` | Monthly CPI, lending rate, PMS |
| `nhces_quarterly_niqs` | Manual | NIQS unit rates |
| `nhces_quarterly_nbs` | `0 5 1 1,4,7,10 *` | NBS quarterly stats |
| `nhces_worldbank_annual` | `0 5 2 1 *` | World Bank GDP + CPI |
| `nhces_retrain_weekly` | `0 1 * * 0` | Weekly champion retrain |
| `nhces_drift_monitor` | `0 17 * * *` | Daily PSI drift detection |

---

## Security Notes

- The `SUPABASE_SERVICE_KEY` bypasses Row Level Security — **never** expose it to the frontend.
- JWT tokens are validated on every protected endpoint using `python-jose` (HS256).
- All database queries use the Supabase SDK (parameterised — no raw SQL injection risk).
- CORS origins are restricted via `ALLOWED_ORIGINS` env var. Set explicitly in production.
- Rotate `SECRET_KEY` and `SUPABASE_JWT_SECRET` before production deployment.

---

## Deployment

See [O6-S14 deployment configuration](../nhces-backend/railway.toml) for Railway deployment.  
The production URL is `https://nhces-api.up.railway.app`.

---

## Research Context

This backend is part of the iNHCES research system developed under TETFund NRF 2025 Grant, Department of Quantity Surveying, Ahmadu Bello University (ABU) Zaria. All synthetic (RED) data sources must be replaced with real survey/API data before any academic publication.

**Principal Investigator**: Department of Quantity Surveying, ABU Zaria  
**Grant**: TETFund National Research Fund (NRF) 2025
