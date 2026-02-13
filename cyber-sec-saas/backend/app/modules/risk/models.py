from sqlalchemy import Column, Integer, Float, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from datetime import datetime
import uuid
import enum

Base = declarative_base()

class ThreatLevel(str, enum.Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MODERATE = "moderate"
    LOW = "low"
    MINIMAL = "minimal"

class RiskScore(Base):
    __tablename__ = "risk_scores"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    overall_score = Column(Float, nullable=False)  # 0.0 - 100.0
    threat_level = Column(Enum(ThreatLevel), nullable=False)
    critical_cve_count = Column(Integer, default=0)
    active_alert_count = Column(Integer, default=0)
    cloud_incident_count = Column(Integer, default=0)
    infrastructure_load_avg = Column(Float, default=0.0)
    uptime_percentage = Column(Float, default=100.0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
