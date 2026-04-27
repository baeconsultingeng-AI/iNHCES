-- =============================================================================
-- iNHCES DATABASE SCHEMA
-- Intelligent National Housing Cost Estimating System
-- TETFund NRF 2025 | Department of Quantity Surveying, ABU Zaria
--
-- Platform:    Supabase PostgreSQL (PostgreSQL 15+)
-- Generated:   O4 Step 2 | DATA SOURCE: AMBER
-- Description: Full schema for all 16 tables covering macroeconomic data,
--              material prices, unit rates, project records, ML model registry,
--              predictions, reports, and audit logging.
--
-- USAGE:
--   Run in Supabase SQL Editor (project -> SQL Editor -> New Query).
--   Execute 04_rls_policies.sql immediately after this script.
--   Execute 04_seed_data.sql to load test data.
--
-- NOTE: auth.users is managed by Supabase GoTrue — do not create it manually.
--       The `users` (profiles) table references auth.users.id.
-- =============================================================================


-- ---------------------------------------------------------------------------
-- EXTENSIONS
-- ---------------------------------------------------------------------------
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";    -- for text search on descriptions


-- ---------------------------------------------------------------------------
-- ENUM TYPES
-- ---------------------------------------------------------------------------
CREATE TYPE user_role         AS ENUM ('qsprofessional', 'researcher', 'admin');
CREATE TYPE project_status    AS ENUM ('active', 'completed', 'archived');
CREATE TYPE building_type     AS ENUM ('Residential', 'Commercial', 'Industrial', 'Institutional', 'Mixed Use');
CREATE TYPE construction_type AS ENUM ('New Build', 'Renovation', 'Extension', 'Fit-Out');
CREATE TYPE model_stage       AS ENUM ('Production', 'Staging', 'Archived');
CREATE TYPE data_source_level AS ENUM ('GREEN', 'AMBER', 'RED');
CREATE TYPE nigeria_zone      AS ENUM ('North Central', 'North East', 'North West', 'South East', 'South South', 'South West');


