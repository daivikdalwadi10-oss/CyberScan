from sqlalchemy import Column, String, DateTime, Enum, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from datetime import datetime
import uuid
import enum

Base = declarative_base()

class AssetType(str, enum.Enum):
    SERVER = "server"
    SERVICE = "service"
    API = "api"
    DATABASE = "database"

class AssetHealth(str, enum.Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    DOWN = "down"

class Asset(Base):
    __tablename__ = "assets"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    type = Column(Enum(AssetType), nullable=False)
    health = Column(Enum(AssetHealth), default=AssetHealth.HEALTHY, nullable=False)
    uptime_percentage = Column(Float, default=100.0)
    risk_level = Column(String(32), default="Low")
    owner_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    last_incident_id = Column(UUID(as_uuid=True), ForeignKey('incidents.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
