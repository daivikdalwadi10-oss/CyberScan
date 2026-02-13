"""
Enterprise RBAC - Role-Based Access Control
Permission checking decorators and dependencies
"""
from functools import wraps
from typing import List, Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models.enterprise_models import User, RoleType
from .dependencies import get_current_user


class PermissionError(HTTPException):
    """Custom exception for permission denied"""
    def __init__(
        self,
        required_permissions: Optional[List[str]] = None,
        required_roles: Optional[List[RoleType]] = None
    ):
        detail = "Insufficient permissions"
        if required_roles:
            detail = f"Requires one of roles: {', '.join([r.value for r in required_roles])}"
        elif required_permissions:
            detail = f"Requires permissions: {', '.join(required_permissions)}"
        
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )


def check_permissions(user: User, required_permissions: List[str]) -> bool:
    """Check if user has all required permissions"""
    if not user or not user.roles:
        return False
    
    # SuperAdmin has all permissions
    if user.has_role(RoleType.SUPER_ADMIN):
        return True
    
    # Collect all permissions from all user's roles
    user_permissions = set()
    for role in user.roles:
        user_permissions.update(role.permissions)
    
    # Check if user has all required permissions
    return all(perm in user_permissions for perm in required_permissions)


def check_roles(user: User, required_roles: List[RoleType]) -> bool:
    """Check if user has any of the required roles"""
    if not user or not user.roles:
        return False
    
    return user.has_any_role(required_roles)


class RequirePermissions:
    """Dependency to require specific permissions"""
    def __init__(self, permissions: List[str]):
        self.permissions = permissions
    
    async def __call__(
        self,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
    ):
        if not check_permissions(current_user, self.permissions):
            raise PermissionError(required_permissions=self.permissions)
        
        return current_user


class RequireRoles:
    """Dependency to require specific roles"""
    def __init__(self, roles: List[RoleType]):
        self.roles = roles
    
    async def __call__(
        self,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
    ):
        if not check_roles(current_user, self.roles):
            raise PermissionError(required_roles=self.roles)
        
        return current_user


# Common role requirement dependencies
require_super_admin = RequireRoles([RoleType.SUPER_ADMIN])
require_security_admin = RequireRoles([RoleType.SUPER_ADMIN, RoleType.SECURITY_ADMIN])
require_soc_analyst = RequireRoles([RoleType.SUPER_ADMIN, RoleType.SECURITY_ADMIN, RoleType.SOC_ANALYST])
require_infra_admin = RequireRoles([RoleType.SUPER_ADMIN, RoleType.INFRA_ADMIN])
require_compliance_officer = RequireRoles([RoleType.SUPER_ADMIN, RoleType.COMPLIANCE_OFFICER])
require_auditor = RequireRoles([RoleType.SUPER_ADMIN, RoleType.AUDITOR, RoleType.COMPLIANCE_OFFICER])

# Common permission requirement dependencies
require_alert_write = RequirePermissions(["alert:acknowledge"])
require_incident_write = RequirePermissions(["incident:create"])
require_user_management = RequirePermissions(["user:create", "user:update"])
require_audit_access = RequirePermissions(["audit:read"])


def require_role(*roles: RoleType):
    """
    Decorator for routes requiring specific roles
    
    Usage:
        @router.get("/admin")
        @require_role(RoleType.SUPER_ADMIN, RoleType.SECURITY_ADMIN)
        async def admin_endpoint():
            ...
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user: User = Depends(get_current_user), **kwargs):
            if not check_roles(current_user, list(roles)):
                raise PermissionError(required_roles=list(roles))
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator


def require_permission(*permissions: str):
    """
    Decorator for routes requiring specific permissions
    
    Usage:
        @router.post("/alerts")
        @require_permission("alert:create", "alert:update")
        async def create_alert():
            ...
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user: User = Depends(get_current_user), **kwargs):
            if not check_permissions(current_user, list(permissions)):
                raise PermissionError(required_permissions=list(permissions))
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator
