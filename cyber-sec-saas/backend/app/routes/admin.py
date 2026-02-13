from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..auth.dependencies import require_roles
from ..database import get_db
from ..models import Role, User
from ..schemas import UserRead

router = APIRouter(tags=["admin"])


@router.get("/users", response_model=list[UserRead])
def list_users(user=Depends(require_roles(Role.admin)), db: Session = Depends(get_db)):
    return db.query(User).filter(User.tenant_id == user.tenant_id).all()
