from pydantic import BaseModel, Field, UUID4
from typing import Optional
from datetime import datetime
from enum import Enum


class ProjectStatus(str, Enum):
    active    = "active"
    completed = "completed"
    archived  = "archived"


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


class ProjectCreate(BaseModel):
    title:             str            = Field(..., min_length=3, max_length=200)
    building_type:     BuildingType   = BuildingType.residential
    construction_type: ConstructionType = ConstructionType.new_build
    floor_area_sqm:    float          = Field(..., gt=0, le=100_000)
    num_floors:        int            = Field(1, ge=1, le=100)
    location_state:    str            = Field(..., min_length=2, max_length=60)
    location_zone:     NigeriaZone    = NigeriaZone.north_west
    location_lga:      Optional[str]  = None
    target_cost_ngn:   Optional[float] = Field(None, gt=0)
    notes:             Optional[str]  = None


class ProjectUpdate(BaseModel):
    title:           Optional[str]           = None
    status:          Optional[ProjectStatus] = None
    target_cost_ngn: Optional[float]         = Field(None, gt=0)
    notes:           Optional[str]           = None


class ProjectRead(BaseModel):
    id:                str
    user_id:           str
    title:             str
    building_type:     str
    construction_type: str
    floor_area_sqm:    float
    num_floors:        int
    location_state:    str
    location_zone:     str
    location_lga:      Optional[str] = None
    target_cost_ngn:   Optional[float] = None
    notes:             Optional[str] = None
    status:            str
    created_at:        datetime
    updated_at:        datetime


class ProjectList(BaseModel):
    items: list[ProjectRead]
    total: int
    page:  int
    limit: int
