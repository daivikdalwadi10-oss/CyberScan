from typing import cast

from fastapi import APIRouter, Depends
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from starlette.responses import Response
from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.dependencies import get_current_user
from ..database import get_db
from ..metrics import ALERT_COUNT, RISK_SCORE, SYSTEM_CPU, SYSTEM_MEMORY
from ..models.enterprise_models import Alert, AlertStatus, RiskScore, SystemMetric

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("")
async def metrics_endpoint(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    alert_result = await db.execute(
        select(func.count()).select_from(Alert).where(
            Alert.status.in_([AlertStatus.NEW, AlertStatus.ACKNOWLEDGED, AlertStatus.IN_PROGRESS])
        )
    )
    ALERT_COUNT.set(alert_result.scalar_one() or 0)

    risk_result = await db.execute(
        select(RiskScore).order_by(desc(RiskScore.calculated_at)).limit(1)
    )
    risk_score = risk_result.scalar_one_or_none()
    if risk_score:
        RISK_SCORE.set(cast(float, risk_score.overall_score))

    metrics_result = await db.execute(
        select(
            func.avg(SystemMetric.cpu_percent),
            func.avg(SystemMetric.memory_percent),
        )
    )
    avg_cpu, avg_memory = metrics_result.one()
    if avg_cpu is not None:
        SYSTEM_CPU.set(float(avg_cpu))
    if avg_memory is not None:
        SYSTEM_MEMORY.set(float(avg_memory))

    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
