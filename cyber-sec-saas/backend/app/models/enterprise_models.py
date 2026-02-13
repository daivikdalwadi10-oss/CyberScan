"""
Enterprise Cyber Intelligence Platform - Database Models
Production-grade schema with UUID primary keys, audit trails, and RBAC
Designed for PostgreSQL with fallback to JSON for SQLite
"""
import enum
import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime, Text, 
    ForeignKey, Enum, Table, UniqueConstraint, Index, JSON
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from ..database import Base


# Use JSON (works for both SQLite and PostgreSQL)
JSONType = JSON


# ============================================
# ENUMS
# ============================================

class RoleType(str, enum.Enum):
    """8 distinct roles for enterprise security platform"""
    SUPER_ADMIN = "SuperAdmin"
    SECURITY_ADMIN = "SecurityAdmin"
    SOC_ANALYST = "SOCAnalyst"
    INFRA_ADMIN = "InfraAdmin"
    COMPLIANCE_OFFICER = "ComplianceOfficer"
    AUDITOR = "Auditor"
    INTERNAL_USER = "InternalUser"
    PUBLIC_VISITOR = "PublicVisitor"


class AlertSeverity(str, enum.Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class AlertStatus(str, enum.Enum):
    NEW = "new"
    ACKNOWLEDGED = "acknowledged"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    FALSE_POSITIVE = "false_positive"


class IncidentStatus(str, enum.Enum):
    OPEN = "open"
    INVESTIGATING = "investigating"
    CONTAINED = "contained"
    RESOLVED = "resolved"
    CLOSED = "closed"


class ThreatLevel(str, enum.Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MODERATE = "moderate"
    LOW = "low"
    MINIMAL = "minimal"


# ============================================
# ASSOCIATION TABLES
# ============================================

user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('role_id', UUID(as_uuid=True), ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True),
    Column('assigned_at', DateTime, default=datetime.utcnow, nullable=False),
    Index('idx_user_roles_user', 'user_id'),
    Index('idx_user_roles_role', 'role_id')
)


# ============================================
# CORE MODELS
# ============================================

class User(Base):
    """Enterprise user with multi-role support"""
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(320), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_locked = Column(Boolean, default=False, nullable=False)
    failed_login_attempts = Column(Integer, default=0, nullable=False)
    last_login_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    roles = relationship("Role", secondary=user_roles, back_populates="users")
    audit_logs = relationship("AuditLog", back_populates="user", foreign_keys="[AuditLog.user_id]")
    created_incidents = relationship("Incident", back_populates="created_by_user", foreign_keys="[Incident.created_by]")
    assigned_incidents = relationship("Incident", back_populates="assigned_to_user", foreign_keys="[Incident.assigned_to]")

    def has_role(self, role_type: RoleType) -> bool:
        """Check if user has specific role"""
        return any(r.role_type == role_type for r in self.roles)

    def has_any_role(self, role_types: list[RoleType]) -> bool:
        """Check if user has any of the specified roles"""
        return any(self.has_role(rt) for rt in role_types)


class Role(Base):
    """Predefined security roles with permissions"""
    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role_type = Column(Enum(RoleType), unique=True, nullable=False, index=True)
    display_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    permissions = Column(JSONType, default=list, nullable=False)  # List of permission strings
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    users = relationship("User", secondary=user_roles, back_populates="roles")


class AuditLog(Base):
    """Comprehensive audit trail for security compliance"""
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True, index=True)
    action = Column(String(100), nullable=False, index=True)  # login, logout, create, update, delete, etc.
    resource_type = Column(String(100), nullable=True, index=True)  # user, alert, incident, etc.
    resource_id = Column(String(255), nullable=True)
    details = Column(JSONType, default=dict, nullable=False)  # Additional context
    ip_address = Column(String(45), nullable=True)  # IPv6 compatible
    user_agent = Column(Text, nullable=True)
    success = Column(Boolean, default=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relationships
    user = relationship("User", back_populates="audit_logs", foreign_keys=[user_id])

    __table_args__ = (
        Index('idx_audit_logs_timestamp', 'timestamp'),
        Index('idx_audit_logs_user_action', 'user_id', 'action'),
    )


class Alert(Base):
    """Real-time security alerts"""
    __tablename__ = "alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(Enum(AlertSeverity), nullable=False, index=True)
    status = Column(Enum(AlertStatus), default=AlertStatus.NEW, nullable=False, index=True)
    source = Column(String(100), nullable=False)  # CVE, cloud_monitor, system_check, etc.
    source_id = Column(String(255), nullable=True)  # External ID if applicable
    alert_data = Column(JSONType, default=dict, nullable=False)  # Additional alert data
    acknowledged_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    acknowledged_at = Column(DateTime, nullable=True)
    resolved_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index('idx_alerts_severity_status', 'severity', 'status'),
        Index('idx_alerts_created_at', 'created_at'),
    )


