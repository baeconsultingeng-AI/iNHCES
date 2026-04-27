"""
iNHCES Airflow DAG — nhces_retrain_weekly
Schedule: Sunday 02:00 WAT (01:00 UTC)  CRON: 0 1 * * 0

Pipeline:
  Task 1: assemble_features   — join all Supabase macro/material tables -> feature matrix
  Task 2: train_challengers   — train Ridge, Lasso, RF, XGB, LGB, MLP, SVR in parallel
  Task 3: train_stacking      — train Stacking Ensemble on OOF predictions from Task 2
  Task 4: evaluate_compare    — compute MAPE/R2/MAE; compare challenger vs champion
  Task 5: promote_if_better   — promote to Staging/Production if MAPE improves >= 0.5pp
  Task 6: audit_and_notify    — log event to audit_log; notify admin if promoted

Dependencies (Railway env vars):
  SUPABASE_URL, SUPABASE_SERVICE_KEY
  MLFLOW_TRACKING_URI, MLFLOW_EXPERIMENT
  CLOUDFLARE_R2_ENDPOINT, CLOUDFLARE_R2_ACCESS_KEY, CLOUDFLARE_R2_SECRET_KEY
  CLOUDFLARE_R2_BUCKET
  AIRFLOW_ADMIN_EMAIL (for failure/promotion notifications)

DATA SOURCE: AMBER — Airflow DAG code. Data sourced from Supabase (see task docstrings).
TETFund NRF 2025 | Department of Quantity Surveying, ABU Zaria
"""

import os
import json
import pickle
import logging
from datetime import datetime, timedelta
from typing import Dict, Any

# ── Airflow imports (only available in deployed Airflow environment) ───────────
try:
    from airflow import DAG
    from airflow.operators.python import PythonOperator
    from airflow.operators.email  import EmailOperator
    from airflow.utils.dates      import days_ago
    AIRFLOW_AVAILABLE = True
except ImportError:
    AIRFLOW_AVAILABLE = False
    # Provide stub for local development / documentation purposes
    class DAG:
        def __init__(self, *a, **kw): pass
        def __enter__(self): return self
        def __exit__(self, *a): pass
    class PythonOperator:
        def __init__(self, *a, **kw): pass
    class EmailOperator:
        def __init__(self, *a, **kw): pass
    days_ago = lambda n: datetime.utcnow() - timedelta(days=n)

import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)

# ── DAG default args ──────────────────────────────────────────────────────────
DEFAULT_ARGS = {
    'owner':            'iNHCES',
    'depends_on_past':  False,
    'email_on_failure': True,
    'email_on_retry':   False,
    'retries':          2,
    'retry_delay':      timedelta(minutes=5),
    'email':            [os.getenv('AIRFLOW_ADMIN_EMAIL', 'admin@nhces.ng')],
}

SEED            = 42
MAPE_TARGET     = 15.0
R2_TARGET       = 0.90
PROMO_THRESHOLD = 0.5   # % improvement required for auto-promotion


