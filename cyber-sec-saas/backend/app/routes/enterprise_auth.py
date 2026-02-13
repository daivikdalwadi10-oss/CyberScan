"""
Enterprise Authentication Routes
Login, logout, refresh tokens, and profile management
"""
from typing import List
from uuid import UUID
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from pydantic import BaseModel, EmailStr

from ..database import get_db
from ..models.enterprise_models import User, Role, RoleType
from ..auth.jwt import create_access_token, create_refresh_token, decode_token
from ..auth.password import verify_password, hash_password
from ..auth.dependencies import get_current_user
from ..utils.audit import log_login, log_logout

router = APIRouter(prefix="/auth", tags=["authentication"])


# ============================================
# SCHEMAS
# ============================================

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: dict  # user info


class RefreshRequest(BaseModel):
    refresh_token: str


class UserProfileResponse(BaseModel):
    id: str
    email: str
    full_name: str | None
    roles: List[str]
    is_active: bool
    created_at: str


# ============================================
# ROUTES
# ============================================

@router.post("/login", response_model=LoginResponse)
async def login(
    payload: LoginRequest,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Authenticate user and return JWT tokens
    
    - Validates credentials
    - Checks account status
    - Creates audit log
    - Returns access + refresh tokens
    """
    # Find user by email
    result = await db.execute(
        select(User).options(selectinload(User.roles)).where(User.email == payload.email)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Verify password
    if not verify_password(payload.password, user.hashed_password):
        # Increment failed login attempts
        user.failed_login_attempts = int(user.failed_login_attempts or 0) + 1
        if int(user.failed_login_attempts) >= 5:
            user.is_locked = True
        await db.commit()
        
        # Log failed attempt
        await log_login(db, user, request, success=False)
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Check account status
    if not bool(user.is_active):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )
    
    if bool(user.is_locked):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is locked due to multiple failed login attempts"
        )
    
    # Reset failed attempts on successful login
    user.failed_login_attempts = 0
    user.last_login_at = datetime.utcnow()
    await db.commit()
    
    # Get user roles
    role_names = [r.role_type.value for r in user.roles]
    
    # Create tokens
    access_token = create_access_token(UUID(str(user.id)), str(user.email), role_names)
    refresh_token = create_refresh_token(UUID(str(user.id)), str(user.email))
    
    # Log successful login
    await log_login(db, user, request, success=True)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "email": user.email,
            "full_name": user.full_name,
            "roles": role_names
        }
    }


@router.post("/refresh", response_model=LoginResponse)
async def refresh_token(
    payload: RefreshRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Refresh access token using refresh token
    """
    try:
        decoded = decode_token(payload.refresh_token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    if decoded.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )
    
    # Get user
    import uuid
    user_id = uuid.UUID(decoded["sub"])
    result = await db.execute(
        select(User).options(selectinload(User.roles)).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    
    if not user or not bool(user.is_active) or bool(user.is_locked):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # Get roles
    role_names = [r.role_type.value for r in user.roles]
    
    # Create new tokens
    access_token = create_access_token(UUID(str(user.id)), str(user.email), role_names)
    new_refresh_token = create_refresh_token(UUID(str(user.id)), str(user.email))
    
    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "email": user.email,
            "full_name": user.full_name,
            "roles": role_names
        }
    }


@router.post("/logout")
async def logout(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Logout user (client should discard tokens)
    Creates audit log entry
    """
    await log_logout(db, current_user, request)
    
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserProfileResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Get current authenticated user's profile
    """
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "full_name": current_user.full_name,
        "roles": [r.role_type.value for r in current_user.roles],
        "is_active": current_user.is_active,
        "created_at": current_user.created_at.isoformat()
    }


@router.get("/roles")
async def get_available_roles(
    current_user: User = Depends(get_current_user)
):
    """
    Get list of user's roles with permissions
    """
    roles_data = []
    for role in current_user.roles:
        roles_data.append({
            "role_type": role.role_type.value,
            "display_name": role.display_name,
            "description": role.description,
            "permissions": role.permissions
        })
    
    return {"roles": roles_data}
