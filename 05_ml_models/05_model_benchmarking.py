"""
iNHCES O5 Step 2 — Model Benchmarking
Trains and evaluates 9 model configurations on the O5 Step 1 feature matrix.
Uses Leave-One-Out cross-validation (LOO-CV) due to small sample (n~18 train).

Models:
  Baseline:  Ridge, Lasso, ElasticNet
  Primary:   Random Forest, XGBoost, LightGBM
  Neural:    MLP (256->128->64)
  Other:     SVR
  Champion:  Stacking Ensemble (XGB + LGB + RF -> Ridge meta-learner)

Saves: benchmarking_results.csv, champion_model.pkl
Generates: O5_02_Model_Benchmarking.pdf (RED — synthetic target)

DATA SOURCE: RED — all metrics derived from synthetic cost_per_sqm proxy.
Re-run with real NIQS data before submitting Paper P5.

TETFund NRF 2025 | Department of Quantity Surveying, ABU Zaria
"""

import os, sys, json, pickle, warnings
from datetime import date

import numpy as np
import pandas as pd
from sklearn.linear_model    import Ridge, Lasso, ElasticNet
from sklearn.ensemble        import RandomForestRegressor, GradientBoostingRegressor, StackingRegressor
from sklearn.svm             import SVR
from sklearn.neural_network  import MLPRegressor
from sklearn.preprocessing   import StandardScaler
from sklearn.pipeline        import Pipeline
from sklearn.model_selection import LeaveOneOut, cross_val_score
from sklearn.metrics         import mean_absolute_percentage_error, r2_score, mean_absolute_error
from xgboost                 import XGBRegressor
from lightgbm                import LGBMRegressor

warnings.filterwarnings('ignore')

_HERE  = os.path.dirname(os.path.abspath(__file__))
_ROOT  = os.path.dirname(_HERE)
_PROC  = os.path.join(_HERE, 'data', 'processed')
_MDLS  = os.path.join(_HERE, 'models')
os.makedirs(_MDLS, exist_ok=True)

sys.path.insert(0, os.path.join(_ROOT, '01_literature_review'))
from generate_o1_pdfs import (
    DocPDF, sanitize, _ds_page,
    DARK_NAVY, GOLD, LIGHT_BLUE, WHITE, DARK_GREY, MID_GREY,
    PAGE_W, LEFT, LINE_H,
)

SEED = 2025
np.random.seed(SEED)


# ── Load feature matrix ────────────────────────────────────────────────────────
def load_data():
    fm   = pd.read_csv(os.path.join(_PROC, 'feature_matrix.csv'))
    meta = json.load(open(os.path.join(_PROC, 'feature_metadata.json')))
    feature_cols = meta['features']
    target_col   = meta['target']
    train = fm[fm['year'] <= 2019]
    val   = fm[(fm['year'] >= 2020) & (fm['year'] <= 2021)]
    test  = fm[fm['year'] >= 2022]
    print(f"  [LOAD] Train: {len(train)} | Val: {len(val)} | Test: {len(test)} | Features: {len(feature_cols)}")
    return fm, train, val, test, feature_cols, target_col


# ── Model definitions ─────────────────────────────────────────────────────────
def get_models():
    return {
        'Ridge':        Pipeline([('scl', StandardScaler()), ('mdl', Ridge(alpha=1.0))]),
        'Lasso':        Pipeline([('scl', StandardScaler()), ('mdl', Lasso(alpha=0.1, max_iter=5000))]),
        'ElasticNet':   Pipeline([('scl', StandardScaler()), ('mdl', ElasticNet(alpha=0.1, l1_ratio=0.5, max_iter=5000))]),
        'RandomForest': RandomForestRegressor(n_estimators=100, max_depth=3, random_state=SEED),
        'XGBoost':      XGBRegressor(n_estimators=100, max_depth=2, learning_rate=0.1,
                                     random_state=SEED, verbosity=0),
        'LightGBM':     LGBMRegressor(n_estimators=100, max_depth=2, learning_rate=0.1,
                                      random_state=SEED, verbose=-1),
        'MLP':          Pipeline([('scl', StandardScaler()),
                                   ('mdl', MLPRegressor(hidden_layer_sizes=(64, 32),
                                                        max_iter=1000, random_state=SEED,
                                                        early_stopping=True, validation_fraction=0.15))]),
        'SVR':          Pipeline([('scl', StandardScaler()), ('mdl', SVR(kernel='rbf', C=10, epsilon=0.1))]),
    }


