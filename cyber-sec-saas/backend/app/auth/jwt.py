"""JWT token management for enterprise platform"""
from datetime import datetime, timedelta, timezone
from typing import List
import uuid
from jose import jwt, JWTError

from ..config import settings


def create_access_token(user_id: uuid.UUID, email: str, roles: List[str]) -> str:
    """Create JWT access token with user ID and roles"""
    expires = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expires_minutes)
    payload = {
        "sub": str(user_id),  # Convert UUID to string
        "email": email,
        "roles": roles,  # List of role names
        "exp": expires,
        "type": "access"
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def create_refresh_token(user_id: uuid.UUID, email: str) -> str:
    """Create JWT refresh token"""
    expires = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expires_days)
    payload = {
        "sub": str(user_id),  # Convert UUID to string
        "email": email,
        "exp": expires,
        "type": "refresh"
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def decode_token(token: str) -> dict:
    """Decode and validate JWT token"""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError as exc:
        raise ValueError("Invalid or expired token") from exc
