from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..auth.jwt import create_access_token, create_refresh_token, decode_token
from ..auth.password import hash_password, verify_password
from ..database import get_db
from ..models import Tenant, User
from ..schemas import LoginRequest, RefreshRequest, RegisterRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    if payload.role.value == "SuperAdmin":
        raise HTTPException(status_code=403, detail="Super admin registration is disabled")

    tenant = db.query(Tenant).filter(Tenant.id == payload.tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    existing = (
        db.query(User)
        .filter(User.email == payload.email, User.tenant_id == payload.tenant_id)
        .first()
    )
    if existing:
        raise HTTPException(status_code=409, detail="User already exists")

    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role=payload.role,
        tenant_id=payload.tenant_id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    access_token = create_access_token(str(user.id), user.tenant_id, user.role.value)
    refresh_token = create_refresh_token(str(user.id), user.tenant_id, user.role.value)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = (
        db.query(User)
        .filter(User.email == payload.email)
        .first()
    )
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(str(user.id), user.tenant_id, user.role.value)
    refresh_token = create_refresh_token(str(user.id), user.tenant_id, user.role.value)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=TokenResponse)
def refresh(payload: RefreshRequest):
    try:
        decoded = decode_token(payload.refresh_token)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    if decoded.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")

    access_token = create_access_token(decoded["sub"], decoded["tenant_id"], decoded["role"])
    refresh_token = create_refresh_token(decoded["sub"], decoded["tenant_id"], decoded["role"])
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)
