"""
Audit logging utilities for security compliance
"""
import uuid
from typing import Optional, Dict, Any
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

from ..models.enterprise_models import AuditLog, User


async def create_audit_log(
    db: AsyncSession,
    action: str,
    user: Optional[User] = None,
    user_id: Optional[uuid.UUID] = None,
    resource_type: Optional[str] = None,
    resource_id: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    success: bool = True
) -> AuditLog:
    """
    Create an audit log entry
    
    Args:
        db: Database session
        action: Action performed (login, logout, create, update, delete, etc.)
        user: User object (optional)
        user_id: User UUID (optional, if user object not available)
        resource_type: Type of resource affected (user, alert, incident, etc.)
        resource_id: ID of the resource
        details: Additional context as JSON
        ip_address: Client IP address
        user_agent: Client user agent string
        success: Whether action succeeded
    
    Returns:
        AuditLog instance
    """
    audit_log = AuditLog(
        user_id=user.id if user else user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details or {},
        ip_address=ip_address,
        user_agent=user_agent,
        success=success
    )
    
    db.add(audit_log)
    await db.commit()
    await db.refresh(audit_log)
    
    return audit_log


async def log_login(
    db: AsyncSession,
    user: User,
    request: Request,
    success: bool = True
):
    """Log user login attempt"""
    return await create_audit_log(
        db=db,
        action="login",
        user=user,
        details={"email": user.email},
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
        success=success
    )


async def log_logout(
    db: AsyncSession,
    user: User,
    request: Request
):
    """Log user logout"""
    return await create_audit_log(
        db=db,
        action="logout",
        user=user,
        details={"email": user.email},
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent")
    )


async def log_resource_access(
    db: AsyncSession,
    user: User,
    resource_type: str,
    resource_id: str,
    action: str = "read",
    details: Optional[Dict] = None
):
    """Log resource access"""
    return await create_audit_log(
        db=db,
        action=action,
        user=user,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details or {}
    )


async def log_permission_denied(
    db: AsyncSession,
    user: User,
    action: str,
    resource_type: Optional[str] = None,
    details: Optional[Dict] = None,
    request: Optional[Request] = None
):
    """Log permission denied attempt"""
    log_details = details or {}
    log_details["attempted_action"] = action
    
    return await create_audit_log(
        db=db,
        action="access_denied",
        user=user,
        resource_type=resource_type,
        details=log_details,
        ip_address=request.client.host if request and request.client else None,
        user_agent=request.headers.get("user-agent") if request else None,
        success=False
    )


async def log_alert_action(
    db: AsyncSession,
    user: User,
    alert_id: uuid.UUID,
    action: str,
    details: Optional[Dict] = None
):
    """Log alert-related actions (acknowledge, resolve, etc.)"""
    return await create_audit_log(
        db=db,
        action=action,
        user=user,
        resource_type="alert",
        resource_id=str(alert_id),
        details=details or {}
    )


async def log_incident_action(
    db: AsyncSession,
    user: User,
    incident_id: uuid.UUID,
    action: str,
    details: Optional[Dict] = None
):
    """Log incident-related actions"""
    return await create_audit_log(
        db=db,
        action=action,
        user=user,
        resource_type="incident",
        resource_id=str(incident_id),
        details=details or {}
    )


async def log_user_management(
    db: AsyncSession,
    admin_user: User,
    action: str,
    target_user_id: uuid.UUID,
    details: Optional[Dict] = None
):
    """Log user management actions"""
    return await create_audit_log(
        db=db,
        action=action,
        user=admin_user,
        resource_type="user",
        resource_id=str(target_user_id),
        details=details or {}
    )
