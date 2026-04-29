-- =============================================================================
-- iNHCES SEED DATA
-- Intelligent National Housing Cost Estimating System
-- TETFund NRF 2025 | Department of Quantity Surveying, ABU Zaria
--
-- Platform:    Supabase PostgreSQL
-- Run AFTER:   04_schema.sql AND 04_rls_policies.sql
-- Generated:   O4 Step 2 | DATA SOURCE: RED (synthetic test data)
--
-- PURPOSE:
--   Provides representative test data for development and unit testing.
--   All values are SYNTHETIC — based on approximate real-world ranges for
--   Nigerian construction costs and macroeconomic data (2024 estimates).
--   DO NOT use this data for any published analysis or grant reporting.
--
-- USAGE:
--   Run in Supabase SQL Editor with service_role privileges (bypasses RLS).
--   To reset: run DELETE FROM <table> WHERE source LIKE '%seed%' or
--   truncate all tables and re-run in order.
--
-- WARNING: This script uses hardcoded UUIDs for test users to allow
--   reproducible foreign key references across tables. Replace with
--   real auth.users.id values when deploying to production.
-- =============================================================================

-- ---------------------------------------------------------------------------
-- TEST USER PROFILES
-- Step 1: Insert into auth.users first (required by FK constraint).
-- Step 2: public.users is then populated (trigger or manual insert below).
-- Requires service_role privileges in the Supabase SQL editor.
-- ---------------------------------------------------------------------------

-- Step 1: seed auth.users
INSERT INTO auth.users (
    id, email, encrypted_password,
    email_confirmed_at, created_at, updated_at,
    raw_app_meta_data, raw_user_meta_data,
    aud, role, confirmation_token, recovery_token,
    is_super_admin
) VALUES
    ('00000000-0000-0000-0000-000000000001',
     'qs.professional@test.nhces.ng',
     crypt('TestPassword123!', gen_salt('bf')),
     NOW(), NOW(), NOW(),
     '{"provider":"email","providers":["email"]}'::jsonb,
     '{"full_name":"Aisha Bello (Test QS)"}'::jsonb,
     'authenticated', 'authenticated', '', '', FALSE),
    ('00000000-0000-0000-0000-000000000002',
     'researcher@test.nhces.ng',
     crypt('TestPassword123!', gen_salt('bf')),
     NOW(), NOW(), NOW(),
     '{"provider":"email","providers":["email"]}'::jsonb,
     '{"full_name":"Dr. Ibrahim Yusuf (Test Researcher)"}'::jsonb,
     'authenticated', 'authenticated', '', '', FALSE),
    ('00000000-0000-0000-0000-000000000003',
     'admin@test.nhces.ng',
     crypt('TestPassword123!', gen_salt('bf')),
     NOW(), NOW(), NOW(),
     '{"provider":"email","providers":["email"]}'::jsonb,
     '{"full_name":"Prof. Musa Abdullahi (Test Admin)"}'::jsonb,
     'authenticated', 'authenticated', '', '', FALSE)
ON CONFLICT (id) DO NOTHING;

-- Step 2: seed public.users (FK to auth.users now satisfied)
INSERT INTO public.users (id, email, full_name, role, institution) VALUES
    ('00000000-0000-0000-0000-000000000001',
     'qs.professional@test.nhces.ng',
     'Aisha Bello (Test QS)',
     'qsprofessional',
     'ABU Zaria, Dept. of Quantity Surveying'),
    ('00000000-0000-0000-0000-000000000002',
     'researcher@test.nhces.ng',
     'Dr. Ibrahim Yusuf (Test Researcher)',
     'researcher',
     'ABU Zaria, Dept. of Quantity Surveying'),
    ('00000000-0000-0000-0000-000000000003',
     'admin@test.nhces.ng',
     'Prof. Musa Abdullahi (Test Admin)',
     'admin',
     'ABU Zaria, Dept. of Quantity Surveying')
ON CONFLICT (id) DO NOTHING;


-- ---------------------------------------------------------------------------
-- MACROECONOMIC DATA (annual, 2020-2024 approximate synthetic values)
-- Data level = RED (synthetic seed data)
-- ---------------------------------------------------------------------------

