"""
Dashboard configuration schemas
Define dashboard layouts, widgets, and metrics per role
"""
from typing import List, Optional
from pydantic import BaseModel
from enum import Enum


class WidgetType(str, Enum):
    """Types of dashboard widgets"""
    METRIC_CARD = "metric_card"          # Single metric display
    CHART = "chart"                      # Line/bar/pie chart
    TABLE = "table"                      # Data table
    ALERT_LIST = "alert_list"            # List of alerts
    INCIDENT_LIST = "incident_list"      # List of incidents
    TIMELINE = "timeline"                # Event timeline
    MAP = "map"                          # Geographic map
    HEATMAP = "heatmap"                  # Heatmap visualization


class ChartType(str, Enum):
    """Chart types for visualizations"""
    LINE = "line"
    BAR = "bar"
    PIE = "pie"
    AREA = "area"
    SCATTER = "scatter"
    SANKEY = "sankey"


class Widget(BaseModel):
    """Individual dashboard widget"""
    id: str
    type: WidgetType
    title: str
    description: Optional[str] = None
    
    # Chart-specific
    chart_type: Optional[ChartType] = None
    
    # Data source
    metric_key: Optional[str] = None      # For metric cards
    data_endpoint: Optional[str] = None   # API endpoint for data
    
    # Layout
    grid_x: int                           # Column position
    grid_y: int                           # Row position
    grid_width: int = 4                   # Width in grid units
    grid_height: int = 3                  # Height in grid units
    
    # Permissions
    required_permissions: List[str] = []  # Permissions needed to view
    
    # Refresh interval in seconds
    refresh_interval: int = 300


class MenuItem(BaseModel):
    """Navigation menu item"""
    id: str
    label: str
    icon: str
    path: str
    badge_key: Optional[str] = None  # Key for badge count
    children: List['MenuItem'] = []


class DashboardConfig(BaseModel):
    """Complete dashboard configuration for a role"""
    role_type: str
    display_name: str
    description: str
    
    # Layout
    layout_type: str = "grid"  # grid, kanban, timeline
    
    # Menu items
    menu_items: List[MenuItem]
    
    # Dashboard widgets
    widgets: List[Widget]
    
    # Quick actions
    quick_actions: List[dict] = []
    
    # Permissions granted
    permissions: List[str]
    
    # Metrics visible in this dashboard
    visible_metrics: List[str]
    
    # Refresh settings
    auto_refresh: bool = True
    refresh_interval: int = 60  # seconds


class DashboardStats(BaseModel):
    """Dashboard statistics/overview"""
    total_widgets: int
    total_menu_items: int
    permissions_count: int
    metrics_count: int


# Update forward refs for recursive MenuItem
MenuItem.model_rebuild()
