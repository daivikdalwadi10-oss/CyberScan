import uuid
from typing import Optional

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.dependencies import get_current_user
from ..database import get_db
from ..models.enterprise_models import Incident, IncidentStatus, AlertSeverity, User

router = APIRouter(prefix="/api/internal", tags=["incidents"])


class IncidentStatusUpdate(BaseModel):
    status: str
    resolution_notes: Optional[str] = None


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


@router.get("/incidents")
async def list_incidents(
    limit: int = 20,
    severity: Optional[str] = None,
    status: Optional[str] = None,
    assigned_to: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    limit = max(1, min(limit, 100))
    severity_enum = _parse_enum(severity, AlertSeverity, "severity")
    status_enum = _parse_enum(status, IncidentStatus, "status")
    assigned_user = _parse_user_filter(assigned_to, current_user)

    stmt = select(Incident).order_by(desc(Incident.created_at)).limit(limit)

    if severity_enum:
        stmt = stmt.where(Incident.severity == severity_enum)
    if status_enum:
        stmt = stmt.where(Incident.status == status_enum)
    if assigned_user is not None:
        stmt = stmt.where(Incident.assigned_to == assigned_user)

    result = await db.execute(stmt)
    incidents = result.scalars().all()

    return [
        {
            "id": str(incident.id),
            "title": incident.title,
            "description": incident.description,
            "severity": incident.severity.value,
            "status": incident.status.value,
            "category": incident.category,
            "created_at": incident.created_at.isoformat() if incident.created_at is not None else None,
            "updated_at": incident.updated_at.isoformat() if incident.updated_at is not None else None,
            "assigned_to": str(incident.assigned_to) if incident.assigned_to is not None else None,
            "resolved_at": incident.resolved_at.isoformat() if incident.resolved_at is not None else None,
        }
        for incident in incidents
    ]


@router.post("/incidents/{incident_id}/status")
async def update_incident_status(
    incident_id: str,
    payload: IncidentStatusUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        incident_uuid = uuid.UUID(incident_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid incident id")

    new_status = _parse_enum(payload.status, IncidentStatus, "status")
    if not new_status:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Status is required")

    result = await db.execute(select(Incident).where(Incident.id == incident_uuid))
    incident = result.scalar_one_or_none()
    if not incident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")

    incident.status = new_status  # type: ignore[assignment]
    if payload.resolution_notes:
        incident.resolution_notes = payload.resolution_notes  # type: ignore[assignment]
    if new_status in {IncidentStatus.RESOLVED, IncidentStatus.CLOSED}:
        incident.resolved_at = datetime.utcnow()  # type: ignore[assignment]
    await db.commit()

    return {"id": str(incident.id), "status": incident.status.value}