-- Exchange rates (NGN/USD — approximate CBN official rates)
INSERT INTO public.macro_fx (date, ngn_usd, ngn_eur, ngn_gbp, source, data_level) VALUES
    ('2020-01-01', 381.00,  415.50,  487.20, 'seed-synthetic', 'RED'),
    ('2021-01-01', 410.00,  488.00,  556.00, 'seed-synthetic', 'RED'),
    ('2022-01-01', 425.00,  477.00,  512.00, 'seed-synthetic', 'RED'),
    ('2023-01-01', 750.00,  824.00,  953.00, 'seed-synthetic', 'RED'),
    ('2024-01-01', 1480.00, 1598.00, 1863.00,'seed-synthetic', 'RED')
ON CONFLICT (date) DO NOTHING;

-- CPI annual inflation (%)
INSERT INTO public.macro_cpi (date, frequency, cpi_annual_pct, source, data_level) VALUES
    ('2020-01-01', 'annual', 13.20, 'seed-synthetic', 'RED'),
    ('2021-01-01', 'annual', 17.00, 'seed-synthetic', 'RED'),
    ('2022-01-01', 'annual', 19.60, 'seed-synthetic', 'RED'),
    ('2023-01-01', 'annual', 24.50, 'seed-synthetic', 'RED'),
    ('2024-01-01', 'annual', 31.70, 'seed-synthetic', 'RED')
ON CONFLICT (date, frequency) DO NOTHING;

-- GDP growth (%)
INSERT INTO public.macro_gdp (date, gdp_growth_pct, gdp_per_capita_usd, source, data_level) VALUES
    ('2020-01-01', -1.80,  2097.00, 'seed-synthetic', 'RED'),
    ('2021-01-01',  3.40,  2065.00, 'seed-synthetic', 'RED'),
    ('2022-01-01',  3.30,  2184.00, 'seed-synthetic', 'RED'),
    ('2023-01-01',  2.90,  1598.00, 'seed-synthetic', 'RED'),
    ('2024-01-01',  3.10,  1110.00, 'seed-synthetic', 'RED')
ON CONFLICT (date) DO NOTHING;

-- Lending rate (%)
INSERT INTO public.macro_interest (date, frequency, lending_rate_pct, mpr_pct, source, data_level) VALUES
    ('2020-01-01', 'annual', 25.80, 11.50, 'seed-synthetic', 'RED'),
    ('2021-01-01', 'annual', 26.20, 11.50, 'seed-synthetic', 'RED'),
    ('2022-01-01', 'annual', 26.70, 16.50, 'seed-synthetic', 'RED'),
    ('2023-01-01', 'annual', 27.30, 18.75, 'seed-synthetic', 'RED'),
    ('2024-01-01', 'annual', 29.50, 26.25, 'seed-synthetic', 'RED')
ON CONFLICT (date, frequency) DO NOTHING;

-- Brent crude (USD/barrel)
INSERT INTO public.macro_oil (date, frequency, brent_usd_barrel, source, data_level) VALUES
    ('2020-01-01', 'annual', 41.96,  'seed-synthetic', 'RED'),
    ('2021-01-01', 'annual', 70.68,  'seed-synthetic', 'RED'),
    ('2022-01-01', 'annual', 99.04,  'seed-synthetic', 'RED'),
    ('2023-01-01', 'annual', 82.49,  'seed-synthetic', 'RED'),
    ('2024-01-01', 'annual', 80.00,  'seed-synthetic', 'RED')
ON CONFLICT (date, frequency) DO NOTHING;


-- ---------------------------------------------------------------------------
-- MATERIAL PRICES (2024 approximate synthetic values)
-- ---------------------------------------------------------------------------