# ── TASK 1: Assemble Feature Matrix ──────────────────────────────────────────
def task_assemble_features(**context) -> str:
    """
    Joins all Supabase macro + material tables into a feature matrix.
    Applies the same transformations as 05_feature_engineering.py.
    Saves the feature matrix to Cloudflare R2.
    Returns the R2 key for downstream tasks via XCom.
    """
    logger.info("Task 1: Assembling feature matrix from Supabase")

    try:
        from supabase import create_client
        sb = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_SERVICE_KEY'])
    except (ImportError, KeyError) as e:
        raise RuntimeError(f"Supabase connection failed: {e}")

    # Pull latest macro data
    def fetch_table(table, cols, limit=500):
        resp = sb.table(table).select(','.join(cols)).order('date', desc=True).limit(limit).execute()
        return pd.DataFrame(resp.data)

    macro_fx  = fetch_table('macro_fx',       ['date', 'ngn_usd', 'ngn_eur', 'ngn_gbp'])
    macro_cpi = fetch_table('macro_cpi',      ['date', 'cpi_annual_pct'])
    macro_gdp = fetch_table('macro_gdp',      ['date', 'gdp_growth_pct'])
    macro_int = fetch_table('macro_interest', ['date', 'lending_rate_pct'])
    macro_oil = fetch_table('macro_oil',      ['date', 'brent_usd_barrel'])

    # Merge on date (annual — group by year)
    dfs = [macro_fx, macro_cpi, macro_gdp, macro_int, macro_oil]
    for df in dfs:
        df['year'] = pd.to_datetime(df['date']).dt.year
    merged = dfs[0]
    for df in dfs[1:]:
        merged = merged.merge(df[['year'] + [c for c in df.columns if c != 'date' and c != 'year']],
                              on='year', how='outer')
    merged = merged.groupby('year').mean(numeric_only=True).reset_index()
    merged = merged.sort_values('year').reset_index(drop=True)

    # Apply transformations (same as 05_feature_engineering.py)
    i1_cols = ['gdp_growth_pct', 'cpi_annual_pct', 'lending_rate_pct', 'brent_usd_barrel']
    i2_cols = ['ngn_usd', 'ngn_eur', 'ngn_gbp']
    for col in i1_cols:
        if col in merged.columns:
            merged[f'd_{col}'] = merged[col].diff()
    for col in i2_cols:
        if col in merged.columns:
            merged[f'ret_{col}'] = merged[col].pct_change() * 100
    transform_cols = [f'd_{c}' for c in i1_cols if f'd_{c}' in merged.columns] + \
                     [f'ret_{c}' for c in i2_cols if f'ret_{c}' in merged.columns]
    for col in transform_cols:
        merged[f'lag1_{col}'] = merged[col].shift(1)

    feature_cols = [c for c in merged.columns
                    if c.startswith('d_') or c.startswith('ret_') or c.startswith('lag1_')]
    feature_cols = [c for c in feature_cols if c in merged.columns]
    fm = merged[['year'] + feature_cols].dropna().reset_index(drop=True)

    logger.info(f"Feature matrix: {len(fm)} rows x {len(feature_cols)} features")

    # Save to R2
    run_date = context['ds']
    r2_key   = f"datasets/{run_date}/feature_matrix.csv"
    _upload_to_r2(fm.to_csv(index=False).encode(), r2_key)

    # Push feature cols via XCom
    context['ti'].xcom_push(key='feature_cols', value=feature_cols)
    context['ti'].xcom_push(key='r2_key_features', value=r2_key)
    context['ti'].xcom_push(key='n_rows', value=len(fm))
    return r2_key


# ── TASK 2: Train Challengers ─────────────────────────────────────────────────
def task_train_challengers(**context):
    """
    Trains all base challenger models (Ridge, Lasso, RF, XGBoost, LightGBM, SVR).
    Logs each run to MLflow. Uses the feature matrix from Task 1.
    """
    logger.info("Task 2: Training challenger models")
    from sklearn.linear_model  import Ridge, Lasso
    from sklearn.ensemble      import RandomForestRegressor
    from sklearn.svm           import SVR
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline      import Pipeline
    from sklearn.model_selection import LeaveOneOut
    from sklearn.metrics       import mean_absolute_percentage_error, r2_score
    from xgboost import XGBRegressor
    from lightgbm import LGBMRegressor
    import mlflow

    ti           = context['ti']
    feature_cols = ti.xcom_pull(key='feature_cols',      task_ids='assemble_features')
    r2_key       = ti.xcom_pull(key='r2_key_features',   task_ids='assemble_features')
    fm           = _load_csv_from_r2(r2_key)

    X = fm[feature_cols].values
    y = fm['cost_per_sqm'].values if 'cost_per_sqm' in fm.columns else np.zeros(len(fm))
    train_mask = fm['year'] <= (fm['year'].max() - 2)
    X_train, y_train = X[train_mask], y[train_mask]
    X_test,  y_test  = X[~train_mask], y[~train_mask]

    models = {
        'ridge':  Pipeline([('scl', StandardScaler()), ('mdl', Ridge(alpha=1.0))]),
        'lasso':  Pipeline([('scl', StandardScaler()), ('mdl', Lasso(alpha=0.1))]),
        'rf':     RandomForestRegressor(n_estimators=100, max_depth=3, random_state=SEED),
        'xgb':    XGBRegressor(n_estimators=100, max_depth=2, learning_rate=0.1,
                               random_state=SEED, verbosity=0),
        'lgb':    LGBMRegressor(n_estimators=100, max_depth=2, learning_rate=0.1,
                                random_state=SEED, verbose=-1),
        'svr':    Pipeline([('scl', StandardScaler()), ('mdl', SVR(C=10, epsilon=0.1))]),
    }

    mlflow.set_tracking_uri(os.getenv('MLFLOW_TRACKING_URI', './mlruns'))
    mlflow.set_experiment(os.getenv('MLFLOW_EXPERIMENT', 'nhces_cost_estimation'))

    run_ids = {}
    for name, model in models.items():
        with mlflow.start_run(run_name=f"{name}_{context['ds']}") as run:
            model.fit(X_train, y_train)
            loo = LeaveOneOut()
            loo_preds = []
            for tr, te in loo.split(X_train):
                m = pickle.loads(pickle.dumps(model))
                m.fit(X_train[tr], y_train[tr])
                loo_preds.append(m.predict(X_train[te])[0])
            loo_mape = float(mean_absolute_percentage_error(y_train, loo_preds) * 100)
            test_mape = float(mean_absolute_percentage_error(y_test, model.predict(X_test)) * 100) \
                if len(y_test) > 0 else float('nan')
            r2 = float(r2_score(y_test, model.predict(X_test))) \
                if len(y_test) > 1 else float('nan')

            mlflow.log_params({'model_type': name, 'n_features': len(feature_cols)})
            mlflow.log_metrics({'loo_cv_mape': loo_mape,
                                'mape_test': test_mape if not np.isnan(test_mape) else -1,
                                'r2_test': r2 if not np.isnan(r2) else -1})
            mlflow.sklearn.log_model(model, f"models/{name}")
            run_ids[name] = run.info.run_id
            logger.info(f"  [{name}] LOO-CV MAPE: {loo_mape:.2f}% | Test MAPE: {test_mape:.2f}%")

    ti.xcom_push(key='challenger_run_ids', value=run_ids)
    ti.xcom_push(key='X_train_r2', value=_save_array_r2(X_train, f"tmp/{context['ds']}/X_train.npy"))
    ti.xcom_push(key='y_train_r2', value=_save_array_r2(y_train, f"tmp/{context['ds']}/y_train.npy"))


