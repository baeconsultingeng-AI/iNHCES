# Chapter 4: Conceptual System Design

**iNHCES — Intelligent National Housing Cost Estimating System**
TETFund NRF 2025 | Department of Quantity Surveying, ABU Zaria

> **DATA SOURCE: AMBER** — AI-authored first draft. Research team must validate
> against O3 Delphi consensus, SRS IEEE 830, and Research Advisory Framework
> before inclusion in any thesis chapter, conference paper, or grant report.
> All citations marked [VERIFY] must be independently checked in Scopus/WoS.

---

## 4.1 Introduction

This chapter presents the conceptual design of the Intelligent National Housing Cost
Estimating System (iNHCES), translating the system requirements elicited through the
three-round Delphi consensus process (Chapter 3) into formal architectural and
behavioural specifications. The conceptual design serves two purposes: it provides the
implementation blueprint for the O6 development phase, and it constitutes the
theoretical contribution of iNHCES to the system design literature on AI-augmented
cost estimation in developing-economy construction sectors.

The conceptual design is organised across four interconnected artefacts, each developed
as a formal model:

1. **System Architecture** (Section 4.2): a seven-layer cloud-native architecture
   specifying all components, technology choices, and inter-component relationships.
2. **Database Schema** (Section 4.3): a normalised relational schema for Supabase
   PostgreSQL comprising sixteen tables, seven enumerated types, and two helper views,
   with row-level security policies governing all data access.
3. **Data Flow Diagrams** (Section 4.4): a two-level DFD decomposition (context and
   process levels) defining all system processes, data stores, and data flows.
4. **Pipeline and User Journey Models** (Section 4.5): an Airflow-based data ingestion
   and ML retraining pipeline design, and satisfaction-scored user journey maps for the
   primary and secondary user personas.

Together, these artefacts address the 36 Delphi consensus items across seven
functional categories and satisfy all 47 functional requirements documented in the
iNHCES Software Requirements Specification (SRS, IEEE 830, O3 Step 4).

---

## 4.2 System Architecture

### 4.2.1 Architecture Philosophy

The iNHCES architecture follows three guiding principles derived from the Delphi
consensus:

- **Separation of concerns**: data ingestion, ML inference, API logic, and frontend
  presentation are deployed as independently scalable services. This addresses Delphi
  Category F (Performance and Scalability) items F1-F6, which required that the system
  support concurrent user requests without performance degradation.
- **Data provenance transparency**: every data record in the system carries a
  `data_source_level` field (GREEN/AMBER/RED) reflecting its reliability. This directly
  implements the iNHCES Simulation-to-Publication Framework obligation and supports
  Delphi Category D (Security and Privacy) item D5 (data quality disclosure).
- **Cost-appropriate technology**: all platform choices prioritise free or low-cost
  tiers suitable for an academic research prototype, while remaining upgradeable to
  production-scale equivalents without architectural changes.

### 4.2.2 Seven-Layer Architecture

The iNHCES system is organised into seven layers (see `04_Architecture_Diagram.mmd`):

| Layer | Technology | Hosting | Primary Responsibility |
|-------|-----------|---------|----------------------|
| 1. User | Browser (any) | — | HTTPS access |
| 2. Presentation | Vanilla HTML/CSS/JS | Vercel CDN | Cost estimator form; pipeline dashboard |
| 3. API | FastAPI (Python 3.10+) | Railway | Business logic; JWT auth; routing; PDF generation |
| 4. ML | MLflow Model Registry | Railway | Champion model serving; experiment tracking; retrain orchestration |
| 5. Data | Supabase PostgreSQL | Supabase | All persistent data: macro, materials, projects, predictions, models, users |
| 6. Storage | Cloudflare R2 | Cloudflare | PDF reports; model artefacts; training datasets |
| 7. Pipeline | Apache Airflow | Railway | 9 DAGs for data ingestion, weekly ML retrain, daily drift monitoring |

**Rationale for key technology choices:**

*FastAPI over Django/Flask*: FastAPI provides automatic OpenAPI/Swagger documentation
critical for academic transparency, native async support for concurrent calls to
Supabase and MLflow, and Pydantic-based request validation aligned with the typed
feature schema from the database design. Response time for the /estimate endpoint is
projected at under three seconds, meeting the Delphi Category F performance target.

