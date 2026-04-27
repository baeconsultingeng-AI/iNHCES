-- =============================================================================
-- iNHCES ROW LEVEL SECURITY (RLS) POLICIES
-- Intelligent National Housing Cost Estimating System
-- TETFund NRF 2025 | Department of Quantity Surveying, ABU Zaria
--
-- Platform:    Supabase PostgreSQL (PostgreSQL 15+)
-- Run AFTER:   04_schema.sql
-- Generated:   O4 Step 2 | DATA SOURCE: AMBER
--
-- DESIGN PRINCIPLES:
--   1. All tables have RLS enabled — no table is publicly accessible.
--   2. Users can only access their own project/prediction/report data.
--   3. Macro and material data is readable by all authenticated users;
--      writable only by the service_role (Airflow DAGs).
--   4. Admin role has elevated read access (all projects, anonymised).
--   5. ML model registry is readable by all; writable by admin only.
--   6. Audit log is append-only; readable by admin only.
--
-- HELPER: auth.uid()     = UUID of the currently authenticated user
--         auth.role()    = 'authenticated' | 'anon' | 'service_role'
--         current_setting('request.jwt.claims', true)::jsonb->>'role'
--                        = custom role from JWT claim set by Supabase
-- =============================================================================


-- ---------------------------------------------------------------------------
-- HELPER FUNCTION: get current user's role from profiles table
-- ---------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.current_user_role()
RETURNS TEXT LANGUAGE sql STABLE SECURITY DEFINER AS $$
    SELECT role::TEXT FROM public.users WHERE id = auth.uid();
$$;


-- =============================================================================
-- 1. USERS (profiles)
-- =============================================================================
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;

-- Users can read their own profile
CREATE POLICY "users_select_own"
    ON public.users FOR SELECT
    USING (id = auth.uid());

-- Admins can read all profiles
CREATE POLICY "users_select_admin"
    ON public.users FOR SELECT
    USING (public.current_user_role() = 'admin');

-- Users can update their own profile (not role — role change requires admin)
CREATE POLICY "users_update_own"
    ON public.users FOR UPDATE
    USING (id = auth.uid())
    WITH CHECK (id = auth.uid() AND role = (SELECT role FROM public.users WHERE id = auth.uid()));

-- Admins can update any profile including role changes
CREATE POLICY "users_update_admin"
    ON public.users FOR UPDATE
    USING (public.current_user_role() = 'admin');

-- Insert handled by trigger (handle_new_user) via service_role — no user policy needed
-- Delete only via service_role (admin action in dashboard)


-- =============================================================================
-- 2. MACROECONOMIC TABLES
-- Read: all authenticated users. Write: service_role only (Airflow DAGs).
-- =============================================================================

-- macro_fx
ALTER TABLE public.macro_fx ENABLE ROW LEVEL SECURITY;
CREATE POLICY "macro_fx_select_authenticated"
    ON public.macro_fx FOR SELECT
    USING (auth.role() = 'authenticated');
CREATE POLICY "macro_fx_insert_service"
    ON public.macro_fx FOR INSERT
    WITH CHECK (auth.role() = 'service_role');
CREATE POLICY "macro_fx_update_service"
    ON public.macro_fx FOR UPDATE
    USING (auth.role() = 'service_role');

-- macro_cpi
ALTER TABLE public.macro_cpi ENABLE ROW LEVEL SECURITY;
CREATE POLICY "macro_cpi_select_authenticated"
    ON public.macro_cpi FOR SELECT USING (auth.role() = 'authenticated');
CREATE POLICY "macro_cpi_insert_service"
    ON public.macro_cpi FOR INSERT WITH CHECK (auth.role() = 'service_role');
CREATE POLICY "macro_cpi_update_service"
    ON public.macro_cpi FOR UPDATE USING (auth.role() = 'service_role');

-- macro_gdp
ALTER TABLE public.macro_gdp ENABLE ROW LEVEL SECURITY;
CREATE POLICY "macro_gdp_select_authenticated"
    ON public.macro_gdp FOR SELECT USING (auth.role() = 'authenticated');
CREATE POLICY "macro_gdp_insert_service"
    ON public.macro_gdp FOR INSERT WITH CHECK (auth.role() = 'service_role');
CREATE POLICY "macro_gdp_update_service"
    ON public.macro_gdp FOR UPDATE USING (auth.role() = 'service_role');

