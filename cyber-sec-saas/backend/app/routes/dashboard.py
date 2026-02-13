"""
Dashboard Configuration Routes
Provides role-specific dashboard layouts and metrics
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models.enterprise_models import User, RoleType
from ..auth.dependencies import get_current_user
from ..services.dashboard_service import DashboardConfigService
from ..schemas.dashboard import DashboardConfig, DashboardStats

router = APIRouter(prefix="/api/internal/dashboard", tags=["dashboard"])


@router.get("/config", response_model=DashboardConfig)
async def get_dashboard_config(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get dashboard configuration for current user's primary role
    
    Returns:
    - Menu items navigation
    - Dashboard widgets
    - Quick action buttons
    - Available permissions
    - Visible metrics
    
    Customized per role type
    """
    if not current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User has no assigned roles"
        )
    
    # Use user's first role (primary role)
    primary_role = current_user.roles[0]
    
    return DashboardConfigService.get_dashboard_config(primary_role.role_type)


@router.get("/config/{role_type}", response_model=DashboardConfig)
async def get_dashboard_config_by_role(
    role_type: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get dashboard configuration for a specific role
    
    Admin endpoint to retrieve any role's dashboard configuration
    Useful for testing or admin purposes
    
    Parameters:
    - role_type: The role type (SuperAdmin, SecurityAdmin, SOCAnalyst, etc.)
    """
    # Check if user has admin permissions
    if not any(r.role_type == RoleType.SUPER_ADMIN for r in current_user.roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only super admins can view other role dashboards"
        )
    
    # Validate role type
    try:
        role = RoleType(role_type)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid role type: {role_type}"
        )
    
    return DashboardConfigService.get_dashboard_config(role)


@router.get("/config/all", response_model=list[DashboardConfig])
async def get_all_dashboard_configs(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get dashboard configurations for all roles
    
    Admin endpoint - requires SuperAdmin role
    Useful for admin tools and dashboard builder
    """
    if not any(r.role_type == RoleType.SUPER_ADMIN for r in current_user.roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only super admins can view all dashboards"
        )
    
    return [
        DashboardConfigService.get_dashboard_config(role_type)
        for role_type in RoleType
    ]


@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get statistics about current user's dashboard
    
    Returns metrics about widgets, menu items, permissions
    """
    if not current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User has no assigned roles"
        )
    
    primary_role = current_user.roles[0]
    config = DashboardConfigService.get_dashboard_config(primary_role.role_type)
    
    return DashboardStats(
        total_widgets=len(config.widgets),
        total_menu_items=sum(1 + len(item.children) for item in config.menu_items),
        permissions_count=len(config.permissions),
        metrics_count=len(config.visible_metrics),
    )