*Supabase PostgreSQL over NoSQL alternatives*: The iNHCES data model is fundamentally
relational — time-series macroeconomic data with foreign keys to project and prediction
records. Supabase provides PostgreSQL (SQL, JOINs, window functions), built-in row-level
security, GoTrue authentication (JWT), and a Python client within a single free-tier
platform, eliminating the need for a separate authentication service.

*Cloudflare R2 over AWS S3*: R2 has zero egress fees compared to AWS S3's
approximately USD 0.09/GB. For an academic prototype generating PDF reports and serving
model artefacts, zero egress cost is decisive. R2 is S3-API-compatible, enabling
migration to S3 with only an endpoint URL change if required at production scale.

*Apache Airflow over Prefect/Dagster*: Airflow is the industry-standard orchestrator
with the largest community and most mature operator library. The nine-DAG schedule maps
naturally to Airflow's cron-based scheduler, and the `SqlSensor` operator handles the
drift monitor's database condition check natively.

### 4.2.3 Security Architecture

Three security mechanisms work in combination:

1. **JWT Authentication** (Supabase GoTrue): All API endpoints require a valid JWT
   access token (one-hour expiry) issued by Supabase on login. The FastAPI JWT
   middleware validates the token signature on every request.
2. **Row Level Security (RLS)**: All sixteen database tables have RLS enabled.
   Users can read and write only their own project, prediction, and report records.
   Macroeconomic and material data is readable by all authenticated users but writable
   only by the service role (Airflow pipelines).
3. **Role-Based Access Control (RBAC)**: Three roles are defined — `qsprofessional`
   (estimate and projects), `researcher` (plus aggregate data read), and `admin`
   (plus user management and model promotion).

---

## 4.3 Database Design

### 4.3.1 Schema Overview

The iNHCES database schema (file: `04_schema.sql`) comprises sixteen tables organised
into five functional groups. The schema is designed for deployment on Supabase
PostgreSQL 15+.

**Macroeconomic Data Tables** (5 tables):
`macro_fx`, `macro_cpi`, `macro_gdp`, `macro_interest`, `macro_oil` — store the seven
macroeconomic variables identified as significant determinants of housing construction
costs in O2 (SHAP analysis). Each row records a time-stamped observation with a
`data_source_level` field tracking data quality.

**Material Price Tables** (3 tables):
`material_cement`, `material_steel`, `material_pms` — store weekly cement prices
(by brand and region), iron rod prices (by diameter and region), and monthly petrol
(PMS) pump prices (by state). These address the material cost variables identified
in the O1 QS survey (parameter RII rankings).

**Unit Rates and Market Prices** (2 tables):
`unit_rates` stores NIQS quarterly unit rates by trade, region, and building type.
`market_prices` stores weekly property listing prices (NGN/sqm) by zone and property
type from PropertyPro and PrivateProperty scrapers.

**Project and Prediction Records** (3 tables):
`projects`, `predictions`, `reports` — user-owned records with RLS enforcement.
The `predictions` table includes a `feature_snapshot` JSONB column recording the
exact macro and material feature values used for each prediction (explainability
audit trail) and a `shap_values` JSONB column for per-feature SHAP contributions.

**System Management Tables** (3 tables):
`users` (extends Supabase `auth.users`), `ml_models` (mirrors MLflow registry),
`audit_log` (append-only audit trail for all significant actions).

### 4.3.2 Key Design Decisions

**JSONB for SHAP values and feature snapshots**: Storing `shap_values` and
`feature_snapshot` as JSONB in the `predictions` table, rather than normalising them
into separate rows, enables the `/estimate` endpoint to return the full prediction
record in a single query while keeping the schema flexible as the feature set evolves
across ML retraining cycles. The trade-off is reduced queryability of individual SHAP
values; a JSONB GIN index can mitigate this if needed in O6.

**`data_source_level` enum on every macro/material table**: Rather than maintaining a
separate data quality table, the `data_source_level` (GREEN/AMBER/RED) is stored
directly on every observation row. This enables the `/macro` endpoint to report
data provenance in real time and allows the frontend to display freshness warnings
without a separate API call.