-- macro_interest
ALTER TABLE public.macro_interest ENABLE ROW LEVEL SECURITY;
CREATE POLICY "macro_interest_select_authenticated"
    ON public.macro_interest FOR SELECT USING (auth.role() = 'authenticated');
CREATE POLICY "macro_interest_insert_service"
    ON public.macro_interest FOR INSERT WITH CHECK (auth.role() = 'service_role');
CREATE POLICY "macro_interest_update_service"
    ON public.macro_interest FOR UPDATE USING (auth.role() = 'service_role');

-- macro_oil
ALTER TABLE public.macro_oil ENABLE ROW LEVEL SECURITY;
CREATE POLICY "macro_oil_select_authenticated"
    ON public.macro_oil FOR SELECT USING (auth.role() = 'authenticated');
CREATE POLICY "macro_oil_insert_service"
    ON public.macro_oil FOR INSERT WITH CHECK (auth.role() = 'service_role');
CREATE POLICY "macro_oil_update_service"
    ON public.macro_oil FOR UPDATE USING (auth.role() = 'service_role');


-- =============================================================================
-- 3. MATERIAL PRICE TABLES
-- Same pattern as macro tables.
-- =============================================================================

-- material_cement
ALTER TABLE public.material_cement ENABLE ROW LEVEL SECURITY;
CREATE POLICY "material_cement_select_authenticated"
    ON public.material_cement FOR SELECT USING (auth.role() = 'authenticated');
CREATE POLICY "material_cement_insert_service"
    ON public.material_cement FOR INSERT WITH CHECK (auth.role() = 'service_role');
CREATE POLICY "material_cement_update_service"
    ON public.material_cement FOR UPDATE USING (auth.role() = 'service_role');

-- material_steel
ALTER TABLE public.material_steel ENABLE ROW LEVEL SECURITY;
CREATE POLICY "material_steel_select_authenticated"
    ON public.material_steel FOR SELECT USING (auth.role() = 'authenticated');
CREATE POLICY "material_steel_insert_service"
    ON public.material_steel FOR INSERT WITH CHECK (auth.role() = 'service_role');
CREATE POLICY "material_steel_update_service"
    ON public.material_steel FOR UPDATE USING (auth.role() = 'service_role');

-- material_pms
ALTER TABLE public.material_pms ENABLE ROW LEVEL SECURITY;
CREATE POLICY "material_pms_select_authenticated"
    ON public.material_pms FOR SELECT USING (auth.role() = 'authenticated');
CREATE POLICY "material_pms_insert_service"
    ON public.material_pms FOR INSERT WITH CHECK (auth.role() = 'service_role');
CREATE POLICY "material_pms_update_service"
    ON public.material_pms FOR UPDATE USING (auth.role() = 'service_role');


-- =============================================================================
-- 4. UNIT RATES AND MARKET PRICES
-- Read: all authenticated. Write: service_role (Airflow + admin upload).
-- =============================================================================

-- unit_rates
ALTER TABLE public.unit_rates ENABLE ROW LEVEL SECURITY;
CREATE POLICY "unit_rates_select_authenticated"
    ON public.unit_rates FOR SELECT USING (auth.role() = 'authenticated');
CREATE POLICY "unit_rates_insert_service"
    ON public.unit_rates FOR INSERT WITH CHECK (auth.role() = 'service_role');
CREATE POLICY "unit_rates_update_service"
    ON public.unit_rates FOR UPDATE USING (auth.role() = 'service_role');
CREATE POLICY "unit_rates_delete_admin"
    ON public.unit_rates FOR DELETE
    USING (public.current_user_role() = 'admin');

-- market_prices
ALTER TABLE public.market_prices ENABLE ROW LEVEL SECURITY;
CREATE POLICY "market_prices_select_authenticated"
    ON public.market_prices FOR SELECT USING (auth.role() = 'authenticated');
CREATE POLICY "market_prices_insert_service"
    ON public.market_prices FOR INSERT WITH CHECK (auth.role() = 'service_role');
CREATE POLICY "market_prices_update_service"
    ON public.market_prices FOR UPDATE USING (auth.role() = 'service_role');


-- =============================================================================
-- 5. PROJECTS
-- Users own their projects. Researchers can read all (anonymised). Admins: all.
-- =============================================================================
ALTER TABLE public.projects ENABLE ROW LEVEL SECURITY;