-- Cement prices (NGN per 50kg bag, approximate 2024 ranges)
INSERT INTO public.material_cement (date, brand, region, state, price_ngn_50kg, source, data_level) VALUES
    ('2024-01-01', 'Dangote',  'North',       'Kaduna',   8500.00, 'seed-synthetic', 'RED'),
    ('2024-01-01', 'Dangote',  'South-West',  'Lagos',    9200.00, 'seed-synthetic', 'RED'),
    ('2024-01-01', 'Dangote',  'South-East',  'Enugu',    9800.00, 'seed-synthetic', 'RED'),
    ('2024-01-01', 'Dangote',  'South-South', 'Rivers',   10200.00,'seed-synthetic', 'RED'),
    ('2024-01-01', 'BUA',      'North',       'Abuja',    8300.00, 'seed-synthetic', 'RED'),
    ('2024-01-01', 'BUA',      'South-West',  'Lagos',    8900.00, 'seed-synthetic', 'RED'),
    ('2024-01-01', 'Lafarge',  'South-West',  'Lagos',    9000.00, 'seed-synthetic', 'RED'),
    ('2024-01-01', 'UNICEM',   'South-East',  'Calabar',  9500.00, 'seed-synthetic', 'RED')
ON CONFLICT (date, brand, region) DO NOTHING;

-- Steel / iron rod prices (NGN per tonne, approximate 2024)
INSERT INTO public.material_steel (date, diameter_mm, region, state, price_ngn_tonne, source, data_level) VALUES
    ('2024-01-01', 12, 'North',       'Kaduna',   580000.00, 'seed-synthetic', 'RED'),
    ('2024-01-01', 16, 'North',       'Kaduna',   600000.00, 'seed-synthetic', 'RED'),
    ('2024-01-01', 12, 'South-West',  'Lagos',    620000.00, 'seed-synthetic', 'RED'),
    ('2024-01-01', 16, 'South-West',  'Lagos',    640000.00, 'seed-synthetic', 'RED'),
    ('2024-01-01', 12, 'South-East',  'Enugu',    650000.00, 'seed-synthetic', 'RED'),
    ('2024-01-01', 16, 'South-East',  'Enugu',    670000.00, 'seed-synthetic', 'RED'),
    ('2024-01-01', 20, 'South-West',  'Lagos',    680000.00, 'seed-synthetic', 'RED')
ON CONFLICT (date, diameter_mm, region) DO NOTHING;

-- PMS (petrol) pump prices (NGN per litre, approximate 2024 deregulated prices)
INSERT INTO public.material_pms (date, state, price_ngn_litre, source, data_level) VALUES
    ('2024-01-01', 'Lagos',    617.00, 'seed-synthetic', 'RED'),
    ('2024-01-01', 'Kaduna',   640.00, 'seed-synthetic', 'RED'),
    ('2024-01-01', 'Abuja',    625.00, 'seed-synthetic', 'RED'),
    ('2024-01-01', 'Kano',     650.00, 'seed-synthetic', 'RED'),
    ('2024-01-01', 'Rivers',   610.00, 'seed-synthetic', 'RED'),
    ('2024-01-01', 'Enugu',    660.00, 'seed-synthetic', 'RED'),
    ('2024-01-01', 'Anambra',  665.00, 'seed-synthetic', 'RED')
ON CONFLICT (date, state) DO NOTHING;