**Unique constraint on champion model**: A partial unique index
(`WHERE is_champion = TRUE`) on the `ml_models` table enforces at the database level
that exactly one model is in Production at any time, preventing race conditions during
the weekly champion promotion workflow.

**Denormalised `user_id` in `predictions`**: The `user_id` is stored directly in the
`predictions` table (in addition to `project_id` → `projects.user_id`) to enable
efficient RLS policy evaluation without a JOIN to the `projects` table on every
prediction query.

### 4.3.3 Normalisation and Referential Integrity

The schema is in Third Normal Form (3NF). All transitive dependencies have been
eliminated. Referential integrity is enforced by PostgreSQL foreign key constraints with
appropriate cascade rules:

- `projects.user_id → users.id ON DELETE CASCADE`: deleting a user removes all their projects.
- `predictions.project_id → projects.id ON DELETE CASCADE`: deleting a project removes its predictions.
- `reports.prediction_id → predictions.id ON DELETE SET NULL`: deleting a prediction
  retains the report record (the PDF file in R2 is not automatically deleted).

---

## 4.4 Data Flow Model

### 4.4.1 DFD Level 0 — System Boundary

The Level 0 DFD (context diagram, file: `04_DFD_Level0.mmd`) defines the iNHCES system
boundary. Three categories of external entity interact with the system:

**Human users**: QS Professional (primary), Researcher/PI (secondary), System Admin
(operations). The QS Professional is the primary source of project input data and the
primary consumer of cost estimates and PDF reports.

**Automated data sources**: World Bank Open Data API, EIA API, FRED/CBN API,
PropertyPro and Private Property scrapers, BusinessDay and Jiji.ng scrapers,
NNPC/NMDPRA, and NIQS (manual upload). These eight sources collectively provide all
macroeconomic and material price features required by the ML prediction model.

**CI/CD infrastructure**: GitHub Actions, which triggers deployment of the FastAPI
backend and Vercel frontend on push to the main branch.

### 4.4.2 DFD Level 1 — Process Decomposition

The Level 1 DFD (file: `04_DFD_Level1.mmd`) decomposes the system into six processes:

**Process 1.0 — User Authentication**: Issues and validates JWT tokens via Supabase
GoTrue. Logs all authentication events to the `audit_log` table. Maps directly to
SRS requirement FR-AUTH-01 through FR-AUTH-06.

**Process 2.0 — Cost Estimation**: The core ML inference pipeline. Receives project
parameters, assembles the feature vector from the latest Supabase macro and material
records, loads the champion model artefact from Cloudflare R2, and returns the
predicted `cost_per_sqm` with confidence interval, feature snapshot, and SHAP values.
Target response time: under three seconds. Maps to SRS requirements FR-EST-01
through FR-EST-12.

**Process 3.0 — Data Ingestion Pipeline**: All seven Airflow ingestion DAGs. Collects
data from external sources, validates schema and value ranges, and inserts records into
the appropriate Supabase tables. Handles synthetic fallback when API keys are absent.
Maps to SRS requirements FR-DATA-01 through FR-DATA-09.

**Process 4.0 — ML Model Management**: The weekly retrain and champion promotion
workflow. Assembles the feature matrix, trains the full model family, logs experiments
to MLflow, and conditionally promotes a challenger to champion if MAPE improves by more
than 0.5 percentage points. Maps to SRS requirements FR-ML-01 through FR-ML-08.

**Process 5.0 — Report Generation**: Compiles project, prediction, and SHAP data into
a professional PDF report using fpdf2, uploads to Cloudflare R2, and returns a
presigned download URL. Maps to SRS requirements FR-RPT-01 through FR-RPT-05.

**Process 6.0 — Pipeline Monitoring**: Daily PSI drift detection across all ML
features. Compares the latest 30-day feature distribution against the champion model's
training baseline. Triggers an emergency retrain if PSI exceeds 0.2 for any top-4
SHAP feature. Provides pipeline health status to Admin and Researcher. Maps to
SRS requirements FR-MON-01 through FR-MON-06.

---

