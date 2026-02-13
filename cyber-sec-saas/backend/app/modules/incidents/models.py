from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base

class IncidentStatus(str, enum.Enum):
    open = "Open"
    investigating = "Investigating"
    resolved = "Resolved"

class Incident(Base):
    __tablename__ = "incidents"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(Enum(IncidentStatus), default=IncidentStatus.open)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    assigned_to_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    assigned_to = relationship("User", back_populates="incidents")
    timeline = Column(Text)  # JSON or text for timeline events
    evidence = Column(Text)  # JSON or text for evidence links/notes

# Add relationship to User model in app/models/enterprise_models.py:
# incidents = relationship("Incident", back_populates="assigned_to")
