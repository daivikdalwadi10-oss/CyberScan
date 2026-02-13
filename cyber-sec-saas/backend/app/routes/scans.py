from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session

from ..auth.dependencies import require_roles
from ..database import get_db
from ..models import Project, Role, Scan
from ..schemas import ScanDetail, ScanRead
from ..services.scan_service import execute_scan, start_scan

router = APIRouter(tags=["scans"])


@router.get("/scans", response_model=list[ScanRead])
def list_scans(
    user=Depends(require_roles(Role.admin, Role.analyst, Role.viewer)),
    db: Session = Depends(get_db),
):
    return (
        db.query(Scan)
        .filter(Scan.tenant_id == user.tenant_id)
        .order_by(Scan.started_at.desc().nullslast(), Scan.id.desc())
        .all()
    )


@router.post("/scan/{project_id}", response_model=ScanRead)
def run_scan(
    project_id: int,
    background_tasks: BackgroundTasks,
    user=Depends(require_roles(Role.admin, Role.analyst)),
    db: Session = Depends(get_db),
):
    project = (
        db.query(Project)
        .filter(Project.id == project_id, Project.tenant_id == user.tenant_id)
        .first()
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    scan = start_scan(db, project_id=project.id, tenant_id=user.tenant_id, user_id=user.id)
    background_tasks.add_task(execute_scan, scan.id)
    return scan


@router.get("/scan/{scan_id}", response_model=ScanDetail)
def get_scan(
    scan_id: int,
    user=Depends(require_roles(Role.admin, Role.analyst, Role.viewer)),
    db: Session = Depends(get_db),
):
    scan = (
        db.query(Scan)
        .filter(Scan.id == scan_id, Scan.tenant_id == user.tenant_id)
        .first()
    )
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    return scan