## 4.5 Pipeline Architecture and User Experience

### 4.5.1 Airflow Pipeline Design

The nine-DAG Airflow pipeline (file: `04_Pipeline_Flow.mmd`) is the data backbone of
iNHCES. DAGs are organised into three tiers by cadence:

**High-frequency DAGs** (daily and weekly): `nhces_daily_fx_oil` (06:00 WAT daily)
and the two weekly scrapers (`nhces_weekly_materials`, `nhces_weekly_property`)
maintain the most volatile features — exchange rates, material prices, and property
listings — at near-real-time freshness.

**Low-frequency DAGs** (monthly to annual): `nhces_monthly_macro`,
`nhces_quarterly_niqs`, `nhces_quarterly_nbs`, and `nhces_worldbank_annual` maintain
the more stable macroeconomic series. Their lower cadence is appropriate because GDP
growth, CPI inflation, and lending rates change more slowly than commodity prices.

**ML management DAGs**: `nhces_retrain_weekly` (Sunday 02:00 WAT) performs the weekly
champion-challenger comparison. `nhces_drift_monitor` (18:00 WAT daily) detects
feature distribution shift using Population Stability Index (PSI) and triggers
emergency retraining when PSI > 0.2 for any top-4 SHAP feature.

The retrain pipeline implements the champion-challenger promotion methodology
recommended by Christensen and Larsen (2020) [VERIFY] for production ML systems:
retain the current champion until a statistically meaningful improvement is confirmed
(MAPE improvement >= 0.5%), preventing unnecessary model churn while ensuring
continuous improvement.

### 4.5.2 User Experience Design

The user journey analysis (file: `04_User_Journey.mmd`) identifies three pain points
requiring design attention:

1. **Data freshness transparency**: When EIA or FRED API keys are not configured,
   exchange rate and oil price data remain at RED level. The estimation results page
   must display a prominent freshness warning with the as-of date for each feature,
   colour-coded GREEN/AMBER/RED. This is architecturally supported by the
   `data_source_level` field on all macro and material tables.
2. **Report URL expiry**: The 24-hour Cloudflare R2 presigned URL creates friction
   for users who do not download the report immediately. The O6 frontend will include
   a persistent report history page with on-demand URL refresh.
3. **Model transparency**: Researchers require direct access to MLflow experiment
   history. The O6 admin dashboard will include a read-only MLflow link accessible
   to the researcher role.

---

## 4.6 Requirements Traceability

The following table maps the seven Delphi functional categories to their primary
realisation in the iNHCES conceptual design. All 36 consensus items (of 38 total;
B6, C6, E5, and G2 excluded by consensus) are addressed.

| Delphi Category | Items | Primary Architecture Realisation |
|----------------|-------|----------------------------------|
| A — System Functionality | A1-A6 | FastAPI routers: /estimate, /macro, /projects, /reports, /pipeline |
| B — Data and Integration | B1-B5 (B6 excl.) | 9 Airflow DAGs; 10 Supabase tables for macro/material/market data; `data_source_level` field |
| C — ML and AI Features | C1-C5 (C6 excl.) | MLflow champion/challenger; Stacking Ensemble; SHAP values in predictions table; v_champion_model view |
| D — Security and Privacy | D1-D6 | JWT Auth (Supabase GoTrue); RLS (36 policies); RBAC (3 roles); audit_log table; HTTPS/TLS |
| E — Usability and UX | E1-E4, E6 (E5 excl.) | Vanilla JS frontend; SHAP chart on results page; PDF report; freshness indicator; mobile-responsive CSS |
| F — Performance and Scalability | F1-F6 | FastAPI async; Railway horizontal scaling; Supabase connection pooling; rate limiting (10 req/min); /estimate < 3s target |
| G — Deployment and Operations | G1, G3-G6 (G2 excl.) | GitHub Actions CI/CD; Railway auto-deploy; Airflow monitoring; PSI drift detection; MLflow experiment history |

**Excluded items (by Delphi consensus):**
- B6 (mandate specific procurement method): excluded — outside ML/system scope.
- C6 (mandate stacking ensemble as sole method): excluded — benchmarking (O5) will determine champion model empirically.
- E5 (dedicated mobile app): excluded — mobile-responsive web is sufficient for prototype.
- G2 (dedicated on-premise deployment): excluded — cloud-native architecture adopted.