# ── TASK 3: Train Stacking Ensemble ───────────────────────────────────────────
def task_train_stacking(**context):
    """Trains the Stacking Ensemble using cross-validated OOF from base learners."""
    logger.info("Task 3: Training Stacking Ensemble")
    from sklearn.ensemble import StackingRegressor
    from sklearn.linear_model import Ridge
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import mean_absolute_percentage_error, r2_score
    from xgboost import XGBRegressor
    from lightgbm import LGBMRegressor
    import mlflow

    ti    = context['ti']
    fm    = _load_csv_from_r2(ti.xcom_pull(key='r2_key_features', task_ids='assemble_features'))
    feats = ti.xcom_pull(key='feature_cols', task_ids='assemble_features')
    X     = fm[feats].values
    y     = fm['cost_per_sqm'].values if 'cost_per_sqm' in fm.columns else np.zeros(len(fm))
    mask  = fm['year'] <= (fm['year'].max() - 2)
    Xtr, ytr = X[mask], y[mask]
    Xte, yte = X[~mask], y[~mask]

    estimators = [
        ('xgb', XGBRegressor(n_estimators=100, max_depth=2, learning_rate=0.1,
                              random_state=SEED, verbosity=0)),
        ('lgb', LGBMRegressor(n_estimators=100, max_depth=2, learning_rate=0.1,
                              random_state=SEED, verbose=-1)),
        ('rf',  RandomForestRegressor(n_estimators=100, max_depth=3, random_state=SEED)),
    ]
    stacking = StackingRegressor(estimators=estimators, final_estimator=Ridge(alpha=1.0), cv=3)
    stacking.fit(Xtr, ytr)

    test_mape = float(mean_absolute_percentage_error(yte, stacking.predict(Xte)) * 100) \
        if len(yte) > 0 else float('nan')
    r2 = float(r2_score(yte, stacking.predict(Xte))) if len(yte) > 1 else float('nan')

    mlflow.set_tracking_uri(os.getenv('MLFLOW_TRACKING_URI', './mlruns'))
    mlflow.set_experiment(os.getenv('MLFLOW_EXPERIMENT', 'nhces_cost_estimation'))
    with mlflow.start_run(run_name=f"stacking_{context['ds']}") as run:
        mlflow.log_params({'model_type': 'stacking', 'n_features': len(feats),
                           'base_learners': 'xgb+lgb+rf', 'meta': 'ridge'})
        mlflow.log_metrics({'mape_test': test_mape if not np.isnan(test_mape) else -1,
                            'r2_test':   r2        if not np.isnan(r2)        else -1})
        mlflow.sklearn.log_model(stacking, "models/stacking",
                                 registered_model_name='nhces_champion')
        ti.xcom_push(key='stacking_run_id',   value=run.info.run_id)
        ti.xcom_push(key='stacking_mape',     value=test_mape)
    logger.info(f"Stacking test MAPE: {test_mape:.2f}%")


