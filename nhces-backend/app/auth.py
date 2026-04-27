from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from typing import Optional
from app.config import get_settings

bearer          = HTTPBearer(auto_error=True)
bearer_optional = HTTPBearer(auto_error=False)   # returns None if no token


class CurrentUser:
    def __init__(self, user_id: str, email: str, role: str):
        self.user_id = user_id
        self.email = email
        self.role = role

    @property
    def is_admin(self) -> bool:
        return self.role == "admin"

    @property
    def is_researcher(self) -> bool:
        return self.role in ("researcher", "admin")


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
) -> CurrentUser:
    """
    Validates a Supabase GoTrue JWT token.
    Raises 401 if token is missing, expired, or invalid.
    """
    settings = get_settings()
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.supabase_jwt_secret,
            algorithms=["HS256"],
            options={"verify_aud": False},
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    email = payload.get("email", "")
    # Supabase stores custom claims under app_metadata or user_metadata
    role = (
        payload.get("app_metadata", {}).get("role")
        or payload.get("user_metadata", {}).get("role")
        or "qsprofessional"
    )

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing subject claim.",
        )

    return CurrentUser(user_id=user_id, email=email, role=role)


async def require_researcher(user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
    if not user.is_researcher:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Researcher or admin role required.",
        )
    return user


async def require_admin(user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin role required.",
        )
    return user


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_optional),
) -> Optional[CurrentUser]:
    """
    Returns the authenticated user if a valid JWT is provided,
    or None if no token is present. Does NOT raise 401.
    Used on endpoints that show empty results to unauthenticated users
    rather than an error.
    """
    if credentials is None:
        return None
    settings = get_settings()
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.supabase_jwt_secret,
            algorithms=["HS256"],
            options={"verify_aud": False},
        )
        user_id = payload.get("sub")
        if not user_id:
            return None
        email = payload.get("email", "")
        role = (
            payload.get("app_metadata", {}).get("role")
            or payload.get("user_metadata", {}).get("role")
            or "qsprofessional"
        )
        return CurrentUser(user_id=user_id, email=email, role=role)
    except JWTError:
        return None
