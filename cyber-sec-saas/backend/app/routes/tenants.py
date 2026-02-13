from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..auth.dependencies import require_roles
from ..database import get_db
from ..models import Role, Tenant
from ..schemas import TenantCreate, TenantRead

router = APIRouter(prefix="/tenants", tags=["tenants"])


@router.post("", response_model=TenantRead, status_code=status.HTTP_201_CREATED)
def create_tenant(
    payload: TenantCreate,
    user=Depends(require_roles(Role.super_admin)),
    db: Session = Depends(get_db),
):
    existing = db.query(Tenant).filter(Tenant.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=409, detail="Tenant already exists")

    tenant = Tenant(name=payload.name)
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant


@router.get("", response_model=list[TenantRead])
def list_tenants(
    user=Depends(require_roles(Role.super_admin)),
    db: Session = Depends(get_db),
):
    return db.query(Tenant).order_by(Tenant.created_at.desc()).all()
