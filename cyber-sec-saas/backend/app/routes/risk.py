from typing import cast

from fastapi import APIRouter, Depends
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.dependencies import get_current_user
from ..database import get_db
from ..models.enterprise_models import RiskScore, User

router = APIRouter(prefix="/api/internal", tags=["risk"])


@router.get("/risk-score")
async def get_latest_risk_score(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(RiskScore).order_by(desc(RiskScore.calculated_at)).limit(1)
    )
    score = result.scalar_one_or_none()
    if not score:
        return {"riskScore": 0, "threatLevel": "minimal", "calculatedAt": None}

    return {
        "riskScore": round(cast(float, score.overall_score)),
        "threatLevel": score.threat_level.value,
        "calculatedAt": score.calculated_at.isoformat(),
        "factors": {
            "criticalCveCount": score.critical_cve_count,
            "activeAlertCount": score.active_alert_count,
            "cloudIncidentCount": score.cloud_incident_count,
            "infrastructureLoadAvg": score.infrastructure_load_avg,
            "uptimePercentage": score.uptime_percentage,
        },
    }
