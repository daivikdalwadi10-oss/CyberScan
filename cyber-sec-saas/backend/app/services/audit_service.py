from sqlalchemy.orm import Session

from ..models import AuditLog


def log_action(db: Session, user_id: int, tenant_id: int, action: str) -> None:
    entry = AuditLog(user_id=user_id, tenant_id=tenant_id, action=action)
    db.add(entry)
    db.commit()
