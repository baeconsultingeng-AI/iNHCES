from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime


class ReportRequest(BaseModel):
    project_id:    str
    prediction_id: str


class ReportRead(BaseModel):
    id:              str
    project_id:      str
    prediction_id:   Optional[str] = None
    r2_key:          str
    download_url:    Optional[str] = None   # presigned — generated on request
    url_expires_at:  Optional[datetime] = None
    file_size_bytes: Optional[int] = None
    page_count:      Optional[int] = None
    created_at:      datetime


class ReportList(BaseModel):
    items: list[ReportRead]
    total: int
