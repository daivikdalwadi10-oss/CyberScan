import uuid
from typing import Optional

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.dependencies import get_current_user
from ..database import get_db
from ..models.enterprise_models import Alert, AlertSeverity, AlertStatus, User

router = APIRouter(prefix="/api/internal", tags=["alerts"])


def _parse_enum(value: Optional[str], enum_type, label: str):
    if not value:
        return None
    try:
        return enum_type(value.lower())
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid {label}: {value}"
        )


def _parse_user_filter(value: Optional[str], current_user: User):
    if not value:
        return None
    if value == "me":
        return current_user.id
    try:
        return uuid.UUID(value)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid assigned_to value"
        )


@router.get("/alerts")
async def list_alerts(
    limit: int = 20,
    severity: Optional[str] = None,
    status: Optional[str] = None,
    assigned_to: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    limit = max(1, min(limit, 100))
    severity_enum = _parse_enum(severity, AlertSeverity, "severity")
    status_enum = _parse_enum(status, AlertStatus, "status")
    assigned_user = _parse_user_filter(assigned_to, current_user)

    stmt = select(Alert).order_by(desc(Alert.created_at)).limit(limit)

    if severity_enum:
        stmt = stmt.where(Alert.severity == severity_enum)
    if status_enum:
        stmt = stmt.where(Alert.status == status_enum)
    if assigned_user is not None:
        stmt = stmt.where(Alert.acknowledged_by == assigned_user)

    result = await db.execute(stmt)
    alerts = result.scalars().all()

    return [
        {
            "id": str(alert.id),
            "title": alert.title,
            "description": alert.description,
            "severity": alert.severity.value,
            "status": alert.status.value,
            "source": alert.source,
            "created_at": alert.created_at.isoformat() if alert.created_at is not None else None,
            "updated_at": alert.updated_at.isoformat() if alert.updated_at is not None else None,
            "acknowledged_by": str(alert.acknowledged_by) if alert.acknowledged_by is not None else None,
            "acknowledged_at": alert.acknowledged_at.isoformat() if alert.acknowledged_at is not None else None,
            "resolved_by": str(alert.resolved_by) if alert.resolved_by is not None else None,
            "resolved_at": alert.resolved_at.isoformat() if alert.resolved_at is not None else None,
        }
        for alert in alerts
    ]


@router.post("/alerts/{alert_id}/ack")
async def acknowledge_alert(
    alert_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        alert_uuid = uuid.UUID(alert_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid alert id")

    result = await db.execute(select(Alert).where(Alert.id == alert_uuid))
    alert = result.scalar_one_or_none()
    if not alert:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alert not found")

    alert.status = AlertStatus.ACKNOWLEDGED  # type: ignore[assignment]
    alert.acknowledged_by = current_user.id
    alert.acknowledged_at = datetime.utcnow()  # type: ignore[assignment]
    await db.commit()

    return {"id": str(alert.id), "status": alert.status.value}


@router.post("/alerts/{alert_id}/escalate")
async def escalate_alert(
    alert_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        alert_uuid = uuid.UUID(alert_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid alert id")

    result = await db.execute(select(Alert).where(Alert.id == alert_uuid))
    alert = result.scalar_one_or_none()
    if not alert:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alert not found")

    alert.status = AlertStatus.IN_PROGRESS  # type: ignore[assignment]
    alert.acknowledged_by = alert.acknowledged_by or current_user.id
    if alert.acknowledged_at is None:
        alert.acknowledged_at = datetime.utcnow()  # type: ignore[assignment]
    await db.commit()

    return {"id": str(alert.id), "status": alert.status.value}


@router.post("/alerts/{alert_id}/resolve")
async def resolve_alert(
    alert_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        alert_uuid = uuid.UUID(alert_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid alert id")

    result = await db.execute(select(Alert).where(Alert.id == alert_uuid))
    alert = result.scalar_one_or_none()
    if not alert:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alert not found")

    alert.status = AlertStatus.RESOLVED  # type: ignore[assignment]
    alert.resolved_by = current_user.id
    alert.resolved_at = datetime.utcnow()  # type: ignore[assignment]
    await db.commit()

    return {"id": str(alert.id), "status": alert.status.value}