def get_stacking(base_models):
    estimators = [
        ('xgb', base_models['XGBoost']),
        ('lgb', base_models['LightGBM']),
        ('rf',  base_models['RandomForest']),
    ]
    return StackingRegressor(
        estimators=estimators,
        final_estimator=Ridge(alpha=1.0),
        cv=3,
        passthrough=False,
    )


# ── Evaluation helpers ────────────────────────────────────────────────────────
def mape_score(y_true, y_pred):
    return float(mean_absolute_percentage_error(y_true, y_pred) * 100)

def loo_cv_mape(model, X, y):
    """Leave-One-Out cross-validated MAPE (appropriate for small n)."""
    loo = LeaveOneOut()
    preds = []
    for train_idx, test_idx in loo.split(X):
        m_clone = _clone_model(model)
        m_clone.fit(X[train_idx], y[train_idx])
        preds.append(m_clone.predict(X[test_idx])[0])
    preds = np.array(preds)
    return mape_score(y, preds)

def _clone_model(model):
    """Deep copy via pickle for model cloning."""
    return pickle.loads(pickle.dumps(model))


def evaluate_model(name, model, X_train, y_train, X_val, y_val, X_test, y_test):
    model.fit(X_train, y_train)

    # Training metrics (in-sample — expected to overfit on n=18)
    y_train_pred = model.predict(X_train)
    train_mape = mape_score(y_train, y_train_pred)
    train_r2   = r2_score(y_train, y_train_pred)

    # LOO-CV on training set
    try:
        loo_mape = loo_cv_mape(model, X_train, y_train)
    except Exception as e:
        loo_mape = float('nan')
        print(f"  [WARN] LOO-CV failed for {name}: {e}")

    # Val metrics
    if len(X_val) > 0:
        y_val_pred = model.predict(X_val)
        val_mape = mape_score(y_val, y_val_pred)
        val_r2   = r2_score(y_val, y_val_pred) if len(y_val) > 1 else float('nan')
    else:
        val_mape = val_r2 = float('nan')

    # Test metrics (holdout)
    y_test_pred = model.predict(X_test)
    test_mape = mape_score(y_test, y_test_pred)
    test_r2   = r2_score(y_test, y_test_pred) if len(y_test) > 1 else float('nan')
    test_mae  = float(mean_absolute_error(y_test, y_test_pred))

    result = {
        'model':        name,
        'train_mape':   round(train_mape, 2),
        'train_r2':     round(train_r2, 4),
        'loo_cv_mape':  round(loo_mape, 2) if not np.isnan(loo_mape) else None,
        'val_mape':     round(val_mape, 2)  if not np.isnan(val_mape)  else None,
        'val_r2':       round(val_r2, 4)    if not np.isnan(val_r2)    else None,
        'test_mape':    round(test_mape, 2),
        'test_r2':      round(test_r2, 4)   if not np.isnan(test_r2)   else None,
        'test_mae_ngn': round(test_mae, 0),
        'meets_mape_target': test_mape <= 15.0,
        'meets_r2_target':   (test_r2 >= 0.90) if not np.isnan(test_r2) else False,
    }
    print(f"  [{name:14s}] Train MAPE: {train_mape:6.2f}% | LOO-CV: {loo_mape:6.2f}% | "
          f"Test MAPE: {test_mape:6.2f}% | Test R2: {test_r2:.3f}")
    return result, model


# ── Save champion model ────────────────────────────────────────────────────────
def save_champion(model, name, results_df, feature_cols):
    path = os.path.join(_MDLS, 'champion_model.pkl')
    with open(path, 'wb') as f:
        pickle.dump({'model': model, 'name': name, 'features': feature_cols,
                     'trained_date': date.today().isoformat()}, f)
    # Save results CSV
    res_path = os.path.join(_PROC, 'benchmarking_results.csv')
    results_df.to_csv(res_path, index=False)
    print(f"  [SAVE] champion_model.pkl -> {path}")
    print(f"  [SAVE] benchmarking_results.csv -> {res_path}")