-- =============================================================================
-- LAYER 1: USER PROFILES
-- References auth.users (Supabase Auth / GoTrue).
-- One row per registered user. Created by trigger on auth.users insert.
-- =============================================================================
CREATE TABLE IF NOT EXISTS public.users (
    id              UUID        PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email           TEXT        UNIQUE NOT NULL,
    full_name       TEXT,
    role            user_role   NOT NULL DEFAULT 'qsprofessional',
    institution     TEXT,
    phone           TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE  public.users          IS 'iNHCES user profiles. Extends Supabase auth.users.';
COMMENT ON COLUMN public.users.role     IS 'qsprofessional: estimate + projects. researcher: + read all. admin: + manage users + promote models.';

-- Trigger: auto-insert profile on new auth.users row
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER LANGUAGE plpgsql SECURITY DEFINER AS $$
BEGIN
    INSERT INTO public.users (id, email, full_name)
    VALUES (NEW.id, NEW.email, NEW.raw_user_meta_data->>'full_name');
    RETURN NEW;
END;
$$;

CREATE OR REPLACE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- Trigger: auto-update updated_at
CREATE OR REPLACE FUNCTION public.set_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN NEW.updated_at = NOW(); RETURN NEW; END;
$$;

CREATE TRIGGER users_updated_at
    BEFORE UPDATE ON public.users
    FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();


-- =============================================================================
-- LAYER 2: MACROECONOMIC DATA TABLES
-- Populated by Airflow DAGs (nhces_daily_fx_oil, nhces_monthly_macro,
-- nhces_worldbank_annual). Service role inserts only.
-- =============================================================================

-- 2a. Exchange rates (daily)
CREATE TABLE IF NOT EXISTS public.macro_fx (
    id              BIGSERIAL   PRIMARY KEY,
    date            DATE        NOT NULL,
    ngn_usd         NUMERIC(12,4) NOT NULL,  -- NGN per 1 USD
    ngn_eur         NUMERIC(12,4),            -- NGN per 1 EUR (cross-rate)
    ngn_gbp         NUMERIC(12,4),            -- NGN per 1 GBP (cross-rate)
    source          TEXT        NOT NULL DEFAULT 'FRED',
    data_level      data_source_level NOT NULL DEFAULT 'RED',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (date)
);
COMMENT ON TABLE public.macro_fx IS 'Daily NGN exchange rates. Source: FRED API (DEXNAUS, cross-rates). data_level=RED until FRED_API_KEY configured.';

-- 2b. CPI / Inflation (monthly or annual)
CREATE TABLE IF NOT EXISTS public.macro_cpi (
    id              BIGSERIAL   PRIMARY KEY,
    date            DATE        NOT NULL,       -- first day of period
    frequency       TEXT        NOT NULL DEFAULT 'annual',  -- 'monthly', 'annual'
    cpi_annual_pct  NUMERIC(8,4) NOT NULL,      -- % annual change
    source          TEXT        NOT NULL DEFAULT 'World Bank',
    data_level      data_source_level NOT NULL DEFAULT 'GREEN',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (date, frequency)
);
COMMENT ON TABLE public.macro_cpi IS 'Nigeria CPI inflation rate. Source: World Bank Open Data API (FP.CPI.TOTL.ZG). data_level=GREEN.';

-- 2c. GDP growth (annual)
CREATE TABLE IF NOT EXISTS public.macro_gdp (
    id                  BIGSERIAL   PRIMARY KEY,
    date                DATE        NOT NULL,   -- year start (YYYY-01-01)
    gdp_growth_pct      NUMERIC(8,4) NOT NULL,  -- real GDP growth %
    gdp_per_capita_usd  NUMERIC(12,2),          -- USD per capita (optional)
    source              TEXT        NOT NULL DEFAULT 'World Bank',
    data_level          data_source_level NOT NULL DEFAULT 'GREEN',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (date)
);
COMMENT ON TABLE public.macro_gdp IS 'Nigeria annual GDP growth. Source: World Bank (NY.GDP.MKTP.KD.ZG). data_level=GREEN.';

-- 2d. Lending rate / MPR (monthly or annual)
CREATE TABLE IF NOT EXISTS public.macro_interest (
    id              BIGSERIAL   PRIMARY KEY,
    date            DATE        NOT NULL,
    frequency       TEXT        NOT NULL DEFAULT 'annual',
    lending_rate_pct NUMERIC(8,4) NOT NULL,     -- commercial lending rate %
    mpr_pct         NUMERIC(8,4),               -- CBN Monetary Policy Rate %
    source          TEXT        NOT NULL DEFAULT 'World Bank',
    data_level      data_source_level NOT NULL DEFAULT 'GREEN',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (date, frequency)
);
COMMENT ON TABLE public.macro_interest IS 'Nigeria lending rate and MPR. Source: World Bank (FR.INR.LEND) + CBN. data_level=GREEN.';

-- 2e. Brent crude oil price (daily or monthly)
CREATE TABLE IF NOT EXISTS public.macro_oil (
    id                  BIGSERIAL   PRIMARY KEY,
    date                DATE        NOT NULL,
    frequency           TEXT        NOT NULL DEFAULT 'annual',
    brent_usd_barrel    NUMERIC(10,4) NOT NULL,
    source              TEXT        NOT NULL DEFAULT 'EIA',
    data_level          data_source_level NOT NULL DEFAULT 'RED',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (date, frequency)
);
COMMENT ON TABLE public.macro_oil IS 'Brent crude oil price. Source: EIA API (PET.RBRTE.A). data_level=RED until EIA_API_KEY configured.';


-- =============================================================================
-- LAYER 3: MATERIAL PRICE TABLES
-- Populated by Airflow DAGs (nhces_weekly_materials, nhces_monthly_macro).
-- =============================================================================

-- 3a. Cement prices by brand and region (weekly)
CREATE TABLE IF NOT EXISTS public.material_cement (
    id              BIGSERIAL   PRIMARY KEY,
    date            DATE        NOT NULL,
    brand           TEXT        NOT NULL,   -- 'Dangote', 'BUA', 'Lafarge', 'UNICEM', 'Ibeto'
    region          TEXT        NOT NULL,   -- 'North', 'South-West', 'South-East', 'South-South'
    state           TEXT,                   -- optional (more granular)
    price_ngn_50kg  NUMERIC(10,2) NOT NULL, -- price per 50kg bag, NGN
    source          TEXT        NOT NULL DEFAULT 'BusinessDay',
    data_level      data_source_level NOT NULL DEFAULT 'RED',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (date, brand, region)
);
COMMENT ON TABLE public.material_cement IS 'Cement prices by brand and region. Source: BusinessDay scraper. Weekly frequency.';

-- 3b. Iron rod / reinforcement steel prices (weekly)
CREATE TABLE IF NOT EXISTS public.material_steel (
    id                  BIGSERIAL   PRIMARY KEY,
    date                DATE        NOT NULL,
    diameter_mm         INTEGER     NOT NULL CHECK (diameter_mm IN (8,10,12,16,20,25,32)),
    region              TEXT        NOT NULL,
    state               TEXT,
    price_ngn_tonne     NUMERIC(12,2) NOT NULL,
    source              TEXT        NOT NULL DEFAULT 'Jiji.ng',
    data_level          data_source_level NOT NULL DEFAULT 'RED',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (date, diameter_mm, region)
);
COMMENT ON TABLE public.material_steel IS 'Iron rod prices by diameter and region. Source: Jiji.ng / BuildBay scraper. Weekly.';

-- 3c. PMS (petrol) pump price by state (monthly)
CREATE TABLE IF NOT EXISTS public.material_pms (
    id                  BIGSERIAL   PRIMARY KEY,
    date                DATE        NOT NULL,
    state               TEXT        NOT NULL,
    price_ngn_litre     NUMERIC(8,2) NOT NULL,
    source              TEXT        NOT NULL DEFAULT 'NNPC',
    data_level          data_source_level NOT NULL DEFAULT 'RED',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (date, state)
);
COMMENT ON TABLE public.material_pms IS 'PMS (petrol) pump prices by state. Source: NNPC/NMDPRA. Monthly frequency.';


-- =============================================================================
-- LAYER 4: UNIT RATES AND MARKET PRICES
-- =============================================================================

-- 4a. NIQS unit rates by trade, region, and building type (quarterly)
CREATE TABLE IF NOT EXISTS public.unit_rates (
    id              BIGSERIAL   PRIMARY KEY,
    quarter_date    DATE        NOT NULL,   -- quarter start: YYYY-01-01 / YYYY-04-01 etc.
    trade           TEXT        NOT NULL,   -- 'Substructure', 'Frame', 'Roofing', 'Finishes', etc.
    description     TEXT        NOT NULL,   -- specific work item
    unit            TEXT        NOT NULL,   -- 'm2', 'm3', 'nr', 'lm', 'item', 'tonne'
    region          TEXT        NOT NULL,
    building_type   building_type NOT NULL DEFAULT 'Residential',
    rate_ngn        NUMERIC(12,2) NOT NULL,
    source          TEXT        NOT NULL DEFAULT 'NIQS',
    data_level      data_source_level NOT NULL DEFAULT 'RED',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
COMMENT ON TABLE public.unit_rates IS 'NIQS quarterly unit rates by trade and region. Uploaded manually via admin dashboard.';

-- 4b. Property listing market prices by zone (weekly)
CREATE TABLE IF NOT EXISTS public.market_prices (
    id                  BIGSERIAL   PRIMARY KEY,
    date                DATE        NOT NULL,
    zone                nigeria_zone NOT NULL,
    state               TEXT        NOT NULL,
    city                TEXT,
    property_type       TEXT        NOT NULL,   -- 'Bungalow', 'Duplex', 'Flat', 'Terrace', 'Detached'
    price_ngn_sqm       NUMERIC(12,2) NOT NULL,
    listing_count       INTEGER     DEFAULT 1,  -- number of listings averaged
    source              TEXT        NOT NULL DEFAULT 'PropertyPro',
    data_level          data_source_level NOT NULL DEFAULT 'RED',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (date, zone, state, property_type, source)
);
COMMENT ON TABLE public.market_prices IS 'Property listing prices (NGN/sqm). Source: PropertyPro + PrivateProperty scrapers. Weekly.';


-- =============================================================================
-- LAYER 5: PROJECT AND PREDICTION RECORDS
-- User-owned. RLS enforces row-level isolation.
-- =============================================================================

-- 5a. Projects
CREATE TABLE IF NOT EXISTS public.projects (
    id                  UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id             UUID        NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    title               TEXT        NOT NULL,
    building_type       building_type NOT NULL DEFAULT 'Residential',
    construction_type   construction_type NOT NULL DEFAULT 'New Build',
    floor_area_sqm      NUMERIC(10,2) NOT NULL CHECK (floor_area_sqm > 0),
    num_floors          INTEGER     NOT NULL DEFAULT 1 CHECK (num_floors >= 1),
    location_state      TEXT        NOT NULL,
    location_zone       nigeria_zone NOT NULL,
    location_lga        TEXT,
    target_cost_ngn     NUMERIC(15,2),          -- client budget, optional
    notes               TEXT,
    status              project_status NOT NULL DEFAULT 'active',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
COMMENT ON TABLE public.projects IS 'iNHCES cost estimation projects. Each project belongs to one user. RLS enforced.';

CREATE TRIGGER projects_updated_at
    BEFORE UPDATE ON public.projects
    FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();


-- 5b. ML Predictions (log of all /estimate calls)
CREATE TABLE IF NOT EXISTS public.predictions (
    id                      UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id              UUID        NOT NULL REFERENCES public.projects(id) ON DELETE CASCADE,
    user_id                 UUID        NOT NULL REFERENCES public.users(id),  -- denormalised for RLS
    model_version           TEXT        NOT NULL,   -- MLflow run_id
    model_stage             model_stage NOT NULL DEFAULT 'Production',
    predicted_cost_per_sqm  NUMERIC(12,2) NOT NULL,
    total_predicted_cost_ngn NUMERIC(15,2),          -- per_sqm * floor_area_sqm
    confidence_lower        NUMERIC(12,2),
    confidence_upper        NUMERIC(12,2),
    mape_at_prediction      NUMERIC(8,4),            -- champion model MAPE at time of call
    feature_snapshot        JSONB,                   -- macro + material features used
    shap_values             JSONB,                   -- SHAP per feature {feature: shap_value}
    api_response_ms         INTEGER,                 -- /estimate endpoint response time
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
COMMENT ON TABLE public.predictions IS 'Log of every /estimate API call. Includes feature snapshot and SHAP values for explainability audit.';

CREATE INDEX idx_predictions_project  ON public.predictions(project_id);
CREATE INDEX idx_predictions_user     ON public.predictions(user_id);
CREATE INDEX idx_predictions_created  ON public.predictions(created_at DESC);


-- =============================================================================
-- LAYER 6: REPORTS
-- =============================================================================
CREATE TABLE IF NOT EXISTS public.reports (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id      UUID        NOT NULL REFERENCES public.projects(id) ON DELETE CASCADE,
    prediction_id   UUID        REFERENCES public.predictions(id) ON DELETE SET NULL,
    user_id         UUID        NOT NULL REFERENCES public.users(id),
    r2_key          TEXT        NOT NULL UNIQUE,    -- Cloudflare R2 object key
    file_size_bytes INTEGER,
    page_count      INTEGER,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
COMMENT ON TABLE public.reports IS 'PDF cost report records. Actual PDF files stored in Cloudflare R2; r2_key is the object path.';


-- =============================================================================
-- LAYER 7: ML MODEL REGISTRY (mirrors MLflow)
-- =============================================================================
CREATE TABLE IF NOT EXISTS public.ml_models (
    id                  UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    mlflow_run_id       TEXT        UNIQUE NOT NULL,
    model_name          TEXT        NOT NULL,   -- 'stacking_ensemble', 'xgboost', 'rf', etc.
    stage               model_stage NOT NULL DEFAULT 'Staging',
    mape_test           NUMERIC(8,4),           -- % MAPE on holdout test set
    r2_test             NUMERIC(8,4),           -- R2 on holdout test set
    mae_test            NUMERIC(12,2),          -- MAE in NGN/sqm
    training_date       DATE,
    feature_count       INTEGER,
    training_rows       INTEGER,
    r2_artifact_key     TEXT,                   -- Cloudflare R2 path to .pkl file
    hyperparameters     JSONB,                  -- model hyperparameters
    feature_importance  JSONB,                  -- SHAP importance {feature: pct}
    is_champion         BOOLEAN     NOT NULL DEFAULT FALSE,
    promoted_by         UUID        REFERENCES public.users(id),  -- admin who promoted
    promoted_at         TIMESTAMPTZ,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
COMMENT ON TABLE public.ml_models IS 'ML model registry mirroring MLflow. is_champion=TRUE for the current Production model used by /estimate.';

-- Ensure only one champion at a time
CREATE UNIQUE INDEX idx_ml_models_one_champion ON public.ml_models(is_champion)
    WHERE is_champion = TRUE;


-- =============================================================================
-- LAYER 8: AUDIT LOG
-- =============================================================================
CREATE TABLE IF NOT EXISTS public.audit_log (
    id          BIGSERIAL   PRIMARY KEY,
    user_id     UUID        REFERENCES public.users(id) ON DELETE SET NULL,
    action      TEXT        NOT NULL,   -- 'login', 'predict', 'export_report', 'promote_model', 'admin_action'
    table_name  TEXT,
    record_id   TEXT,                   -- string representation of affected record PK
    old_values  JSONB,
    new_values  JSONB,
    ip_address  INET,
    user_agent  TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
COMMENT ON TABLE public.audit_log IS 'System-wide audit trail. All significant user actions are logged here. INSERT-only (no UPDATE or DELETE).';

CREATE INDEX idx_audit_log_user    ON public.audit_log(user_id);
CREATE INDEX idx_audit_log_action  ON public.audit_log(action);
CREATE INDEX idx_audit_log_created ON public.audit_log(created_at DESC);


-- =============================================================================
-- HELPER VIEWS
-- =============================================================================

-- Latest macro snapshot (most recent record per variable) for /macro endpoint
CREATE OR REPLACE VIEW public.v_latest_macro AS
SELECT
    'ngn_usd'   AS variable,
    date        AS as_of_date,
    ngn_usd     AS value,
    source,
    data_level::TEXT
FROM public.macro_fx
WHERE date = (SELECT MAX(date) FROM public.macro_fx)
UNION ALL
SELECT 'cpi_annual_pct', date, cpi_annual_pct, source, data_level::TEXT
FROM public.macro_cpi WHERE date = (SELECT MAX(date) FROM public.macro_cpi)
UNION ALL
SELECT 'gdp_growth_pct', date, gdp_growth_pct, source, data_level::TEXT
FROM public.macro_gdp WHERE date = (SELECT MAX(date) FROM public.macro_gdp)
UNION ALL
SELECT 'lending_rate_pct', date, lending_rate_pct, source, data_level::TEXT
FROM public.macro_interest WHERE date = (SELECT MAX(date) FROM public.macro_interest)
UNION ALL
SELECT 'brent_usd_barrel', date, brent_usd_barrel, source, data_level::TEXT
FROM public.macro_oil WHERE date = (SELECT MAX(date) FROM public.macro_oil);

COMMENT ON VIEW public.v_latest_macro IS 'Single-row-per-variable latest macro snapshot. Used by FastAPI GET /macro endpoint.';


-- Champion model summary view for /estimate endpoint
CREATE OR REPLACE VIEW public.v_champion_model AS
SELECT id, mlflow_run_id, model_name, mape_test, r2_test, r2_artifact_key,
       feature_importance, training_date, training_rows, promoted_at
FROM public.ml_models
WHERE is_champion = TRUE;

COMMENT ON VIEW public.v_champion_model IS 'Single-row view of the current Production (champion) ML model.';


-- =============================================================================
-- END OF SCHEMA
-- Run 04_rls_policies.sql next.
-- =============================================================================
