-- =============================================================================
-- iNHCES DATABASE FUNCTIONS
-- Supabase PostgreSQL — Helper functions for the FastAPI backend
-- Run AFTER: 04_schema.sql and 04_rls_policies.sql
-- Generated: O6 Step 11 (Agent 05) | DATA SOURCE: AMBER
--
-- Functions:
--   1. get_latest_macro_snapshot()     — used by GET /macro endpoint
--   2. get_user_project_summary()      — used by GET /projects with statistics
--   3. get_champion_model()            — used by POST /estimate ML loading
--   4. log_audit_event()               — used by all write endpoints
--   5. refresh_champion_flag()         — used by model promotion workflow
-- =============================================================================


-- ---------------------------------------------------------------------------
-- 1. get_latest_macro_snapshot()
-- Returns the most recent value for each of the 7 macro variables.
-- Used by: FastAPI GET /macro endpoint (replaces v_latest_macro view)
-- ---------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.get_latest_macro_snapshot()
RETURNS TABLE(
    variable    TEXT,
    label       TEXT,
    value       NUMERIC,
    unit        TEXT,
    as_of_date  DATE,
    source      TEXT,
    data_level  TEXT
)
LANGUAGE sql STABLE SECURITY DEFINER AS $$
    -- NGN/USD exchange rate
    (SELECT 'ngn_usd'::TEXT, 'NGN/USD Exchange Rate', ngn_usd, 'NGN per USD',
           date, source, data_level::TEXT
    FROM public.macro_fx ORDER BY date DESC LIMIT 1)
    UNION ALL
    -- NGN/EUR exchange rate
    (SELECT 'ngn_eur', 'NGN/EUR Exchange Rate', ngn_eur, 'NGN per EUR',
           date, source, data_level::TEXT
    FROM public.macro_fx ORDER BY date DESC LIMIT 1)
    UNION ALL
    -- NGN/GBP exchange rate
    (SELECT 'ngn_gbp', 'NGN/GBP Exchange Rate', ngn_gbp, 'NGN per GBP',
           date, source, data_level::TEXT
    FROM public.macro_fx ORDER BY date DESC LIMIT 1)
    UNION ALL
    -- CPI inflation
    (SELECT 'cpi_annual_pct', 'CPI Inflation (Annual)', cpi_annual_pct, '% per annum',
           date, source, data_level::TEXT
    FROM public.macro_cpi ORDER BY date DESC LIMIT 1)
    UNION ALL
    -- GDP growth
    (SELECT 'gdp_growth_pct', 'GDP Growth Rate', gdp_growth_pct, '% per annum',
           date, source, data_level::TEXT
    FROM public.macro_gdp ORDER BY date DESC LIMIT 1)
    UNION ALL
    -- Lending rate
    (SELECT 'lending_rate_pct', 'Lending Interest Rate', lending_rate_pct, '% per annum',
           date, source, data_level::TEXT
    FROM public.macro_interest ORDER BY date DESC LIMIT 1)
    UNION ALL
    -- Brent crude
    (SELECT 'brent_usd_barrel', 'Brent Crude Oil Price', brent_usd_barrel, 'USD per barrel',
           date, source, data_level::TEXT
    FROM public.macro_oil ORDER BY date DESC LIMIT 1);
$$;

COMMENT ON FUNCTION public.get_latest_macro_snapshot() IS
    'Returns the most recent value for each of the 7 iNHCES macro variables. '
    'Used by FastAPI GET /macro endpoint.';


-- ---------------------------------------------------------------------------
-- 2. get_user_project_summary(p_user_id UUID)
-- Returns all projects for a user with their latest prediction attached.
-- Used by: FastAPI GET /projects endpoint (enhanced version)
-- ---------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.get_user_project_summary(p_user_id UUID)
RETURNS TABLE(
    project_id              UUID,
    title                   TEXT,
    building_type           TEXT,
    construction_type       TEXT,
    floor_area_sqm          NUMERIC,
    location_state          TEXT,
    location_zone           TEXT,
    status                  TEXT,
    created_at              TIMESTAMPTZ,
    latest_cost_per_sqm     NUMERIC,
    latest_total_cost_ngn   NUMERIC,
    latest_prediction_date  TIMESTAMPTZ,
    prediction_count        BIGINT
)
LANGUAGE sql STABLE SECURITY DEFINER AS $$
    SELECT
        p.id,
        p.title,
        p.building_type,
        p.construction_type,
        p.floor_area_sqm,
        p.location_state,
        p.location_zone,
        p.status,
        p.created_at,
        latest_pred.predicted_cost_per_sqm,
        latest_pred.total_predicted_cost_ngn,
        latest_pred.created_at,
        pred_count.cnt
    FROM public.projects p
    -- Latest prediction per project
    LEFT JOIN LATERAL (
        SELECT predicted_cost_per_sqm, total_predicted_cost_ngn, created_at
        FROM public.predictions
        WHERE project_id = p.id
        ORDER BY created_at DESC
        LIMIT 1
    ) latest_pred ON TRUE
    -- Total prediction count per project
    LEFT JOIN LATERAL (
        SELECT COUNT(*) AS cnt
        FROM public.predictions
        WHERE project_id = p.id
    ) pred_count ON TRUE
    WHERE p.user_id = p_user_id
    ORDER BY p.created_at DESC;