-- ---------------------------------------------------------------------------
-- UNIT RATES (NIQS approximate 2024 — synthetic seed data)
-- ---------------------------------------------------------------------------
INSERT INTO public.unit_rates (quarter_date, trade, description, unit, region, building_type, rate_ngn, source, data_level) VALUES
    ('2024-01-01', 'Substructure', 'Excavate topsoil (150mm deep)', 'm2',       'North',      'Residential', 1200.00,   'seed-synthetic', 'RED'),
    ('2024-01-01', 'Substructure', 'Mass concrete grade 15 (150mm)', 'm2',      'North',      'Residential', 18500.00,  'seed-synthetic', 'RED'),
    ('2024-01-01', 'Frame',        'Reinforced concrete column (300x300)', 'm3','South-West', 'Residential', 165000.00, 'seed-synthetic', 'RED'),
    ('2024-01-01', 'Frame',        'Reinforced concrete beam', 'm3',            'South-West', 'Residential', 155000.00, 'seed-synthetic', 'RED'),
    ('2024-01-01', 'Frame',        'Reinforced concrete slab (150mm)', 'm2',    'South-West', 'Residential', 32000.00,  'seed-synthetic', 'RED'),
    ('2024-01-01', 'Walling',      'Sandcrete block wall (225mm)', 'm2',        'North',      'Residential', 14500.00,  'seed-synthetic', 'RED'),
    ('2024-01-01', 'Walling',      'Sandcrete block wall (150mm)', 'm2',        'North',      'Residential', 11000.00,  'seed-synthetic', 'RED'),
    ('2024-01-01', 'Roofing',      'Long span aluminium roof sheeting', 'm2',   'North',      'Residential', 9500.00,   'seed-synthetic', 'RED'),
    ('2024-01-01', 'Roofing',      'Aluminium fascia and gutter', 'lm',         'North',      'Residential', 3500.00,   'seed-synthetic', 'RED'),
    ('2024-01-01', 'Finishes',     'Cement and sand floor screed (50mm)', 'm2', 'South-West', 'Residential', 8200.00,   'seed-synthetic', 'RED'),
    ('2024-01-01', 'Finishes',     'Ceramic floor tiles (300x300)', 'm2',       'South-West', 'Residential', 22000.00,  'seed-synthetic', 'RED'),
    ('2024-01-01', 'Finishes',     'Internal cement render (13mm)', 'm2',       'South-West', 'Residential', 5500.00,   'seed-synthetic', 'RED'),
    ('2024-01-01', 'Finishes',     'Emulsion paint (2 coats)', 'm2',            'South-West', 'Residential', 3200.00,   'seed-synthetic', 'RED'),
    ('2024-01-01', 'M&E',          'PVC conduit wiring (per point)', 'nr',      'South-West', 'Residential', 28000.00,  'seed-synthetic', 'RED'),
    ('2024-01-01', 'M&E',          'UPVC soil pipe (110mm)', 'lm',             'South-West', 'Residential', 12000.00,  'seed-synthetic', 'RED')
ON CONFLICT DO NOTHING;


-- ---------------------------------------------------------------------------
-- MARKET PRICES (approximate 2024 NGN/sqm property listings)
-- ---------------------------------------------------------------------------
INSERT INTO public.market_prices (date, zone, state, city, property_type, price_ngn_sqm, listing_count, source, data_level) VALUES
    ('2024-01-01', 'South West',  'Lagos',  'Lekki',   'Detached',  680000.00, 45, 'seed-synthetic', 'RED'),
    ('2024-01-01', 'South West',  'Lagos',  'Surulere','Flat',       320000.00, 78, 'seed-synthetic', 'RED'),
    ('2024-01-01', 'South West',  'Ogun',   'Abeokuta','Bungalow',   195000.00, 32, 'seed-synthetic', 'RED'),
    ('2024-01-01', 'North Central','Abuja', 'Maitama', 'Detached',   850000.00, 22, 'seed-synthetic', 'RED'),
    ('2024-01-01', 'North Central','Abuja', 'Kubwa',   'Terrace',    280000.00, 55, 'seed-synthetic', 'RED'),
    ('2024-01-01', 'North West',  'Kaduna', 'Kaduna',  'Bungalow',   145000.00, 38, 'seed-synthetic', 'RED'),
    ('2024-01-01', 'South East',  'Enugu',  'Enugu',   'Duplex',     230000.00, 28, 'seed-synthetic', 'RED'),
    ('2024-01-01', 'South South', 'Rivers', 'Port Harcourt','Flat',  380000.00, 42, 'seed-synthetic', 'RED')
ON CONFLICT (date, zone, state, property_type, source) DO NOTHING;


