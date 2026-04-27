import uuid
import logging
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import Optional

from app.auth import get_current_user, get_optional_user, CurrentUser
from app.database import get_db
from app.schemas.project import (
    ProjectCreate, ProjectUpdate, ProjectRead, ProjectList
)

logger = logging.getLogger(__name__)
router = APIRouter()


def _row_to_read(row: dict) -> ProjectRead:
    return ProjectRead(
        id=row["id"],
        user_id=row["user_id"],
        title=row["title"],
        building_type=row["building_type"],
        construction_type=row["construction_type"],
        floor_area_sqm=float(row["floor_area_sqm"]),
        num_floors=int(row.get("num_floors", 1)),
        location_state=row["location_state"],
        location_zone=row["location_zone"],
        location_lga=row.get("location_lga"),
        target_cost_ngn=row.get("target_cost_ngn"),
        notes=row.get("notes"),
        status=row.get("status", "active"),
        created_at=datetime.fromisoformat(row["created_at"].replace("Z", "+00:00")),
        updated_at=datetime.fromisoformat(row["updated_at"].replace("Z", "+00:00")),
    )


@router.get("", response_model=ProjectList)
async def list_projects(
    page:  int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    user: Optional[CurrentUser] = Depends(get_optional_user),
):
    """List the authenticated user's projects. Returns empty list if not authenticated."""
    if user is None:
        return ProjectList(items=[], total=0, page=page, limit=limit)

    db = get_db()
    offset = (page - 1) * limit
    try:
        resp = (
            db.table("projects")
            .select("*", count="exact")
            .eq("user_id", user.user_id)
            .order("created_at", desc=True)
            .range(offset, offset + limit - 1)
            .execute()
        )
    except Exception as e:
        logger.error(f"[projects] list failed: {e}")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="Database error.")

    items = [_row_to_read(r) for r in resp.data]
    return ProjectList(items=items, total=resp.count or 0, page=page, limit=limit)


@router.get("/{project_id}", response_model=ProjectRead)
async def get_project(
    project_id: str,
    user: CurrentUser = Depends(get_current_user),
):
    db = get_db()
    try:
        resp = (
            db.table("projects")
            .select("*")
            .eq("id", project_id)
            .eq("user_id", user.user_id)
            .single()
            .execute()
        )
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Project not found.")
    return _row_to_read(resp.data)


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(
    body: ProjectCreate,
    user: CurrentUser = Depends(get_current_user),
):
    db = get_db()
    now = datetime.now(timezone.utc).isoformat()
    row = {
        "id":                str(uuid.uuid4()),
        "user_id":           user.user_id,
        "title":             body.title,
        "building_type":     body.building_type.value,
        "construction_type": body.construction_type.value,
        "floor_area_sqm":    body.floor_area_sqm,
        "num_floors":        body.num_floors,
        "location_state":    body.location_state,
        "location_zone":     body.location_zone.value,
        "location_lga":      body.location_lga,
        "target_cost_ngn":   body.target_cost_ngn,
        "notes":             body.notes,
        "status":            "active",
        "created_at":        now,
        "updated_at":        now,
    }
    try:
        resp = db.table("projects").insert(row).execute()
    except Exception as e:
        logger.error(f"[projects] create failed: {e}")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="Could not save project.")
    return _row_to_read(resp.data[0])


@router.put("/{project_id}", response_model=ProjectRead)
async def update_project(
    project_id: str,
    body: ProjectUpdate,
    user: CurrentUser = Depends(get_current_user),
):
    db = get_db()
    # Verify ownership
    try:
        db.table("projects").select("id").eq("id", project_id).eq("user_id", user.user_id).single().execute()
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Project not found.")

    updates = {k: v for k, v in body.model_dump(exclude_unset=True).items() if v is not None}
    updates["updated_at"] = datetime.now(timezone.utc).isoformat()

    try:
        resp = db.table("projects").update(updates).eq("id", project_id).execute()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="Could not update project.")
    return _row_to_read(resp.data[0])


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: str,
    user: CurrentUser = Depends(get_current_user),
):
    db = get_db()
    try:
        db.table("projects").delete().eq("id", project_id).eq("user_id", user.user_id).execute()
    except Exception as e:
        logger.error(f"[projects] delete failed: {e}")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="Could not delete project.")
