from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.dependencies import get_current_user
from ..database import get_db
from ..models.enterprise_models import (
    Alert,
    AlertSeverity,
    AuditLog,
    CloudStatusRecord,
    SystemMetric,
    ThreatIntelRecord,
    UptimeRecord,
    User,
)

router = APIRouter(prefix="/api/internal", tags=["operations"])


def _parse_severity(value: Optional[str]):
    if not value:
        return None
    return AlertSeverity(value.lower())


@router.get("/system-health")
async def get_system_health(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    window_1h = datetime.now(timezone.utc) - timedelta(hours=1)
    metrics_result = await db.execute(
        select(
            func.avg(SystemMetric.cpu_percent),
            func.avg(SystemMetric.memory_percent),
            func.avg(SystemMetric.disk_percent),
            func.avg(SystemMetric.load_average),
        ).where(SystemMetric.collected_at >= window_1h)
    )
    avg_cpu, avg_memory, avg_disk, avg_load = metrics_result.one()

    uptime_since = datetime.now(timezone.utc) - timedelta(days=1)
    uptime_result = await db.execute(
        select(func.count()).select_from(UptimeRecord).where(UptimeRecord.checked_at >= uptime_since)
    )
    uptime_total = uptime_result.scalar_one() or 0

    up_result = await db.execute(
        select(func.count()).select_from(UptimeRecord).where(
            UptimeRecord.checked_at >= uptime_since,
            UptimeRecord.is_up.is_(True)
        )
    )
    up_count = up_result.scalar_one() or 0
    uptime_percent = round((up_count / uptime_total) * 100, 2) if uptime_total else None

    cloud_since = datetime.now(timezone.utc) - timedelta(hours=6)
    cloud_result = await db.execute(
        select(func.count()).select_from(CloudStatusRecord).where(
            CloudStatusRecord.checked_at >= cloud_since,
            CloudStatusRecord.status != "operational"
        )
    )
    cloud_issues = cloud_result.scalar_one() or 0

    return {
        "cpu": avg_cpu,
        "memory": avg_memory,
        "disk": avg_disk,
        "loadAverage": avg_load,
        "uptimePercent": uptime_percent,
        "cloudIssues": cloud_issues,
        "lastChecked": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/audit-logs")
async def get_audit_logs(
    limit: int = 50,
    action: Optional[str] = None,
    resource_type: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    limit = max(1, min(limit, 200))
    stmt = select(AuditLog).order_by(desc(AuditLog.timestamp)).limit(limit)

    if action:
        stmt = stmt.where(AuditLog.action == action)
    if resource_type:
        stmt = stmt.where(AuditLog.resource_type == resource_type)

    result = await db.execute(stmt)
    logs = result.scalars().all()

    return [
        {
            "id": str(log.id),
            "action": log.action,
            "resource_type": log.resource_type,
            "resource_id": log.resource_id,
            "user_id": str(log.user_id) if log.user_id is not None else None,
            "success": bool(log.success),
            "timestamp": log.timestamp.isoformat() if log.timestamp is not None else None,
            "details": log.details,
        }
        for log in logs
    ]


@router.get("/threat-intel")
async def get_threat_intel(
    limit: int = 20,
    severity: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    limit = max(1, min(limit, 100))
    severity_enum = _parse_severity(severity)

    stmt = select(ThreatIntelRecord).order_by(desc(ThreatIntelRecord.published_date)).limit(limit)
    if severity_enum:
        stmt = stmt.where(ThreatIntelRecord.severity == severity_enum)

    result = await db.execute(stmt)
    records = result.scalars().all()

    return [
        {
            "id": str(record.id),
            "cve_id": record.cve_id,
            "title": record.title,
            "severity": record.severity.value,
            "cvss_score": record.cvss_score,
            "published_date": record.published_date.isoformat() if record.published_date is not None else None,
        }
        for record in records
    ]


@router.get("/iocs")
async def get_iocs(
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    limit = max(1, min(limit, 100))
    stmt = (
        select(Alert)
        .where(Alert.source == "ioc")
        .order_by(desc(Alert.created_at))
        .limit(limit)
    )
    result = await db.execute(stmt)
    alerts = result.scalars().all()

    return [
        {
            "id": str(alert.id),
            "title": alert.title,
            "severity": alert.severity.value,
            "status": alert.status.value,
            "source": alert.source,
            "created_at": alert.created_at.isoformat() if alert.created_at is not None else None,
        }
        for alert in alerts
    ]