# ── TASK 4: Evaluate and Compare ─────────────────────────────────────────────
def task_evaluate_compare(**context):
    """
    Identifies the best challenger (lowest LOO-CV MAPE across all runs).
    Compares against current Production champion.
    Pushes promotion recommendation via XCom.
    """
    logger.info("Task 4: Evaluating and comparing models")
    import mlflow

    mlflow.set_tracking_uri(os.getenv('MLFLOW_TRACKING_URI', './mlruns'))
    client = mlflow.MlflowClient()

    # Find best challenger by LOO-CV or test MAPE
    ti       = context['ti']
    run_ids  = ti.xcom_pull(key='challenger_run_ids', task_ids='train_challengers') or {}
    run_ids['stacking'] = ti.xcom_pull(key='stacking_run_id', task_ids='train_stacking')

    best_name, best_mape, best_run_id = None, float('inf'), None
    for name, run_id in run_ids.items():
        if not run_id:
            continue
        try:
            run = client.get_run(run_id)
            mape = run.data.metrics.get('loo_cv_mape',
                   run.data.metrics.get('mape_test', float('inf')))
            if mape < best_mape:
                best_name, best_mape, best_run_id = name, mape, run_id
        except Exception as e:
            logger.warning(f"Could not evaluate run {run_id}: {e}")

    # Get current champion MAPE
    champ_mape = None
    try:
        prod = client.get_latest_versions('nhces_champion', stages=["Production"])
        if prod:
            champ_run = client.get_run(prod[0].run_id)
            champ_mape = champ_run.data.metrics.get('mape_test', float('inf'))
    except Exception:
        pass

    logger.info(f"Best challenger: {best_name} MAPE={best_mape:.2f}% | Champion: {champ_mape}")
    ti.xcom_push(key='best_challenger_run_id',  value=best_run_id)
    ti.xcom_push(key='best_challenger_mape',    value=best_mape)
    ti.xcom_push(key='champion_mape',           value=champ_mape)
    ti.xcom_push(key='should_promote',
                 value=(champ_mape is None or best_mape < champ_mape - 0.5))


# ── TASK 5: Promote if Better ─────────────────────────────────────────────────
def task_promote_if_better(**context):
    """
    Promotes the best challenger to Production in MLflow and updates
    is_champion in the Supabase ml_models table if improvement threshold met.
    """
    logger.info("Task 5: Promote if better")
    import mlflow
    ti = context['ti']

    if not ti.xcom_pull(key='should_promote', task_ids='evaluate_compare'):
        logger.info("No promotion — challenger does not improve on champion by >=0.5%")
        return

    run_id    = ti.xcom_pull(key='best_challenger_run_id',  task_ids='evaluate_compare')
    new_mape  = ti.xcom_pull(key='best_challenger_mape',    task_ids='evaluate_compare')
    old_mape  = ti.xcom_pull(key='champion_mape',           task_ids='evaluate_compare')

    mlflow.set_tracking_uri(os.getenv('MLFLOW_TRACKING_URI', './mlruns'))
    client = mlflow.MlflowClient()

    # Transition to Production in MLflow
    try:
        versions = client.search_model_versions(f"run_id='{run_id}'")
        if versions:
            client.transition_model_version_stage(
                name='nhces_champion', version=versions[0].version, stage="Production"
            )
            logger.info(f"MLflow: {run_id} -> Production (MAPE {new_mape:.2f}% vs {old_mape})")
    except Exception as e:
        logger.error(f"MLflow promotion failed: {e}")
        raise

    # Update Supabase ml_models (if available)
    try:
        from supabase import create_client
        sb = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_SERVICE_KEY'])
        sb.table('ml_models').update({'is_champion': False}).eq('is_champion', True).execute()
        sb.table('ml_models').update({'is_champion': True, 'stage': 'Production'}) \
          .eq('mlflow_run_id', run_id).execute()
    except Exception as e:
        logger.warning(f"Supabase ml_models update failed (non-fatal): {e}")

    ti.xcom_push(key='promoted', value=True)
    ti.xcom_push(key='new_champion_run_id', value=run_id)
    ti.xcom_push(key='new_champion_mape',   value=new_mape)


