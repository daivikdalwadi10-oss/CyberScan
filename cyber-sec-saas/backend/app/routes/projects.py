from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..auth.dependencies import require_roles
from ..database import get_db
from ..models import Project, Role
from ..schemas import ProjectCreate, ProjectRead

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("", response_model=ProjectRead)
def create_project(
    payload: ProjectCreate,
    user=Depends(require_roles(Role.admin, Role.analyst)),
    db: Session = Depends(get_db),
):
    project = Project(name=payload.name, target_url=payload.target_url, tenant_id=user.tenant_id)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.get("", response_model=list[ProjectRead])
def list_projects(user=Depends(require_roles(Role.admin, Role.analyst, Role.viewer)), db: Session = Depends(get_db)):
    return db.query(Project).filter(Project.tenant_id == user.tenant_id).all()
