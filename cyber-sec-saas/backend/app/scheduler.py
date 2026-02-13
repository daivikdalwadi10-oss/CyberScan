import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from .database import AsyncSessionLocal
from .services.risk_engine import recalculate_risk_score
logger = logging.getLogger("scheduler")


async def fetch_cve_data() -> None:
    logger.info('{"event":"job_start","job":"fetch_cve_data"}')


async def fetch_cloud_status() -> None:
    logger.info('{"event":"job_start","job":"fetch_cloud_status"}')


async def run_uptime_checks() -> None:
    logger.info('{"event":"job_start","job":"run_uptime_checks"}')


async def collect_system_metrics() -> None:
    logger.info('{"event":"job_start","job":"collect_system_metrics"}')


async def recalc_risk_score() -> None:
    logger.info('{"event":"job_start","job":"recalc_risk_score"}')
    async with AsyncSessionLocal() as session:
        await recalculate_risk_score(session)


async def _run_job(job_name: str, job_fn) -> None:
    try:
        await job_fn()
        logger.info('{"event":"job_complete","job":"%s"}' % job_name)
    except Exception:
        logger.exception('{"event":"job_error","job":"%s"}' % job_name)


def create_scheduler() -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone="UTC")

    scheduler.add_job(
        _run_job,
        IntervalTrigger(seconds=60),
        id="fetch_cve_data",
        args=["fetch_cve_data", fetch_cve_data],
        replace_existing=True,
        misfire_grace_time=20,
    )
    scheduler.add_job(
        _run_job,
        IntervalTrigger(seconds=60),
        id="fetch_cloud_status",
        args=["fetch_cloud_status", fetch_cloud_status],
        replace_existing=True,
        misfire_grace_time=20,
    )
    scheduler.add_job(
        _run_job,
        IntervalTrigger(seconds=30),
        id="run_uptime_checks",
        args=["run_uptime_checks", run_uptime_checks],
        replace_existing=True,
        misfire_grace_time=10,
    )
    scheduler.add_job(
        _run_job,
        IntervalTrigger(seconds=20),
        id="collect_system_metrics",
        args=["collect_system_metrics", collect_system_metrics],
        replace_existing=True,
        misfire_grace_time=10,
    )
    scheduler.add_job(
        _run_job,
        IntervalTrigger(seconds=60),
        id="recalc_risk_score",
        args=["recalc_risk_score", recalc_risk_score],
        replace_existing=True,
        misfire_grace_time=20,
    )

    return scheduler
