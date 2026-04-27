from pydantic import BaseModel, Field, UUID4
from typing import Optional
from enum import Enum
from datetime import datetime


class BuildingType(str, Enum):
    residential   = "Residential"
    commercial    = "Commercial"
    industrial    = "Industrial"
    institutional = "Institutional"
    mixed_use     = "Mixed Use"


class ConstructionType(str, Enum):
    new_build  = "New Build"
    renovation = "Renovation"
    extension  = "Extension"
    fit_out    = "Fit-Out"


class NigeriaZone(str, Enum):
    north_central = "North Central"
    north_east    = "North East"
    north_west    = "North West"
    south_east    = "South East"
    south_south   = "South South"
    south_west    = "South West"


class EstimateRequest(BaseModel):
    building_type:     BuildingType     = BuildingType.residential
    construction_type: ConstructionType = ConstructionType.new_build
    floor_area_sqm:    float            = Field(..., gt=0, le=100_000,
                                                description="Gross floor area in square metres")
    num_floors:        int              = Field(1, ge=1, le=100)
    location_state:    str              = Field(..., min_length=2, max_length=60)
    location_zone:     NigeriaZone      = NigeriaZone.north_west
    project_id:        Optional[UUID4]  = Field(None,
                                                description="Attach prediction to an existing project")
    target_cost_ngn:   Optional[float]  = Field(None, gt=0,
                                                description="Client budget in NGN (optional)")

    model_config = {"json_schema_extra": {"example": {
        "building_type":     "Residential",
        "construction_type": "New Build",
        "floor_area_sqm":    120.0,
        "num_floors":        1,
        "location_state":    "Kaduna",
        "location_zone":     "North West",
    }}}


class ShapItem(BaseModel):
    feature: str
    label:   str
    value:   float


class ProjectionPoint(BaseModel):
    """A single horizon in the temporal cost projection."""
    horizon_key:       str     # current | short_term | medium_term | long_term
    horizon_label:     str     # "Current" | "Short-term (<1 yr)" | etc.
    years:             int     # 0, 1, 3, 5
    cost_per_sqm:      float   # NGN per sqm at this horizon
    total_cost_ngn:    float   # cost_per_sqm * floor_area_sqm
    confidence_lower:  float   # lower bound NGN/sqm
    confidence_upper:  float   # upper bound NGN/sqm
    total_lower_ngn:   float
    total_upper_ngn:   float
    uncertainty_pct:   float   # total uncertainty as % of point estimate
    is_projection:     bool    # False for current, True for future horizons


class EstimateResponse(BaseModel):
    prediction_id:            str
    predicted_cost_per_sqm:   float = Field(description="NGN per sqm — current")
    total_predicted_cost_ngn: float = Field(description="cost_per_sqm × floor_area_sqm")
    confidence_lower:         float = Field(description="Lower bound of prediction interval")
    confidence_upper:         float = Field(description="Upper bound of prediction interval")
    mape_at_prediction:       float = Field(description="Champion model MAPE at time of call (%)")
    model_name:               str
    model_version:            str
    data_freshness:           str   = Field(description="GREEN | AMBER | RED")
    feature_snapshot:         dict  = Field(description="14 feature values used for inference")
    shap_top_features:        list[ShapItem]
    projections:              list[ProjectionPoint] = Field(
                                  description="Cost projections at current, 1yr, 3yr, 5yr horizons"
                              )
    annual_inflation_rate:    float = Field(description="Assumed annual cost inflation rate (%)")
    is_synthetic:             bool  = Field(description="True if model or data uses synthetic fallback")
    api_response_ms:          Optional[int] = None
    created_at:               datetime