-- Owner can do everything with their own projects
CREATE POLICY "projects_select_own"
    ON public.projects FOR SELECT
    USING (user_id = auth.uid());

CREATE POLICY "projects_insert_own"
    ON public.projects FOR INSERT
    WITH CHECK (user_id = auth.uid());

CREATE POLICY "projects_update_own"
    ON public.projects FOR UPDATE
    USING (user_id = auth.uid())
    WITH CHECK (user_id = auth.uid());

CREATE POLICY "projects_delete_own"
    ON public.projects FOR DELETE
    USING (user_id = auth.uid());

-- Researchers can read all projects (for aggregate analysis)
-- Note: application layer should anonymise user_id before returning to researcher
CREATE POLICY "projects_select_researcher"
    ON public.projects FOR SELECT
    USING (public.current_user_role() IN ('researcher', 'admin'));


-- =============================================================================
-- 6. PREDICTIONS
-- Users see only their own predictions. Researchers/admins see all.
-- =============================================================================
ALTER TABLE public.predictions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "predictions_select_own"
    ON public.predictions FOR SELECT
    USING (user_id = auth.uid());

-- Only service_role (FastAPI backend) can insert predictions
CREATE POLICY "predictions_insert_service"
    ON public.predictions FOR INSERT
    WITH CHECK (auth.role() = 'service_role');

CREATE POLICY "predictions_select_researcher"
    ON public.predictions FOR SELECT
    USING (public.current_user_role() IN ('researcher', 'admin'));


-- =============================================================================
-- 7. REPORTS
-- Users own their reports. Service_role inserts (FastAPI /reports endpoint).
-- =============================================================================
ALTER TABLE public.reports ENABLE ROW LEVEL SECURITY;

CREATE POLICY "reports_select_own"
    ON public.reports FOR SELECT
    USING (user_id = auth.uid());

CREATE POLICY "reports_insert_service"
    ON public.reports FOR INSERT
    WITH CHECK (auth.role() = 'service_role');

CREATE POLICY "reports_delete_own"
    ON public.reports FOR DELETE
    USING (user_id = auth.uid());

CREATE POLICY "reports_select_admin"
    ON public.reports FOR SELECT
    USING (public.current_user_role() = 'admin');


-- =============================================================================
-- 8. ML MODELS
-- Read: all authenticated. Write: service_role. Promote: admin only.
-- =============================================================================
ALTER TABLE public.ml_models ENABLE ROW LEVEL SECURITY;

CREATE POLICY "ml_models_select_authenticated"
    ON public.ml_models FOR SELECT
    USING (auth.role() = 'authenticated');

-- Service role inserts new model records (from Airflow retrain DAG)
CREATE POLICY "ml_models_insert_service"
    ON public.ml_models FOR INSERT
    WITH CHECK (auth.role() = 'service_role');

-- Only admins can update (e.g., promote to Production, set is_champion)
CREATE POLICY "ml_models_update_admin"
    ON public.ml_models FOR UPDATE
    USING (public.current_user_role() = 'admin');

-- Only admins can archive/delete models
CREATE POLICY "ml_models_delete_admin"
    ON public.ml_models FOR DELETE
    USING (public.current_user_role() = 'admin');


-- =============================================================================
-- 9. AUDIT LOG
-- Append-only for all authenticated + service_role. Read: admin only.
-- =============================================================================
ALTER TABLE public.audit_log ENABLE ROW LEVEL SECURITY;

CREATE POLICY "audit_log_insert_authenticated"
    ON public.audit_log FOR INSERT
    WITH CHECK (auth.role() IN ('authenticated', 'service_role'));

CREATE POLICY "audit_log_select_admin"
    ON public.audit_log FOR SELECT
    USING (public.current_user_role() = 'admin');

-- No UPDATE or DELETE policies — audit log is immutable by design


-- =============================================================================
-- GRANT STATEMENTS
-- These grants are additive to RLS — RLS is the primary access control.
-- =============================================================================

-- Authenticated users: basic read/write access (RLS controls what they see)
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO authenticated;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO authenticated;

-- Service role (Airflow, FastAPI backend): full access
GRANT ALL ON ALL TABLES IN SCHEMA public TO service_role;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO service_role;

-- Anonymous (unauthenticated): no access
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM anon;

-- =============================================================================
-- END OF RLS POLICIES
-- Run 04_seed_data.sql next to load test data.
-- =============================================================================
