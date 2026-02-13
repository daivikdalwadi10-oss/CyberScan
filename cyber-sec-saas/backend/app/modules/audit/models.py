from sqlalchemy import Column, String, DateTime, Enum, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from datetime import datetime
import uuid
import enum

Base = declarative_base()

class AuditAction(str, enum.Enum):
    LOGIN = "login"
    LOGOUT = "logout"
    ROLE_CHANGE = "role_change"
    INCIDENT_UPDATE = "incident_update"
    CONFIG_CHANGE = "config_change"
    OTHER = "other"

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    action = Column(Enum(AuditAction), nullable=False)
    details = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