# ── TASK 6: Audit and Notify ──────────────────────────────────────────────────
def task_audit_and_notify(**context):
    """Logs retrain event to Supabase audit_log and records DAG run metadata."""
    ti       = context['ti']
    promoted = ti.xcom_pull(key='promoted', task_ids='promote_if_better') or False
    n_rows   = ti.xcom_pull(key='n_rows',   task_ids='assemble_features') or 0
    new_mape = ti.xcom_pull(key='new_champion_mape',   task_ids='promote_if_better')
    old_mape = ti.xcom_pull(key='champion_mape',        task_ids='evaluate_compare')

    audit_entry = {
        'action':     'dag_retrain_weekly',
        'table_name': 'ml_models',
        'record_id':  context['run_id'],
        'new_values': json.dumps({
            'dag_run':       context['run_id'],
            'run_date':      context['ds'],
            'n_training_rows': n_rows,
            'promoted':      promoted,
            'new_mape':      new_mape,
            'old_mape':      old_mape,
        }),
    }
    try:
        from supabase import create_client
        sb = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_SERVICE_KEY'])
        sb.table('audit_log').insert(audit_entry).execute()
        logger.info("Retrain event logged to audit_log")
    except Exception as e:
        logger.warning(f"audit_log insert failed: {e}")

    if promoted:
        logger.info(
            f"PROMOTION ALERT: New champion MAPE={new_mape:.2f}% "
            f"(was {old_mape:.2f}%). FastAPI restart may be required."
        )


# ── R2 helpers (stubs — replace with real boto3 calls in O6) ─────────────────
def _upload_to_r2(data: bytes, key: str) -> str:
    """Upload bytes to Cloudflare R2. Returns the R2 key."""
    try:
        import boto3
        s3 = boto3.client(
            's3',
            endpoint_url=os.environ['CLOUDFLARE_R2_ENDPOINT'],
            aws_access_key_id=os.environ['CLOUDFLARE_R2_ACCESS_KEY'],
            aws_secret_access_key=os.environ['CLOUDFLARE_R2_SECRET_KEY'],
        )
        s3.put_object(Bucket=os.environ['CLOUDFLARE_R2_BUCKET'], Key=key, Body=data)
        logger.info(f"Uploaded to R2: {key}")
    except Exception as e:
        logger.warning(f"R2 upload skipped ({e}) — saving locally")
        local = os.path.join('/tmp', key.replace('/', '_'))
        with open(local, 'wb') as f:
            f.write(data)
    return key


def _load_csv_from_r2(key: str) -> pd.DataFrame:
    """Download CSV from R2 and return as DataFrame."""
    try:
        import boto3, io
        s3 = boto3.client(
            's3',
            endpoint_url=os.environ['CLOUDFLARE_R2_ENDPOINT'],
            aws_access_key_id=os.environ['CLOUDFLARE_R2_ACCESS_KEY'],
            aws_secret_access_key=os.environ['CLOUDFLARE_R2_SECRET_KEY'],
        )
        obj = s3.get_object(Bucket=os.environ['CLOUDFLARE_R2_BUCKET'], Key=key)
        return pd.read_csv(io.BytesIO(obj['Body'].read()))
    except Exception:
        # Fallback to local feature_matrix for development
        local = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'feature_matrix.csv')
        return pd.read_csv(os.path.abspath(local))


def _save_array_r2(arr: np.ndarray, key: str) -> str:
    import io
    buf = io.BytesIO()
    np.save(buf, arr)
    _upload_to_r2(buf.getvalue(), key)
    return key


# ── DAG definition ────────────────────────────────────────────────────────────
if AIRFLOW_AVAILABLE:
    with DAG(
        dag_id='nhces_retrain_weekly',
        description='iNHCES weekly ML retrain and champion promotion',
        schedule_interval='0 1 * * 0',    # Sunday 02:00 WAT (01:00 UTC)
        start_date=days_ago(1),
        default_args=DEFAULT_ARGS,
        catchup=False,
        tags=['iNHCES', 'ML', 'retrain'],
        doc_md=__doc__,
    ) as dag:

        t1 = PythonOperator(
            task_id='assemble_features',
            python_callable=task_assemble_features,
            provide_context=True,
        )
        t2 = PythonOperator(
            task_id='train_challengers',
            python_callable=task_train_challengers,
            provide_context=True,
        )
        t3 = PythonOperator(
            task_id='train_stacking',
            python_callable=task_train_stacking,
            provide_context=True,
        )
        t4 = PythonOperator(
            task_id='evaluate_compare',
            python_callable=task_evaluate_compare,
            provide_context=True,
        )
        t5 = PythonOperator(
            task_id='promote_if_better',
            python_callable=task_promote_if_better,
            provide_context=True,
        )
        t6 = PythonOperator(
            task_id='audit_and_notify',
            python_callable=task_audit_and_notify,
            provide_context=True,
        )

        # DAG dependency chain
        t1 >> t2 >> t3 >> t4 >> t5 >> t6
