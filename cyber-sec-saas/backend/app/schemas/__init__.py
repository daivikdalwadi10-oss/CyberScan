from .auth import LoginRequest, RefreshRequest, RegisterRequest, TokenResponse
from .dashboard import DashboardConfig, DashboardStats
# Legacy schemas commented out - using enterprise models only
# from .project import ProjectCreate, ProjectRead
# from .report import ReportResponse
# from .scan import ScanDetail, ScanRead, VulnerabilityRead
# from .tenant import TenantCreate, TenantRead
# from .user import UserRead

__all__ = [
    "LoginRequest",
    "RefreshRequest",
    "RegisterRequest",
    "TokenResponse",
    "DashboardConfig",
    "DashboardStats",
    # Legacy
    # "ProjectCreate",
    # "ProjectRead",
    # "ReportResponse",
    # "ScanDetail",
    # "ScanRead",
    # "VulnerabilityRead",
    # "TenantCreate",
    # "TenantRead",
    # "UserRead",
]
