import time
import uuid
import logging
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, status

from app.database import get_db
from app.ml.inference import predict
from app.ml.feature_prep import build_feature_vector
from app.ml.explainer import compute_shap, get_shap_labels
from app.ml.temporal import generate_temporal_projections
from app.schemas.estimate import (
    EstimateRequest, EstimateResponse,
    ShapItem, ProjectionPoint,
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("", response_model=EstimateResponse, status_code=status.HTTP_200_OK)
async def create_estimate(body: EstimateRequest):
    """
    Run the iNHCES ML cost estimation model with temporal projections.

    Returns:
      - Current cost prediction (LightGBM champion)
      - Temporal projections at 1yr, 3yr, 5yr horizons
      - SHAP feature importance
      - Widening confidence bands across horizons
    """
    t_start = time.monotonic()
    db = get_db()

    # 1. Build feature vector
    try:
        X, freshness, snapshot = build_feature_vector(db)
    except Exception as e:
        logger.error(f"[estimate] feature_prep failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Feature preparation failed. Please try again shortly.",
        )

    # 2. ML inference
    result       = predict(X)
    cost_per_sqm = result["predicted_cost_per_sqm"]
    total_cost   = round(cost_per_sqm * body.floor_area_sqm, 2)

    # 3. SHAP explainability
    shap_dict  = compute_shap(X)
    shap_items = get_shap_labels(shap_dict)

    # 4. Temporal projections (current + 1yr + 3yr + 5yr)
    proj_raw, inflation_rate = generate_temporal_projections(
        current_cost_per_sqm=cost_per_sqm,
        floor_area_sqm=body.floor_area_sqm,
    )
    projections = [ProjectionPoint(**p) for p in proj_raw]

    # 5. Persist to Supabase (non-fatal)
    prediction_id = str(uuid.uuid4())
    now           = datetime.now(timezone.utc)
    elapsed_ms    = int((time.monotonic() - t_start) * 1000)

    prediction_row = {
        "id":                       prediction_id,
        "user_id":                  "anonymous",
        "model_version":            result["model_version"],
        "model_stage":              "Production",
        "predicted_cost_per_sqm":   cost_per_sqm,
        "total_predicted_cost_ngn": total_cost,
        "confidence_lower":         result["confidence_lower"],
        "confidence_upper":         result["confidence_upper"],
        "mape_at_prediction":       result["mape_at_prediction"],
        "feature_snapshot":         snapshot,
        "shap_values":              {k: v for k, v in shap_dict.items() if k != "computed"},
        "api_response_ms":          elapsed_ms,
    }
    if body.project_id:
        prediction_row["project_id"] = str(body.project_id)

    try:
        db.table("predictions").insert(prediction_row).execute()
    except Exception as e:
        logger.warning(f"[estimate] DB insert failed (non-fatal): {e}")

    # 6. Return full response
    return EstimateResponse(
        prediction_id=prediction_id,
        predicted_cost_per_sqm=cost_per_sqm,
        total_predicted_cost_ngn=total_cost,
        confidence_lower=result["confidence_lower"],
        confidence_upper=result["confidence_upper"],
        mape_at_prediction=result["mape_at_prediction"],
        model_name=result["model_name"],
        model_version=result["model_version"],
        data_freshness=freshness,
        feature_snapshot=snapshot,
        shap_top_features=[ShapItem(**s) for s in shap_items],
        projections=projections,
        annual_inflation_rate=inflation_rate,
        is_synthetic=result["is_synthetic"],
        api_response_ms=elapsed_ms,
        created_at=now,
    )
