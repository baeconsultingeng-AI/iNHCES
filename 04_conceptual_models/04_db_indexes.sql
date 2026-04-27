-- =============================================================================
-- iNHCES PERFORMANCE INDEXES
-- Additional indexes beyond those defined in 04_schema.sql.
-- Run AFTER: 04_schema.sql
-- Generated: O6 Step 11 (Agent 05) | DATA SOURCE: AMBER
--
-- Target: predictions table (highest query volume at scale)
--         macro tables (time-series range queries)
--         projects table (user-scoped list queries)
-- =============================================================================


-- ---------------------------------------------------------------------------
-- PREDICTIONS TABLE (most queried at scale)
-- ---------------------------------------------------------------------------

-- User's predictions ordered by date (dashboard + reports page)
CREATE INDEX IF NOT EXISTS idx_predictions_user_created
    ON public.predictions(user_id, created_at DESC);

-- Project's predictions for project summary view
CREATE INDEX IF NOT EXISTS idx_predictions_project_created
    ON public.predictions(project_id, created_at DESC);

-- Champion model version lookups (drift monitor comparison)
CREATE INDEX IF NOT EXISTS idx_predictions_model_version
    ON public.predictions(model_version);

-- JSONB GIN index for feature_snapshot queries (SHAP analysis, audit)
CREATE INDEX IF NOT EXISTS idx_predictions_feature_snapshot
    ON public.predictions USING GIN(feature_snapshot);


-- ---------------------------------------------------------------------------
-- MACRO TABLES (time-series range queries)
-- ---------------------------------------------------------------------------

-- macro_fx: latest N rows, date range queries
CREATE INDEX IF NOT EXISTS idx_macro_fx_date_desc
    ON public.macro_fx(date DESC);

CREATE INDEX IF NOT EXISTS idx_macro_fx_data_level
    ON public.macro_fx(data_level);

-- macro_cpi
CREATE INDEX IF NOT EXISTS idx_macro_cpi_date_desc
    ON public.macro_cpi(date DESC, frequency);

-- macro_gdp
CREATE INDEX IF NOT EXISTS idx_macro_gdp_date_desc
    ON public.macro_gdp(date DESC);

-- macro_interest
CREATE INDEX IF NOT EXISTS idx_macro_interest_date_desc
    ON public.macro_interest(date DESC, frequency);

-- macro_oil
CREATE INDEX IF NOT EXISTS idx_macro_oil_date_desc
    ON public.macro_oil(date DESC, frequency);


-- ---------------------------------------------------------------------------
-- MATERIAL PRICE TABLES (scraper insert performance + range queries)
-- ---------------------------------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_material_cement_date_brand
    ON public.material_cement(date DESC, brand, region);

CREATE INDEX IF NOT EXISTS idx_material_steel_date_diam
    ON public.material_steel(date DESC, diameter_mm, region);

CREATE INDEX IF NOT EXISTS idx_material_pms_date_state
    ON public.material_pms(date DESC, state);


-- ---------------------------------------------------------------------------
-- PROJECTS TABLE
-- ---------------------------------------------------------------------------

-- User projects list (already has partial index for RLS; add status filter)
CREATE INDEX IF NOT EXISTS idx_projects_user_status
    ON public.projects(user_id, status, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_projects_location
    ON public.projects(location_zone, location_state);


-- ---------------------------------------------------------------------------
-- ML MODELS TABLE
-- ---------------------------------------------------------------------------

-- Staging candidates lookup (weekly comparison)
CREATE INDEX IF NOT EXISTS idx_ml_models_stage_mape
    ON public.ml_models(stage, mape_test ASC NULLS LAST);


-- ---------------------------------------------------------------------------
-- AUDIT LOG TABLE (admin queries — large table at scale)
-- ---------------------------------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_audit_log_action_created
    ON public.audit_log(action, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_audit_log_table_created
    ON public.audit_log(table_name, created_at DESC);


-- =============================================================================
-- VERIFY INDEXES (run after to confirm all created)
-- =============================================================================
-- SELECT indexname, tablename FROM pg_indexes
-- WHERE schemaname = 'public'
-- ORDER BY tablename, indexname;
-- =============================================================================