class ThreatIntelRecord(Base):
    """CVE and threat intelligence data"""
    __tablename__ = "threat_intel_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cve_id = Column(String(50), unique=True, nullable=True, index=True)  # CVE-2024-XXXXX
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(Enum(AlertSeverity), nullable=False, index=True)
    cvss_score = Column(Float, nullable=True)  # 0.0 - 10.0
    published_date = Column(DateTime, nullable=True)
    last_modified_date = Column(DateTime, nullable=True)
    affected_products = Column(JSONType, default=lambda: [], nullable=False)
    references = Column(JSONType, default=lambda: [], nullable=False)
    mitigations = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index('idx_threat_intel_severity', 'severity'),
        Index('idx_threat_intel_published', 'published_date'),
    )


class CloudStatusRecord(Base):
    """Cloud provider health monitoring"""
    __tablename__ = "cloud_status_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    provider = Column(String(50), nullable=False, index=True)  # AWS, Azure, GCP, etc.
    service_name = Column(String(100), nullable=False, index=True)
    region = Column(String(50), nullable=True)
    status = Column(String(50), nullable=False)  # operational, degraded, outage
    status_message = Column(Text, nullable=True)
    impact_level = Column(Enum(AlertSeverity), nullable=True)
    checked_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index('idx_cloud_status_provider_service', 'provider', 'service_name'),
        Index('idx_cloud_status_checked_at', 'checked_at'),
    )


class UptimeRecord(Base):
    """Internal service uptime monitoring"""
    __tablename__ = "uptime_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    service_name = Column(String(100), nullable=False, index=True)
    endpoint = Column(String(500), nullable=False)
    is_up = Column(Boolean, nullable=False)
    response_time_ms = Column(Float, nullable=True)
    status_code = Column(Integer, nullable=True)
    error_message = Column(Text, nullable=True)
    checked_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    __table_args__ = (
        Index('idx_uptime_service_checked', 'service_name', 'checked_at'),
    )


class SystemMetric(Base):
    """Infrastructure metrics (CPU, memory, disk, network)"""
    __tablename__ = "system_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hostname = Column(String(255), nullable=False, index=True)
    cpu_percent = Column(Float, nullable=True)
    memory_percent = Column(Float, nullable=True)
    disk_percent = Column(Float, nullable=True)
    network_in_mbps = Column(Float, nullable=True)
    network_out_mbps = Column(Float, nullable=True)
    load_average = Column(Float, nullable=True)
    collected_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    __table_args__ = (
        Index('idx_system_metrics_hostname_collected', 'hostname', 'collected_at'),
    )


class Incident(Base):
    """Security incident management"""
    __tablename__ = "incidents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(Enum(AlertSeverity), nullable=False, index=True)
    status = Column(Enum(IncidentStatus), default=IncidentStatus.OPEN, nullable=False, index=True)
    category = Column(String(100), nullable=True)  # malware, intrusion, data_breach, etc.
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    assigned_to = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    resolution_notes = Column(Text, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    created_by_user = relationship("User", back_populates="created_incidents", foreign_keys=[created_by])
    assigned_to_user = relationship("User", back_populates="assigned_incidents", foreign_keys=[assigned_to])

    __table_args__ = (
        Index('idx_incidents_severity_status', 'severity', 'status'),
        Index('idx_incidents_created_at', 'created_at'),
    )


class RiskScore(Base):
    """Organizational risk scoring over time"""
    __tablename__ = "risk_scores"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    overall_score = Column(Float, nullable=False)  # 0.0 - 100.0
    threat_level = Column(Enum(ThreatLevel), nullable=False)
    
    # Contributing factors
    critical_cve_count = Column(Integer, default=0)
    active_alert_count = Column(Integer, default=0)
    cloud_incident_count = Column(Integer, default=0)
    infrastructure_load_avg = Column(Float, default=0.0)
    uptime_percentage = Column(Float, default=100.0)
    
    # Metadata
    calculation_data = Column(JSONType, default=dict, nullable=False)
    calculated_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    __table_args__ = (
        Index('idx_risk_scores_calculated_at', 'calculated_at'),
    )