---

## 4.7 Design Limitations and Future Work

The conceptual design presented in this chapter has several acknowledged limitations:

**Synthetic data dependency**: As of the writing of this chapter, the EIA Brent crude
price and CBN exchange rate pipelines operate on synthetic data (RED level) pending
configuration of EIA_API_KEY and FRED_API_KEY. All ML results derived from the
O2 SHAP analysis use a synthetic housing cost proxy and must be re-estimated with
real NIQS unit rate data (O5). The `data_source_level` field ensures these
limitations are visible in all system outputs.

**Small training sample**: The current O2 analysis uses annual data (T=25 observations,
2000-2024). The O5 ML benchmarking phase will supplement this with project-level BQ
cost records and quarterly/monthly data to increase the training sample. The schema's
`predictions` table will accumulate real project cost data post-deployment, enabling
online learning in later research phases.

**Scraper fragility**: The PropertyPro, BusinessDay, and Jiji.ng scrapers are
susceptible to website structure changes. The pipeline design includes RED-level
fallback and admin alert mechanisms, but a data supply agreement with the relevant
platforms is recommended for production deployment.

**Scalability ceiling**: The current Railway/Supabase free-tier configuration is
appropriate for an academic prototype. A production deployment serving the Nigerian
QS industry would require Supabase Pro (connection pooling), Railway paid tiers
(guaranteed uptime SLA), and a CDN-cached model inference layer.

---

## 4.8 Chapter Summary

This chapter has presented the full conceptual design of the iNHCES system across four
formal artefact sets: a seven-layer cloud-native architecture with documented design
decision rationales, a normalised sixteen-table PostgreSQL schema with row-level
security and data provenance tracking, a two-level DFD process model specifying all
six system processes and three data stores, and an Airflow pipeline design with nine
DAGs governing data ingestion, ML retraining, and drift detection.

The design directly realises all 36 Delphi consensus requirements from Chapter 3 and
satisfies all 47 functional requirements in the SRS (Appendix B). The key innovation
of the conceptual design, beyond its technical completeness, is the systematic
integration of data quality tracking (the `data_source_level` field) across the entire
data layer — ensuring that the gap between the simulation prototype and a
publication-ready system is always visible, measurable, and actionable.

Chapter 5 proceeds to the ML model benchmarking phase, in which the feature
engineering pipeline, model training and evaluation framework, and SHAP-based
explainability analysis are implemented using the database schema and pipeline
architecture defined here.

---

## References

> All references are from AI training knowledge. Verify every citation in Scopus or
> Web of Science before inclusion in any submitted manuscript.

- Creswell, J.W. (2014). *Research design: qualitative, quantitative, and mixed methods
  approaches* (4th ed.). SAGE Publications. [VERIFY]
- Fielding, R.T. (2000). *Architectural styles and the design of network-based software
  architectures*. Doctoral dissertation, University of California, Irvine. [VERIFY]
- Fowler, M. (2002). *Patterns of enterprise application architecture*. Addison-Wesley.
  [VERIFY — high confidence]
- Kleppmann, M. (2017). *Designing data-intensive applications*. O'Reilly. [VERIFY]
- Lundberg, S.M., & Lee, S.I. (2017). A unified approach to interpreting model
  predictions. *NeurIPS*, 30. [VERIFY — high confidence]
- Page, M.J. et al. (2021). The PRISMA 2020 statement. *BMJ*, 372, n71. [VERIFY]
- PostgreSQL Global Development Group. (2024). *PostgreSQL 15 Documentation*.
  https://www.postgresql.org/docs/15/ [VERIFY URL]
- Supabase Inc. (2024). *Supabase Documentation*. https://supabase.com/docs [VERIFY]

---

*Document: 04_Chapter4_Conceptual_Models.md*
*Version: 1.0 — AI-Assisted First Draft*
*Generated: O4 Step 4 | DATA SOURCE: AMBER*
*TETFund NRF 2025 | Department of Quantity Surveying, ABU Zaria*
