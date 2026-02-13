import enum
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from ..database import Base


class LegacyRole(str, enum.Enum):
    super_admin = "SuperAdmin"
    admin = "Admin"
    analyst = "Analyst"
    viewer = "Viewer"


class ScanStatus(str, enum.Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"


class Severity(str, enum.Enum):
    critical = "Critical"
    high = "High"
    medium = "Medium"
    low = "Low"


class LegacyTenant(Base):
    __tablename__ = "legacy_tenants"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    users = relationship("LegacyUser", back_populates="tenant", cascade="all, delete-orphan")
    projects = relationship("LegacyProject", back_populates="tenant", cascade="all, delete-orphan")


class LegacyUser(Base):
    __tablename__ = "legacy_users"

    id = Column(Integer, primary_key=True)
    email = Column(String(320), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(LegacyRole), nullable=False, default=LegacyRole.viewer)
    tenant_id = Column(Integer, ForeignKey('legacy_tenants.id'), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    tenant = relationship("LegacyTenant", back_populates="users")


class LegacyProject(Base):
    __tablename__ = "legacy_projects"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    target_url = Column(String(2048), nullable=False)
    tenant_id = Column(Integer, ForeignKey('legacy_tenants.id'), nullable=False, index=True)

    tenant = relationship("LegacyTenant", back_populates="projects")
    scans = relationship("LegacyScan", back_populates="project", cascade="all, delete-orphan")


class LegacyScan(Base):
    __tablename__ = "legacy_scans"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('legacy_projects.id'), nullable=False, index=True)
    tenant_id = Column(Integer, ForeignKey('legacy_tenants.id'), nullable=False, index=True)
    status = Column(Enum(ScanStatus), nullable=False, default=ScanStatus.pending)
    risk_score = Column(Integer, default=0)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)

    project = relationship("LegacyProject", back_populates="scans")
    vulnerabilities = relationship("LegacyVulnerability", back_populates="scan", cascade="all, delete-orphan")


class LegacyVulnerability(Base):
    __tablename__ = "legacy_vulnerabilities"

    id = Column(Integer, primary_key=True)
    scan_id = Column(Integer, ForeignKey('legacy_scans.id'), nullable=False, index=True)
    tenant_id = Column(Integer, ForeignKey('legacy_tenants.id'), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    severity = Column(Enum(Severity), nullable=False)
    description = Column(Text, nullable=False)
    recommendation = Column(Text, nullable=False)

    scan = relationship("LegacyScan", back_populates="vulnerabilities")


class LegacyAuditLog(Base):
    __tablename__ = "legacy_audit_logs"

    id = Column(Integer, primary_key=True)
    action = Column(String(255), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