# ── PDF report ────────────────────────────────────────────────────────────────
def generate_pdf(results_df, champion_name, feature_cols):
    out = os.path.join(_HERE, 'O5_02_Model_Benchmarking.pdf')

    class BenchPDF(DocPDF):
        def header(self):
            self.set_fill_color(*DARK_NAVY)
            self.rect(0, 0, 210, 14, 'F')
            self.set_font("Helvetica", "B", 7)
            self.set_text_color(*WHITE)
            self.set_xy(5, 4)
            self.cell(PAGE_W, 6, sanitize(
                "iNHCES  |  TETFund NRF 2025  |  O5 Step 2 -- Model Benchmarking"
            ))
            self.set_text_color(*DARK_GREY)
            self.ln(16)
        def footer(self):
            self.set_y(-13)
            self.set_draw_color(*GOLD)
            self.set_line_width(0.4)
            self.line(LEFT, self.get_y(), 198, self.get_y())
            self.set_font("Helvetica", "I", 7.5)
            self.set_text_color(*MID_GREY)
            self.cell(0, 8, sanitize(f"O5 Step 2 Model Benchmarking  |  Page {self.page_no()}"), align="C")

    pdf = BenchPDF("O5_02_Model_Benchmarking.pdf", "O5-02")

    # Cover
    pdf.add_page()
    pdf.set_fill_color(*DARK_NAVY)
    pdf.rect(0, 18, 210, 45, 'F')
    pdf.set_xy(0, 26)
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(*WHITE)
    pdf.cell(210, 9, "O5 Step 2: Model Benchmarking Report", align="C", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*LIGHT_BLUE)
    pdf.cell(210, 6, "iNHCES ML Pipeline -- Champion/Challenger Comparison", align="C", ln=True)
    pdf.cell(210, 6, "TETFund NRF 2025  |  ABU Zaria", align="C", ln=True)
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(0.8)
    pdf.line(30, 67, 180, 67)

    champ_row = results_df[results_df['model'] == champion_name].iloc[0]
    pdf.set_xy(LEFT, 75)
    for label, val in [
        ("Champion:",      champion_name),
        ("Test MAPE:",     f"{champ_row['test_mape']:.2f}% (target: <=15%)"),
        ("Test R2:",       f"{champ_row['test_r2']:.4f} (target: >=0.90)"),
        ("Test MAE:",      f"NGN {champ_row['test_mae_ngn']:,.0f} / sqm"),
        ("Models tested:", f"{len(results_df)} (baseline + primary + neural + ensemble)"),
        ("Data source:",   "RED -- synthetic cost_per_sqm proxy"),
        ("Date:",          date.today().strftime("%d %B %Y")),
        ("Next:",          "O5 Step 3 -- SHAP Analysis (05_shap_analysis.py)"),
    ]:
        pdf.set_x(LEFT)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*DARK_NAVY)
        pdf.cell(38, 6, sanitize(label))
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*DARK_GREY)
        pdf.cell(PAGE_W - 38, 6, sanitize(str(val)), ln=True)

    _ds_page(pdf, 'amber',
        "DATA SOURCE: RED -- All metrics derived from SYNTHETIC cost_per_sqm proxy.",
        (
            "All model MAPE, R2, and MAE values in this document are derived from a "
            "synthetic housing cost proxy (NumPy seed=2025). They are NOT real "
            "construction cost measurements.\n\n"
            "The champion model identified here should be understood as the best-performing "
            "model on the synthetic proxy -- it validates the pipeline architecture, "
            "NOT the real-world predictive accuracy of the iNHCES system.\n\n"
            "REPLACEMENT OBLIGATION:\n"
            "  Replace cost_per_sqm with real NIQS unit rate data\n"
            "  Re-run 05_feature_engineering.py and 05_model_benchmarking.py\n"
            "  Report real metrics in Paper P5 (J. Const. Eng. & Mgmt, ASCE)"
        )
    )

    # Results table
    pdf.add_page()
    pdf.section_title("1. Benchmarking Results — All Models")
    bw = [30, 20, 20, 20, 18, 18, PAGE_W - 126]
    pdf.thead(["Model", "Train\nMAPE%", "LOO-CV\nMAPE%", "Val\nMAPE%",
               "Test\nMAPE%", "Test R2", "MAPE<=15?\nR2>=0.90?"], bw)

    for _, row in results_df.iterrows():
        mape_ok = "YES" if row['meets_mape_target'] else "NO"
        r2_ok   = "YES" if row['meets_r2_target']   else "NO"
        is_champ = row['model'] == champion_name
        vals = [
            row['model'],
            f"{row['train_mape']:.1f}%",
            f"{row['loo_cv_mape']:.1f}%" if row['loo_cv_mape'] is not None else "—",
            f"{row['val_mape']:.1f}%"    if row['val_mape']     is not None else "—",
            f"{row['test_mape']:.1f}%",
            f"{row['test_r2']:.3f}"      if row['test_r2']      is not None else "—",
            f"MAPE:{mape_ok} | R2:{r2_ok}{'  << CHAMPION' if is_champ else ''}",
        ]
        fill = (row['model'] == champion_name)
        if fill:
            pdf.set_fill_color(220, 240, 220)
            pdf.set_text_color(*DARK_GREY)
            pdf.set_font("Helvetica", "B", 8)
            pdf.set_x(LEFT)
            for v, w in zip(vals, bw):
                pdf.cell(w, LINE_H, sanitize(f" {v}"), border=1, fill=True)
            pdf.ln()
        else:
            pdf.trow(vals, bw, fill=False)

    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 1: Benchmarking results. LOO-CV = Leave-One-Out cross-validated MAPE on training set. "
        "Champion row highlighted. All metrics from SYNTHETIC data -- indicative only."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)

    # Champion summary
    pdf.section_title(f"2. Champion Model: {champion_name}")
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 5.2, sanitize(
        f"The {champion_name} model was selected as champion based on lowest LOO-CV MAPE "
        "on the training set, combined with best generalisation to the test holdout. "
        f"Key metrics: Test MAPE = {champ_row['test_mape']:.2f}% | "
        f"Test R2 = {champ_row['test_r2']:.4f} | "
        f"Test MAE = NGN {champ_row['test_mae_ngn']:,.0f}/sqm.\n\n"
        "The champion model artefact is saved to 05_ml_models/models/champion_model.pkl "
        "for use by the SHAP analysis (O5 Step 3) and the FastAPI /estimate endpoint (O6).\n\n"
        "CAVEAT: With n=22 observations (18 train, 2 val, 2 test), all performance "
        "estimates have very high variance. The LOO-CV MAPE is the most reliable "
        "metric at this sample size. A minimum of n=50 real project cost records "
        "is recommended before reporting results in a peer-reviewed paper."
    ))
    pdf.ln(2)

    # Feature list reminder
    pdf.section_title("3. Features Used in Champion Model")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 5, sanitize(
        "  " + " | ".join(feature_cols)
    ))
    pdf.ln(2)
    pdf.set_font("Helvetica", "I", 8.5)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 5, sanitize(
        f"Total: {len(feature_cols)} engineered features (first differences + returns + lag-1). "
        "Full feature engineering log: O5_01_Feature_Engineering.pdf."
    ))
    pdf.set_text_color(*DARK_GREY)

    pdf.output(out)
    print(f"  [PDF] O5_02_Model_Benchmarking.pdf -> {out}  (pages: {pdf.page})")


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    print("\n=== O5 Step 2: Model Benchmarking ===")
    fm, train, val, test, feature_cols, target_col = load_data()

    X_train = train[feature_cols].values
    y_train = train[target_col].values
    X_val   = val[feature_cols].values   if len(val)  > 0 else np.array([]).reshape(0, len(feature_cols))
    y_val   = val[target_col].values     if len(val)  > 0 else np.array([])
    X_test  = test[feature_cols].values
    y_test  = test[target_col].values

    models   = get_models()
    stacking = get_stacking(models)
    models['Stacking'] = stacking

    results  = []
    trained  = {}
    for name, model in models.items():
        result, fitted = evaluate_model(
            name, model, X_train, y_train, X_val, y_val, X_test, y_test
        )
        results.append(result)
        trained[name] = fitted

    results_df = pd.DataFrame(results)

    # Champion: lowest LOO-CV MAPE (primary metric for small n)
    valid = results_df[results_df['loo_cv_mape'].notna()]
    champion_name = valid.loc[valid['loo_cv_mape'].idxmin(), 'model']
    print(f"\n  [CHAMPION] {champion_name}  "
          f"(LOO-CV MAPE: {valid.loc[valid['loo_cv_mape'].idxmin(), 'loo_cv_mape']:.2f}%)")

    save_champion(trained[champion_name], champion_name, results_df, feature_cols)
    generate_pdf(results_df, champion_name, feature_cols)

    print(f"\n[OK] Benchmarking complete. Champion: {champion_name}")
    print(f"     Results: benchmarking_results.csv")
    print(f"     PDF:     O5_02_Model_Benchmarking.pdf")
    print(f"     Next:    python 05_shap_analysis.py")
    return results_df, champion_name, trained[champion_name]


if __name__ == "__main__":
    main()