-- ---------------------------------------------------------------------------
-- TEST PROJECTS
-- ---------------------------------------------------------------------------
INSERT INTO public.projects (id, user_id, title, building_type, construction_type,
    floor_area_sqm, num_floors, location_state, location_zone, notes, status) VALUES
    ('10000000-0000-0000-0000-000000000001',
     '00000000-0000-0000-0000-000000000001',
     'Test Project A — 3-Bed Bungalow, Kaduna',
     'Residential', 'New Build',
     120.00, 1, 'Kaduna', 'North West',
     'Seed data test project. Synthetic data only.',
     'active'),
    ('10000000-0000-0000-0000-000000000002',
     '00000000-0000-0000-0000-000000000001',
     'Test Project B — 4-Bed Duplex, Lagos',
     'Residential', 'New Build',
     250.00, 2, 'Lagos', 'South West',
     'Seed data test project. Synthetic data only.',
     'active')
ON CONFLICT (id) DO NOTHING;


-- ---------------------------------------------------------------------------
-- TEST ML MODEL RECORD (synthetic champion for development testing)
-- ---------------------------------------------------------------------------
INSERT INTO public.ml_models (
    id, mlflow_run_id, model_name, stage,
    mape_test, r2_test, mae_test,
    training_date, feature_count, training_rows,
    r2_artifact_key, hyperparameters, feature_importance,
    is_champion
) VALUES (
    '20000000-0000-0000-0000-000000000001',
    'seed-run-00000000000000001',
    'stacking_ensemble',
    'Production',
    12.40, 0.934, 18500.00,
    '2024-01-01', 7, 200,
    'models/seed-run-00000000000000001/model.pkl',
    '{"xgb_n_estimators": 200, "rf_n_estimators": 150, "meta_learner": "Ridge"}'::jsonb,
    '{"ngn_usd": 45.0, "cpi_annual_pct": 25.5, "ngn_eur": 11.6, "brent_usd_barrel": 10.9, "ngn_gbp": 3.8, "gdp_growth_pct": 2.1, "lending_rate_pct": 1.1}'::jsonb,
    TRUE
) ON CONFLICT (mlflow_run_id) DO NOTHING;


-- ---------------------------------------------------------------------------
-- TEST PREDICTION
-- ---------------------------------------------------------------------------
INSERT INTO public.predictions (
    id, project_id, user_id,
    model_version, model_stage,
    predicted_cost_per_sqm, total_predicted_cost_ngn,
    confidence_lower, confidence_upper, mape_at_prediction,
    feature_snapshot, shap_values
) VALUES (
    '30000000-0000-0000-0000-000000000001',
    '10000000-0000-0000-0000-000000000001',
    '00000000-0000-0000-0000-000000000001',
    'seed-run-00000000000000001', 'Production',
    182500.00, 21900000.00,
    152000.00, 213000.00, 12.40,
    '{"ngn_usd": 1480.0, "cpi_annual_pct": 31.7, "ngn_eur": 1598.0, "brent_usd_barrel": 80.0, "ngn_gbp": 1863.0, "gdp_growth_pct": 3.1, "lending_rate_pct": 29.5}'::jsonb,
    '{"ngn_usd": 82125.0, "cpi_annual_pct": 46537.5, "ngn_eur": 21170.0, "brent_usd_barrel": 19881.25, "ngn_gbp": 6935.0, "gdp_growth_pct": 3832.5, "lending_rate_pct": 2008.75}'::jsonb
) ON CONFLICT (id) DO NOTHING;


-- ---------------------------------------------------------------------------
-- AUDIT LOG ENTRY (record that seed data was loaded)
-- ---------------------------------------------------------------------------
INSERT INTO public.audit_log (user_id, action, table_name, record_id, new_values) VALUES
    (NULL, 'seed_data_loaded', 'ALL', 'seed-v1.0',
     '{"note": "iNHCES seed data v1.0 loaded. O4 Step 2. All data is synthetic (RED level). Do not use for analysis."}'::jsonb);


-- =============================================================================
-- END OF SEED DATA
-- Verify with:
--   SELECT COUNT(*) FROM public.macro_fx;        -- expect 5
--   SELECT COUNT(*) FROM public.material_cement; -- expect 8
--   SELECT COUNT(*) FROM public.unit_rates;      -- expect 15
--   SELECT COUNT(*) FROM public.projects;        -- expect 2
--   SELECT is_champion FROM public.ml_models;    -- expect 1 TRUE row
-- =============================================================================
