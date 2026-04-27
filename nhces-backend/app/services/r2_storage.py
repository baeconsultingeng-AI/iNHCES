"""
iNHCES Cloudflare R2 Storage Service
S3-compatible object storage via boto3.

Provides:
  upload_bytes(data, key, content_type)  -- upload in-memory bytes
  download_bytes(key)                    -- download to memory
  generate_presigned_url(key, hours)     -- time-limited download URL
  delete_object(key)                     -- remove an object

Falls back gracefully when R2 credentials are not configured
(development mode — logs warning, returns None / empty bytes).
"""

import io
import logging
from typing import Optional

logger = logging.getLogger(__name__)


def _client():
    """Return a configured boto3 S3 client for Cloudflare R2."""
    from app.config import get_settings
    from botocore.config import Config
    import boto3

    s = get_settings()
    return boto3.client(
        "s3",
        endpoint_url=s.cloudflare_r2_endpoint,
        aws_access_key_id=s.cloudflare_r2_access_key,
        aws_secret_access_key=s.cloudflare_r2_secret_key,
        config=Config(signature_version="s3v4"),
    ), s.cloudflare_r2_bucket


def _is_configured() -> bool:
    from app.config import get_settings
    return get_settings().r2_configured


def upload_bytes(
    data: bytes,
    key: str,
    content_type: str = "application/octet-stream",
) -> bool:
    """
    Upload bytes to R2. Returns True on success, False on failure.
    In development (R2 not configured) logs a warning and returns False.
    """
    if not _is_configured():
        logger.warning(f"[r2] R2 not configured — skipping upload of {key}")
        return False
    try:
        client, bucket = _client()
        client.put_object(
            Bucket=bucket,
            Key=key,
            Body=data,
            ContentType=content_type,
        )
        logger.info(f"[r2] Uploaded {len(data):,} bytes -> {key}")
        return True
    except Exception as e:
        logger.error(f"[r2] upload_bytes failed for {key}: {e}")
        return False


def download_bytes(key: str) -> Optional[bytes]:
    """
    Download an object from R2 to memory.
    Returns bytes on success, None on failure or if R2 not configured.
    """
    if not _is_configured():
        logger.warning(f"[r2] R2 not configured — cannot download {key}")
        return None
    try:
        client, bucket = _client()
        buf = io.BytesIO()
        client.download_fileobj(bucket, key, buf)
        buf.seek(0)
        data = buf.read()
        logger.info(f"[r2] Downloaded {len(data):,} bytes from {key}")
        return data
    except Exception as e:
        logger.error(f"[r2] download_bytes failed for {key}: {e}")
        return None


def generate_presigned_url(key: str, expiry_hours: int = 24) -> Optional[str]:
    """
    Generate a time-limited presigned GET URL.
    Returns URL string on success, None if R2 not configured or error.
    """
    if not _is_configured():
        logger.warning(f"[r2] R2 not configured — returning dev URL for {key}")
        return f"http://localhost:8000/dev-download/{key}"
    try:
        client, bucket = _client()
        url = client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket, "Key": key},
            ExpiresIn=expiry_hours * 3600,
        )
        return url
    except Exception as e:
        logger.error(f"[r2] presign failed for {key}: {e}")
        return None


def delete_object(key: str) -> bool:
    """Delete an object from R2. Returns True on success."""
    if not _is_configured():
        return False
    try:
        client, bucket = _client()
        client.delete_object(Bucket=bucket, Key=key)
        logger.info(f"[r2] Deleted {key}")
        return True
    except Exception as e:
        logger.error(f"[r2] delete failed for {key}: {e}")
        return False
