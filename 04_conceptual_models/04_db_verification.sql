-- =============================================================================
-- iNHCES DATABASE VERIFICATION SCRIPT
-- Run this in Supabase SQL Editor to verify the schema is correctly deployed.
-- Generated: O6 Step 11 (Agent 05) | DATA SOURCE: AMBER
--
-- EXPECTED RESULTS documented inline.
-- Any deviation from expected results must be investigated before O6 launch.
-- =============================================================================


-- ---------------------------------------------------------------------------
-- CHECK 1: All 16 tables exist
-- Expected: 16 rows returned
-- ---------------------------------------------------------------------------
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_type = 'BASE TABLE'
ORDER BY table_name;
-- Expected tables: audit_log, macro_cpi, macro_fx, macro_gdp, macro_interest,
--   macro_oil, market_prices, material_cement, material_steel, material_pms,
--   ml_models, predictions, projects, reports, unit_rates, users


-- ---------------------------------------------------------------------------
-- CHECK 2: RLS is enabled on all 16 tables
-- Expected: 16 rows, all rowsecurity = true
-- ---------------------------------------------------------------------------
SELECT tablename, rowsecurity
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY tablename;


-- ---------------------------------------------------------------------------
-- CHECK 3: Both helper views exist
-- Expected: 2 rows (v_champion_model, v_latest_macro)
-- ---------------------------------------------------------------------------
SELECT viewname
FROM pg_views
WHERE schemaname = 'public'
ORDER BY viewname;


-- ---------------------------------------------------------------------------
-- CHECK 4: All 5 DB functions exist
-- Expected: 5 rows
-- ---------------------------------------------------------------------------
SELECT routine_name, routine_type
FROM information_schema.routines
WHERE routine_schema = 'public'
  AND routine_type = 'FUNCTION'
ORDER BY routine_name;
-- Expected: get_champion_model, get_latest_macro_snapshot,
--   get_user_project_summary, log_audit_event, refresh_champion_flag,
--   handle_new_user, set_updated_at


-- ---------------------------------------------------------------------------
-- CHECK 5: 7 enum types exist
-- Expected: 7 rows
-- ---------------------------------------------------------------------------
SELECT typname
FROM pg_type
WHERE typtype = 'e'
  AND typnamespace = (SELECT oid FROM pg_namespace WHERE nspname = 'public')
ORDER BY typname;
-- Expected: building_type, construction_type, data_source_level,
--   model_stage, nigeria_zone, project_status, user_role


-- ---------------------------------------------------------------------------
-- CHECK 6: Partial unique index on ml_models (champion constraint)
-- Expected: 1 row
-- ---------------------------------------------------------------------------
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'ml_models'
  AND indexname = 'idx_ml_models_one_champion';


-- ---------------------------------------------------------------------------
-- CHECK 7: v_latest_macro view returns 7 rows (one per variable)
-- Expected: 7 rows (or 0 if no data loaded yet)
-- ---------------------------------------------------------------------------
SELECT COUNT(*) AS variable_count FROM public.v_latest_macro;


-- ---------------------------------------------------------------------------
-- CHECK 8: Seed data verification (only if seed was run)
-- Expected: counts match values in 04_seed_data.sql comments
-- ---------------------------------------------------------------------------
SELECT
    'macro_fx'          AS tbl, COUNT(*) AS cnt FROM public.macro_fx      UNION ALL
SELECT 'macro_cpi',              COUNT(*) FROM public.macro_cpi           UNION ALL
SELECT 'material_cement',        COUNT(*) FROM public.material_cement     UNION ALL
SELECT 'unit_rates',             COUNT(*) FROM public.unit_rates          UNION ALL
SELECT 'projects',               COUNT(*) FROM public.projects            UNION ALL
SELECT 'predictions',            COUNT(*) FROM public.predictions         UNION ALL
SELECT 'ml_models',              COUNT(*) FROM public.ml_models
ORDER BY 1;
-- Expected with seed data: macro_fx=5, macro_cpi=5, material_cement=8,
--   unit_rates=15, projects=2, predictions=1, ml_models=1


-- ---------------------------------------------------------------------------
-- CHECK 9: Champion model exists and is_champion constraint works
-- Expected: exactly 1 row
-- ---------------------------------------------------------------------------
SELECT id, model_name, is_champion, mape_test, stage
FROM public.ml_models
WHERE is_champion = TRUE;


-- ---------------------------------------------------------------------------
-- CHECK 10: RLS policy counts per table
-- Expected: each table has at least 2 policies (SELECT + INSERT/UPDATE)
-- ---------------------------------------------------------------------------
SELECT tablename, COUNT(*) AS policy_count
FROM pg_policies
WHERE schemaname = 'public'
GROUP BY tablename
ORDER BY tablename;


-- ---------------------------------------------------------------------------
-- CHECK 11: Test get_latest_macro_snapshot() function
-- Expected: up to 7 rows with variable names, values, data_level
-- ---------------------------------------------------------------------------
SELECT * FROM public.get_latest_macro_snapshot();


-- ---------------------------------------------------------------------------
-- CHECK 12: Test get_champion_model() function
-- Expected: 1 row (after seed data) or 0 rows (empty DB)
-- ---------------------------------------------------------------------------
SELECT * FROM public.get_champion_model();


-- ---------------------------------------------------------------------------
-- CHECK 13: Trigger exists on users table
-- Expected: handle_new_user trigger present
-- ---------------------------------------------------------------------------
SELECT trigger_name, event_manipulation, event_object_table
FROM information_schema.triggers
WHERE trigger_schema = 'public'
ORDER BY event_object_table, trigger_name;


-- ---------------------------------------------------------------------------
-- CHECK 14: All additional performance indexes exist
-- Expected: see 04_db_indexes.sql for full list
-- ---------------------------------------------------------------------------
SELECT COUNT(*) AS index_count
FROM pg_indexes
WHERE schemaname = 'public';
-- Expected: at least 25 indexes (schema + additional)


-- =============================================================================
-- RLS POLICY TESTS (requires test JWT tokens — run with Supabase test client)
-- =============================================================================

-- Test 1: anon user cannot SELECT from any table
-- Run as: supabase.table('projects').select('*') with anon key → expect 0 rows

-- Test 2: qsprofessional user sees only own projects
-- Run as: supabase.table('projects').select('*') with qsprofessional JWT
-- → expect only rows WHERE user_id = auth.uid()

-- Test 3: service_role can INSERT into macro_fx
-- Run as: supabase.table('macro_fx').insert({...}) with service_role key
-- → expect success

-- Test 4: qsprofessional cannot INSERT into macro_fx
-- Run as: supabase.table('macro_fx').insert({...}) with qsprofessional JWT
-- → expect 403 Forbidden

-- =============================================================================
-- END OF VERIFICATION SCRIPT
-- All 14 SQL checks should pass before proceeding to O6-S12 (QA).
-- =============================================================================
