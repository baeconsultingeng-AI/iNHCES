import uuid
import logging
from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional

from app.auth import get_current_user, get_optional_user, CurrentUser
from app.database import get_db
from app.schemas.report import ReportRequest, ReportRead, ReportList

logger = logging.getLogger(__name__)
router = APIRouter()

URL_EXPIRY_HOURS = 24


def _presign(r2_key: str) -> tuple[str, datetime]:
    """
    Generate a presigned Cloudflare R2 download URL.
    Falls back gracefully when R2 is not configured.
    """
    from app.config import get_settings
    settings = get_settings()
    expires_at = datetime.now(timezone.utc) + timedelta(hours=URL_EXPIRY_HOURS)

    if not settings.r2_configured:
        # Development fallback — return a placeholder URL
        return f"http://localhost:8000/reports/download/{r2_key}", expires_at

    try:
        import boto3
        from botocore.config import Config
        s3 = boto3.client(
            "s3",
            endpoint_url=settings.cloudflare_r2_endpoint,
            aws_access_key_id=settings.cloudflare_r2_access_key,
            aws_secret_access_key=settings.cloudflare_r2_secret_key,
            config=Config(signature_version="s3v4"),
        )
        url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": settings.cloudflare_r2_bucket, "Key": r2_key},
            ExpiresIn=URL_EXPIRY_HOURS * 3600,
        )
        return url, expires_at
    except Exception as e:
        logger.warning(f"[reports] presign failed: {e}")
        return "", expires_at


def _row_to_read(row: dict, with_url: bool = False) -> ReportRead:
    url, expires = (None, None)
    if with_url and row.get("r2_key"):
        url, expires = _presign(row["r2_key"])

    return ReportRead(
        id=row["id"],
        project_id=row["project_id"],
        prediction_id=row.get("prediction_id"),
        r2_key=row.get("r2_key", ""),
        download_url=url,
        url_expires_at=expires,
        file_size_bytes=row.get("file_size_bytes"),
        page_count=row.get("page_count"),
        created_at=datetime.fromisoformat(row["created_at"].replace("Z", "+00:00")),
    )


@router.post("", response_model=ReportRead, status_code=status.HTTP_201_CREATED)
async def generate_report(
    body: ReportRequest,
    user: CurrentUser = Depends(get_current_user),
):
    """
    Generate a PDF cost report for a project+prediction pair.
    Uploads to Cloudflare R2 and returns a presigned download URL.
    """
    db = get_db()

    # Verify project ownership
    try:
        proj = db.table("projects").select("id,title,floor_area_sqm,building_type,location_state") \
            .eq("id", body.project_id).eq("user_id", user.user_id).single().execute()
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Project not found.")

    # Fetch prediction
    try:
        pred = db.table("predictions").select("*") \
            .eq("id", body.prediction_id).single().execute()
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Prediction not found.")

    # Generate PDF
    try:
        from app.services.report_generator import build_report_pdf
        pdf_bytes, page_count = build_report_pdf(proj.data, pred.data)
    except Exception as e:
        logger.error(f"[reports] PDF generation failed: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="PDF generation failed.")

    # Upload to R2
    report_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc)
    r2_key = f"reports/{user.user_id}/{body.project_id}/{now.strftime('%Y%m%d_%H%M%S')}_{report_id[:8]}.pdf"

    try:
        from app.services.r2_storage import upload_bytes
        upload_bytes(pdf_bytes, r2_key, content_type="application/pdf")
    except Exception as e:
        logger.warning(f"[reports] R2 upload failed (non-fatal): {e}")
        # Continue — save the record without a working URL

    # Persist to DB
    row = {
        "id":              report_id,
        "project_id":      body.project_id,
        "prediction_id":   body.prediction_id,
        "user_id":         user.user_id,
        "r2_key":          r2_key,
        "file_size_bytes": len(pdf_bytes),
        "page_count":      page_count,
        "created_at":      now.isoformat(),
    }
    try:
        resp = db.table("reports").insert(row).execute()
        saved = resp.data[0]
    except Exception as e:
        logger.warning(f"[reports] DB insert failed: {e}")
        saved = row

    return _row_to_read(saved, with_url=True)


@router.get("", response_model=ReportList)
async def list_reports(
    user: Optional[CurrentUser] = Depends(get_optional_user),
):
    """List all reports for the authenticated user. Returns empty list if not authenticated."""
    if user is None:
        return ReportList(items=[], total=0)

    db = get_db()
    try:
        resp = db.table("reports").select("*") \
            .eq("user_id", user.user_id) \
            .order("created_at", desc=True) \
            .limit(50) \
            .execute()
    except Exception as e:
        logger.error(f"[reports] list failed: {e}")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="Database error.")

    items = [_row_to_read(r, with_url=True) for r in resp.data]
    return ReportList(items=items, total=len(items))