$$;

COMMENT ON FUNCTION public.get_user_project_summary(UUID) IS
    'Returns all projects for a user with their latest prediction and count. '
    'Used by FastAPI GET /projects for an enriched project list.';


-- ---------------------------------------------------------------------------
-- 3. get_champion_model()
-- Returns metadata for the current Production champion model.
-- Used by: FastAPI /estimate endpoint model metadata loading
-- ---------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.get_champion_model()
RETURNS TABLE(
    id                  UUID,
    mlflow_run_id       TEXT,
    model_name          TEXT,
    mape_test           NUMERIC,
    r2_test             NUMERIC,
    r2_artifact_key     TEXT,
    feature_importance  JSONB,
    training_date       DATE,
    training_rows       INTEGER,
    promoted_at         TIMESTAMPTZ
)
LANGUAGE sql STABLE SECURITY DEFINER AS $$
    SELECT id, mlflow_run_id, model_name, mape_test, r2_test,
           r2_artifact_key, feature_importance, training_date,
           training_rows, promoted_at
    FROM public.ml_models
    WHERE is_champion = TRUE
    LIMIT 1;
$$;

COMMENT ON FUNCTION public.get_champion_model() IS
    'Returns the current Production champion ML model metadata. '
    'Guaranteed to return at most one row (enforced by partial unique index).';


-- ---------------------------------------------------------------------------
-- 4. log_audit_event()
-- Convenience function for inserting audit log entries.
-- Used by: all FastAPI write endpoints via the database service layer
-- ---------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.log_audit_event(
    p_user_id    UUID,
    p_action     TEXT,
    p_table_name TEXT DEFAULT NULL,
    p_record_id  TEXT DEFAULT NULL,
    p_new_values JSONB DEFAULT NULL,
    p_old_values JSONB DEFAULT NULL
)
RETURNS void
LANGUAGE sql SECURITY DEFINER AS $$
    INSERT INTO public.audit_log(user_id, action, table_name, record_id, new_values, old_values)
    VALUES (p_user_id, p_action, p_table_name, p_record_id, p_new_values, p_old_values);
$$;

COMMENT ON FUNCTION public.log_audit_event(UUID, TEXT, TEXT, TEXT, JSONB, JSONB) IS
    'Convenience function for inserting audit log entries. '
    'Wraps INSERT INTO audit_log with SECURITY DEFINER to bypass RLS.';


-- ---------------------------------------------------------------------------
-- 5. refresh_champion_flag(p_new_run_id TEXT)
-- Atomically demotes old champion and promotes a new one.
-- Called by: Airflow nhces_retrain_weekly DAG (promote task)
-- ---------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.refresh_champion_flag(p_new_run_id TEXT)
RETURNS void
LANGUAGE plpgsql SECURITY DEFINER AS $$
BEGIN
    -- Demote current champion
    UPDATE public.ml_models
    SET is_champion = FALSE, stage = 'Archived'
    WHERE is_champion = TRUE;

    -- Promote new champion
    UPDATE public.ml_models
    SET is_champion = TRUE, stage = 'Production', promoted_at = NOW()
    WHERE mlflow_run_id = p_new_run_id;

    -- Log the promotion
    INSERT INTO public.audit_log(action, table_name, record_id, new_values)
    VALUES (
        'promote_model', 'ml_models', p_new_run_id,
        jsonb_build_object('promoted_at', NOW(), 'run_id', p_new_run_id)
    );
END;
$$;

COMMENT ON FUNCTION public.refresh_champion_flag(TEXT) IS
    'Atomically promotes a new champion model and archives the old one. '
    'Called by the Airflow nhces_retrain_weekly DAG promote task.';


-- =============================================================================
-- GRANT EXECUTE on all functions to authenticated + service_role
-- =============================================================================
GRANT EXECUTE ON FUNCTION public.get_latest_macro_snapshot()          TO authenticated, service_role;
GRANT EXECUTE ON FUNCTION public.get_user_project_summary(UUID)       TO authenticated, service_role;
GRANT EXECUTE ON FUNCTION public.get_champion_model()                  TO authenticated, service_role;
GRANT EXECUTE ON FUNCTION public.log_audit_event(UUID,TEXT,TEXT,TEXT,JSONB,JSONB) TO service_role;
GRANT EXECUTE ON FUNCTION public.refresh_champion_flag(TEXT)           TO service_role;

-- =============================================================================
-- END OF DB FUNCTIONS
-- =============================================================================
