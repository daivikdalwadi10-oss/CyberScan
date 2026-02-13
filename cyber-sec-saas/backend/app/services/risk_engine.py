from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.enterprise_models import (
    Alert,
    AlertSeverity,
    AlertStatus,
    CloudStatusRecord,
    RiskScore,
    SystemMetric,
    ThreatIntelRecord,
    ThreatLevel,
    UptimeRecord,
)


async def recalculate_risk_score(db: AsyncSession) -> RiskScore:
    now = datetime.now(timezone.utc)
    window_30d = now - timedelta(days=30)
    window_24h = now - timedelta(hours=24)
    window_1h = now - timedelta(hours=1)

    critical_cve_result = await db.execute(
        select(func.count()).select_from(ThreatIntelRecord).where(
            ThreatIntelRecord.severity == AlertSeverity.CRITICAL,
            or_(
                ThreatIntelRecord.published_date.is_(None),
                ThreatIntelRecord.published_date >= window_30d,
            ),
        )
    )
    critical_cve_count = critical_cve_result.scalar_one() or 0

    active_alerts_result = await db.execute(
        select(func.count()).select_from(Alert).where(
            Alert.status.in_(
                [AlertStatus.NEW, AlertStatus.ACKNOWLEDGED, AlertStatus.IN_PROGRESS]
            )
        )
    )
    active_alert_count = active_alerts_result.scalar_one() or 0

    cloud_incident_result = await db.execute(
        select(func.count()).select_from(CloudStatusRecord).where(
            CloudStatusRecord.checked_at >= window_24h,
            CloudStatusRecord.status.in_(
                ["degraded", "outage", "partial_outage", "major_outage"]
            ),
        )
    )
    cloud_incident_count = cloud_incident_result.scalar_one() or 0

    metrics_result = await db.execute(
        select(
            func.avg(SystemMetric.cpu_percent),
            func.avg(SystemMetric.memory_percent),
            func.avg(SystemMetric.disk_percent),
        ).where(SystemMetric.collected_at >= window_1h)
    )
    avg_cpu, avg_memory, avg_disk = metrics_result.one()
    samples = [value for value in [avg_cpu, avg_memory, avg_disk] if value is not None]
    infra_score = sum(samples) / len(samples) if samples else 0.0

    uptime_total_result = await db.execute(
        select(func.count()).select_from(UptimeRecord).where(
            UptimeRecord.checked_at >= window_24h
        )
    )
    uptime_total = uptime_total_result.scalar_one() or 0
    uptime_up_result = await db.execute(
        select(func.count()).select_from(UptimeRecord).where(
            UptimeRecord.checked_at >= window_24h,
            UptimeRecord.is_up.is_(True),
        )
    )
    uptime_up = uptime_up_result.scalar_one() or 0
    uptime_percentage = (uptime_up / uptime_total) * 100 if uptime_total else 99.98

    threat_index = min(100.0, (critical_cve_count * 6) + (active_alert_count * 3) + (cloud_incident_count * 4))
    uptime_penalty = max(0.0, 100.0 - uptime_percentage)
    overall_score = min(100.0, (0.55 * threat_index) + (0.25 * infra_score) + (0.2 * uptime_penalty))

    if overall_score >= 85:
        threat_level = ThreatLevel.CRITICAL
    elif overall_score >= 70:
        threat_level = ThreatLevel.HIGH
    elif overall_score >= 50:
        threat_level = ThreatLevel.MODERATE
    elif overall_score >= 30:
        threat_level = ThreatLevel.LOW
    else:
        threat_level = ThreatLevel.MINIMAL

    risk_score = RiskScore(
        overall_score=overall_score,
        threat_level=threat_level,
        critical_cve_count=critical_cve_count,
        active_alert_count=active_alert_count,
        cloud_incident_count=cloud_incident_count,
        infrastructure_load_avg=infra_score,
        uptime_percentage=uptime_percentage,
        calculation_data={
            "threat_index": threat_index,
            "uptime_penalty": uptime_penalty,
            "avg_cpu": avg_cpu,
            "avg_memory": avg_memory,
            "avg_disk": avg_disk,
        },
        calculated_at=now,
    )

    db.add(risk_score)
    await db.commit()
    await db.refresh(risk_score)

    return risk_score
