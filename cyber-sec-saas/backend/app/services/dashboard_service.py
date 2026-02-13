"""
Dashboard configuration service
Generates role-specific dashboard layouts and configurations
"""
from app.models.enterprise_models import RoleType
from app.schemas.dashboard import (
    DashboardConfig, Widget, MenuItem, WidgetType, ChartType
)
from typing import Dict


class DashboardConfigService:
    """Service for generating dashboard configurations per role"""
    
    @staticmethod
    def get_menu_for_role(role_type: RoleType) -> list[MenuItem]:
        """Generate navigation menu items for a role"""
        
        # Common items for all authenticated users
        common = [
            MenuItem(
                id="dashboard",
                label="Dashboard",
                icon="grid-3x3-gap",
                path="/dashboard"
            )
        ]
        
        # Role-specific menus
        menus = {
            RoleType.SUPER_ADMIN: common + [
                MenuItem(
                    id="admin",
                    label="Administration",
                    icon="gear",
                    path="/admin",
                    children=[
                        MenuItem(id="users", label="Users", icon="people", path="/admin/users"),
                        MenuItem(id="roles", label="Roles", icon="badge", path="/admin/roles"),
                        MenuItem(id="audit-logs", label="Audit Logs", icon="file-text", path="/admin/audit"),
                        MenuItem(id="system", label="System", icon="sliders", path="/admin/system"),
                    ]
                ),
                MenuItem(
                    id="security",
                    label="Security",
                    icon="shield",
                    path="/security",
                    children=[
                        MenuItem(id="alerts", label="Alerts", icon="bell", path="/security/alerts", badge_key="alert_count"),
                        MenuItem(id="incidents", label="Incidents", icon="alert-circle", path="/security/incidents", badge_key="incident_count"),
                        MenuItem(id="threats", label="Threats", icon="zap", path="/security/threats"),
                    ]
                ),
                MenuItem(
                    id="operations",
                    label="Operations",
                    icon="activity",
                    path="/operations",
                    children=[
                        MenuItem(id="cloud", label="Cloud Status", icon="cloud", path="/operations/cloud"),
                        MenuItem(id="uptime", label="Uptime", icon="trending-up", path="/operations/uptime"),
                        MenuItem(id="metrics", label="Metrics", icon="bar-chart-2", path="/operations/metrics"),
                    ]
                ),
                MenuItem(
                    id="compliance",
                    label="Compliance",
                    icon="check-circle",
                    path="/compliance",
                    children=[
                        MenuItem(id="reports", label="Reports", icon="file", path="/compliance/reports"),
                        MenuItem(id="risks", label="Risk Scores", icon="alert-triangle", path="/compliance/risks"),
                    ]
                ),
            ],
            
            RoleType.SECURITY_ADMIN: common + [
                MenuItem(
                    id="security",
                    label="Security Operations",
                    icon="shield",
                    path="/security",
                    children=[
                        MenuItem(id="alerts", label="Alerts", icon="bell", path="/security/alerts", badge_key="alert_count"),
                        MenuItem(id="incidents", label="Incidents", icon="alert-circle", path="/security/incidents", badge_key="incident_count"),
                        MenuItem(id="threats", label="Threat Intel", icon="zap", path="/security/threats"),
                        MenuItem(id="soar", label="Automation", icon="play-circle", path="/security/automation"),
                    ]
                ),
                MenuItem(
                    id="operations",
                    label="Infrastructure",
                    icon="activity",
                    path="/operations",
                    children=[
                        MenuItem(id="cloud", label="Cloud Status", icon="cloud", path="/operations/cloud"),
                        MenuItem(id="uptime", label="Uptime", icon="trending-up", path="/operations/uptime"),
                    ]
                ),
            ],
            
            RoleType.SOC_ANALYST: common + [
                MenuItem(
                    id="threats",
                    label="Threat Monitoring",
                    icon="radar",
                    path="/threats",
                    children=[
                        MenuItem(id="alerts", label="Active Alerts", icon="bell", path="/threats/alerts", badge_key="alert_count"),
                        MenuItem(id="incidents", label="My Incidents", icon="alert-circle", path="/threats/incidents"),
                        MenuItem(id="queue", label="Work Queue", icon="inbox", path="/threats/queue"),
                    ]
                ),
                MenuItem(
                    id="intelligence",
                    label="Threat Intel",
                    icon="info",
                    path="/intelligence",
                    children=[
                        MenuItem(id="indicators", label="IOCs", icon="target", path="/intelligence/indicators"),
                        MenuItem(id="sources", label="Sources", icon="link", path="/intelligence/sources"),
                    ]
                ),
            ],
            
            RoleType.INFRA_ADMIN: common + [
                MenuItem(
                    id="infrastructure",
                    label="Infrastructure",
                    icon="server",
                    path="/infrastructure",
                    children=[
                        MenuItem(id="uptime", label="Uptime Status", icon="trending-up", path="/infrastructure/uptime"),
                        MenuItem(id="metrics", label="Performance", icon="bar-chart-2", path="/infrastructure/metrics"),
                        MenuItem(id="alerts", label="Alerts", icon="bell", path="/infrastructure/alerts", badge_key="alert_count"),
                    ]
                ),
                MenuItem(
                    id="cloud",
                    label="Cloud Services",
                    icon="cloud",
                    path="/cloud",
                    children=[
                        MenuItem(id="status", label="Status", icon="cloud-check", path="/cloud/status"),
                        MenuItem(id="costs", label="Costs", icon="dollar-sign", path="/cloud/costs"),
                    ]
                ),
            ],
            
            RoleType.COMPLIANCE_OFFICER: common + [
                MenuItem(
                    id="compliance",
                    label="Compliance",
                    icon="check-circle",
                    path="/compliance",
                    children=[
                        MenuItem(id="reports", label="Reports", icon="file-text", path="/compliance/reports"),
                        MenuItem(id="audit-logs", label="Audit Logs", icon="file", path="/compliance/audit"),
                        MenuItem(id="risks", label="Risk Assessment", icon="alert-triangle", path="/compliance/risks"),
                    ]
                ),
                MenuItem(
                    id="evidence",
                    label="Evidence",
                    icon="archive",
                    path="/evidence",
                ),
            ],
            
            RoleType.AUDITOR: common + [
                MenuItem(
                    id="audit",
                    label="Audit Trail",
                    icon="file-text",
                    path="/audit",
                    children=[
                        MenuItem(id="logs", label="Audit Logs", icon="list", path="/audit/logs"),
                        MenuItem(id="reports", label="Reports", icon="file", path="/audit/reports"),
                    ]
                ),
            ],
            
            RoleType.INTERNAL_USER: common + [
                MenuItem(
                    id="metrics",
                    label="My Metrics",
                    icon="bar-chart-2",
                    path="/metrics",
                ),
                MenuItem(
                    id="status",
                    label="Status",
                    icon="trending-up",
                    path="/status",
                ),
            ],
            
            RoleType.PUBLIC_VISITOR: [
                MenuItem(
                    id="public-dashboard",
                    label="Public Dashboard",
                    icon="eye",
                    path="/public"
                ),
            ],
        }
        
        return menus.get(role_type, common)
    
    @staticmethod
    def get_widgets_for_role(role_type: RoleType) -> list[Widget]:
        """Generate dashboard widgets for a role"""
        
        widgets = {
            RoleType.SUPER_ADMIN: [
                # Overview row
                Widget(
                    id="active_alerts",
                    type=WidgetType.METRIC_CARD,
                    title="Active Alerts",
                    metric_key="alert:count:active",
                    grid_x=0, grid_y=0, grid_width=2, grid_height=2,
                    required_permissions=["alert:read"],
                ),
                Widget(
                    id="open_incidents",
                    type=WidgetType.METRIC_CARD,
                    title="Open Incidents",
                    metric_key="incident:count:open",
                    grid_x=2, grid_y=0, grid_width=2, grid_height=2,
                    required_permissions=["incident:read"],
                ),
                Widget(
                    id="avg_risk_score",
                    type=WidgetType.METRIC_CARD,
                    title="Avg Risk Score",
                    metric_key="risk:score:average",
                    grid_x=4, grid_y=0, grid_width=2, grid_height=2,
                    required_permissions=["risk:read"],
                ),
                Widget(
                    id="system_health",
                    type=WidgetType.METRIC_CARD,
                    title="System Health",
                    metric_key="system:health:overall",
                    grid_x=6, grid_y=0, grid_width=2, grid_height=2,
                ),
                # Charts row
                Widget(
                    id="alert_trends",
                    type=WidgetType.CHART,
                    title="Alert Trends (24h)",
                    chart_type=ChartType.AREA,
                    data_endpoint="/api/internal/metrics/alert-trends",
                    grid_x=0, grid_y=2, grid_width=4, grid_height=3,
                    required_permissions=["alert:read"],
                    refresh_interval=300,
                ),
                Widget(
                    id="threat_distribution",
                    type=WidgetType.CHART,
                    title="Threat Distribution",
                    chart_type=ChartType.PIE,
                    data_endpoint="/api/internal/metrics/threat-distribution",
                    grid_x=4, grid_y=2, grid_width=4, grid_height=3,
                    required_permissions=["threat:read"],
                    refresh_interval=600,
                ),
                # Lists row
                Widget(
                    id="recent_alerts",
                    type=WidgetType.ALERT_LIST,
                    title="Recent Alerts",
                    data_endpoint="/api/internal/alerts?limit=5",
                    grid_x=0, grid_y=5, grid_width=4, grid_height=3,
                    required_permissions=["alert:read"],
                ),
                Widget(
                    id="critical_incidents",
                    type=WidgetType.INCIDENT_LIST,
                    title="Critical Incidents",
                    data_endpoint="/api/internal/incidents?severity=CRITICAL&limit=5",
                    grid_x=4, grid_y=5, grid_width=4, grid_height=3,
                    required_permissions=["incident:read"],
                ),
            ],
            
            RoleType.SECURITY_ADMIN: [
                Widget(
                    id="active_alerts",
                    type=WidgetType.METRIC_CARD,
                    title="Active Alerts",
                    metric_key="alert:count:active",
                    grid_x=0, grid_y=0, grid_width=2, grid_height=2,
                ),
                Widget(
                    id="open_incidents",
                    type=WidgetType.METRIC_CARD,
                    title="Open Incidents",
                    metric_key="incident:count:open",
                    grid_x=2, grid_y=0, grid_width=2, grid_height=2,
                ),
                Widget(
                    id="mean_response_time",
                    type=WidgetType.METRIC_CARD,
                    title="Mean Response Time",
                    metric_key="incident:response:mean",
                    grid_x=4, grid_y=0, grid_width=2, grid_height=2,
                ),
                Widget(
                    id="threat_level",
                    type=WidgetType.METRIC_CARD,
                    title="Current Threat Level",
                    metric_key="threat:level:current",
                    grid_x=6, grid_y=0, grid_width=2, grid_height=2,
                ),
                Widget(
                    id="alert_timeline",
                    type=WidgetType.CHART,
                    title="Alert Timeline",
                    chart_type=ChartType.AREA,
                    data_endpoint="/api/internal/metrics/alert-timeline",
                    grid_x=0, grid_y=2, grid_width=6, grid_height=3,
                ),
                Widget(
                    id="incident_queue",
                    type=WidgetType.INCIDENT_LIST,
                    title="Incident Queue",
                    data_endpoint="/api/internal/incidents?status=OPEN&limit=10",
                    grid_x=6, grid_y=2, grid_width=2, grid_height=5,
                ),
                Widget(
                    id="recent_alerts",
                    type=WidgetType.ALERT_LIST,
                    title="Recent Alerts",
                    data_endpoint="/api/internal/alerts?limit=8",
                    grid_x=0, grid_y=5, grid_width=6, grid_height=3,
                ),
            ],
            
            RoleType.SOC_ANALYST: [
                Widget(
                    id="alert_queue",
                    type=WidgetType.METRIC_CARD,
                    title="My Alert Queue",
                    metric_key="alert:count:assigned_to_me",
                    grid_x=0, grid_y=0, grid_width=2, grid_height=2,
                ),
                Widget(
                    id="my_incidents",
                    type=WidgetType.METRIC_CARD,
                    title="My Incidents",
                    metric_key="incident:count:assigned_to_me",
                    grid_x=2, grid_y=0, grid_width=2, grid_height=2,
                ),
                Widget(
                    id="avg_resolution_time",
                    type=WidgetType.METRIC_CARD,
                    title="Avg Resolution",
                    metric_key="incident:resolution:mean",
                    grid_x=4, grid_y=0, grid_width=2, grid_height=2,
                ),
                Widget(
                    id="threat_sources",
                    type=WidgetType.CHART,
                    title="Top Threat Sources",
                    chart_type=ChartType.BAR,
                    data_endpoint="/api/internal/metrics/threat-sources",
                    grid_x=0, grid_y=2, grid_width=3, grid_height=4,
                ),
                Widget(
                    id="assigned_alerts",
                    type=WidgetType.ALERT_LIST,
                    title="Assigned to Me",
                    data_endpoint="/api/internal/alerts?assigned_to=me&limit=10",
                    grid_x=3, grid_y=2, grid_width=5, grid_height=4,
                ),
                Widget(
                    id="incident_board",
                    type=WidgetType.INCIDENT_LIST,
                    title="Work Queue",
                    data_endpoint="/api/internal/incidents?assigned_to=me&status=OPEN",
                    grid_x=0, grid_y=6, grid_width=8, grid_height=3,
                ),
            ],
            
            RoleType.INFRA_ADMIN: [
                Widget(
                    id="uptime_percentage",
                    type=WidgetType.METRIC_CARD,
                    title="System Uptime",
                    metric_key="system:uptime:percentage",
                    grid_x=0, grid_y=0, grid_width=2, grid_height=2,
                ),
                Widget(
                    id="avg_latency",
                    type=WidgetType.METRIC_CARD,
                    title="Avg Latency",
                    metric_key="system:latency:mean",
                    grid_x=2, grid_y=0, grid_width=2, grid_height=2,
                ),
                Widget(
                    id="cpu_usage",
                    type=WidgetType.METRIC_CARD,
                    title="CPU Usage",
                    metric_key="system:cpu:usage",
                    grid_x=4, grid_y=0, grid_width=2, grid_height=2,
                ),
                Widget(
                    id="memory_usage",
                    type=WidgetType.METRIC_CARD,
                    title="Memory Usage",
                    metric_key="system:memory:usage",
                    grid_x=6, grid_y=0, grid_width=2, grid_height=2,
                ),
                Widget(
                    id="uptime_trend",
                    type=WidgetType.CHART,
                    title="Uptime Trend",
                    chart_type=ChartType.LINE,
                    data_endpoint="/api/internal/metrics/uptime-trend",
                    grid_x=0, grid_y=2, grid_width=4, grid_height=3,
                ),
                Widget(
                    id="resource_heatmap",
                    type=WidgetType.HEATMAP,
                    title="Resource Usage Heatmap",
                    data_endpoint="/api/internal/metrics/resource-heatmap",
                    grid_x=4, grid_y=2, grid_width=4, grid_height=3,
                ),
            ],
            
            RoleType.COMPLIANCE_OFFICER: [
                Widget(
                    id="compliance_score",
                    type=WidgetType.METRIC_CARD,
                    title="Compliance Score",
                    metric_key="compliance:score:overall",
                    grid_x=0, grid_y=0, grid_width=2, grid_height=2,
                ),
                Widget(
                    id="avg_risk",
                    type=WidgetType.METRIC_CARD,
                    title="Avg Risk Score",
                    metric_key="risk:score:average",
                    grid_x=2, grid_y=0, grid_width=2, grid_height=2,
                ),
                Widget(
                    id="audit_events",
                    type=WidgetType.METRIC_CARD,
                    title="Audit Events (24h)",
                    metric_key="audit:count:24h",
                    grid_x=4, grid_y=0, grid_width=2, grid_height=2,
                ),
                Widget(
                    id="risk_distribution",
                    type=WidgetType.CHART,
                    title="Risk Distribution",
                    chart_type=ChartType.PIE,
                    data_endpoint="/api/internal/metrics/risk-distribution",
                    grid_x=0, grid_y=2, grid_width=4, grid_height=4,
                ),
                Widget(
                    id="compliance_timeline",
                    type=WidgetType.TIMELINE,
                    title="Compliance Events",
                    data_endpoint="/api/internal/metrics/compliance-timeline",
                    grid_x=4, grid_y=2, grid_width=4, grid_height=4,
                ),
            ],
            
            RoleType.AUDITOR: [
                Widget(
                    id="audit_count",
                    type=WidgetType.METRIC_CARD,
                    title="Total Audit Events",
                    metric_key="audit:count:total",
                    grid_x=0, grid_y=0, grid_width=2, grid_height=2,
                ),
                Widget(
                    id="recent_audits",
                    type=WidgetType.TABLE,
                    title="Recent Audit Log",
                    data_endpoint="/api/internal/audit-logs?limit=15",
                    grid_x=0, grid_y=2, grid_width=8, grid_height=5,
                ),
            ],
            
            RoleType.INTERNAL_USER: [
                Widget(
                    id="my_metrics",
                    type=WidgetType.METRIC_CARD,
                    title="My Metrics",
                    metric_key="user:metrics:summary",
                    grid_x=0, grid_y=0, grid_width=4, grid_height=2,
                ),
                Widget(
                    id="system_status",
                    type=WidgetType.METRIC_CARD,
                    title="System Status",
                    metric_key="system:status:overall",
                    grid_x=4, grid_y=0, grid_width=4, grid_height=2,
                ),
                Widget(
                    id="personal_notifications",
                    type=WidgetType.ALERT_LIST,
                    title="My Notifications",
                    data_endpoint="/api/internal/notifications?limit=10",
                    grid_x=0, grid_y=2, grid_width=8, grid_height=3,
                ),
            ],
            
            RoleType.PUBLIC_VISITOR: [
                Widget(
                    id="public_status",
                    type=WidgetType.METRIC_CARD,
                    title="System Status",
                    metric_key="public:status",
                    grid_x=0, grid_y=0, grid_width=4, grid_height=2,
                ),
                Widget(
                    id="public_incidents",
                    type=WidgetType.ALERT_LIST,
                    title="Service Incidents",
                    data_endpoint="/api/public/incidents?limit=5",
                    grid_x=0, grid_y=2, grid_width=8, grid_height=3,
                ),
            ],
        }
        
        return widgets.get(role_type, [])
    
    @staticmethod
    def get_quick_actions_for_role(role_type: RoleType) -> list[dict]:
        """Generate quick action buttons for a role"""
        
        actions = {
            RoleType.SUPER_ADMIN: [
                {"id": "create_user", "label": "Add User", "icon": "user-plus", "action": "open:/admin/users/create", "color": "blue"},
                {"id": "new_incident", "label": "Create Incident", "icon": "alert-circle", "action": "open:/security/incidents/create", "color": "red"},
                {"id": "view_audit", "label": "View Audit Log", "icon": "file-text", "action": "open:/admin/audit", "color": "green"},
            ],
            RoleType.SECURITY_ADMIN: [
                {"id": "new_alert", "label": "Create Alert", "icon": "bell", "action": "open:/security/alerts/create", "color": "orange"},
                {"id": "incident_create", "label": "New Incident", "icon": "alert-triangle", "action": "open:/security/incidents/create", "color": "red"},
            ],
            RoleType.SOC_ANALYST: [
                {"id": "claim_alert", "label": "Claim Alert", "icon": "check", "action": "claim_next_alert", "color": "blue"},
                {"id": "resolve_incident", "label": "Resolve Incident", "icon": "check-circle", "action": "resolve_next_incident", "color": "green"},
            ],
            RoleType.INFRA_ADMIN: [
                {"id": "check_status", "label": "System Check", "icon": "activity", "action": "trigger:system_check", "color": "blue"},
                {"id": "scale_resources", "label": "Scale Resources", "icon": "zap", "action": "open:/infrastructure/scale", "color": "orange"},
            ],
            RoleType.COMPLIANCE_OFFICER: [
                {"id": "generate_report", "label": "Generate Report", "icon": "file-text", "action": "open:/compliance/reports/create", "color": "blue"},
                {"id": "risk_assessment", "label": "Risk Assessment", "icon": "alert-triangle", "action": "open:/compliance/risks", "color": "red"},
            ],
        }
        
        return actions.get(role_type, [])
    
    @staticmethod
    def get_permissions_for_role(role_type: RoleType) -> list[str]:
        """Get all permissions for a role"""
        
        permissions_map = {
            RoleType.SUPER_ADMIN: [
                "user:create", "user:read", "user:update", "user:delete",
                "role:assign", "role:revoke", "role:read",
                "alert:create", "alert:read", "alert:update", "alert:delete", "alert:acknowledge",
                "incident:create", "incident:read", "incident:update", "incident:delete", "incident:assign",
                "audit:read", "audit:export",
                "threat:read", "threat:create",
                "cloud:read", "cloud:update",
                "metrics:read", "metrics:export",
                "risk:read", "risk:calculate",
                "system:configure", "system:restart",
                "dashboard:all",
            ],
            RoleType.SECURITY_ADMIN: [
                "alert:read", "alert:acknowledge", "alert:update",
                "incident:read", "incident:update", "incident:assign", "incident:create",
                "threat:read",
                "audit:read",
                "metrics:read",
                "risk:read",
                "dashboard:security",
            ],
            RoleType.SOC_ANALYST: [
                "alert:read", "alert:acknowledge",
                "incident:read", "incident:update",
                "threat:read",
                "audit:read",
                "dashboard:soc",
            ],
            RoleType.INFRA_ADMIN: [
                "cloud:read",
                "metrics:read", "metrics:export",
                "audit:read",
                "dashboard:infra",
            ],
            RoleType.COMPLIANCE_OFFICER: [
                "audit:read", "audit:export",
                "risk:read",
                "threat:read",
                "dashboard:compliance",
            ],
            RoleType.AUDITOR: [
                "audit:read", "audit:export",
                "dashboard:audit",
            ],
            RoleType.INTERNAL_USER: [
                "metrics:read",
                "dashboard:internal",
            ],
            RoleType.PUBLIC_VISITOR: [
                "dashboard:public",
            ],
        }
        
        return permissions_map.get(role_type, [])
    
    @staticmethod
    def get_dashboard_config(role_type: RoleType) -> DashboardConfig:
        """Generate complete dashboard configuration for a role"""
        
        role_display_names = {
            RoleType.SUPER_ADMIN: "Super Administrator",
            RoleType.SECURITY_ADMIN: "Security Administrator",
            RoleType.SOC_ANALYST: "SOC Analyst",
            RoleType.INFRA_ADMIN: "Infrastructure Administrator",
            RoleType.COMPLIANCE_OFFICER: "Compliance Officer",
            RoleType.AUDITOR: "Auditor",
            RoleType.INTERNAL_USER: "Internal User",
            RoleType.PUBLIC_VISITOR: "Public Visitor",
        }
        
        role_descriptions = {
            RoleType.SUPER_ADMIN: "Platform super administrator with full system access",
            RoleType.SECURITY_ADMIN: "Security operations administrator",
            RoleType.SOC_ANALYST: "Security Operations Center analyst",
            RoleType.INFRA_ADMIN: "Infrastructure and system administration",
            RoleType.COMPLIANCE_OFFICER: "Compliance and audit officer",
            RoleType.AUDITOR: "Read-only auditor",
            RoleType.INTERNAL_USER: "Internal employee with limited access",
            RoleType.PUBLIC_VISITOR: "Public dashboard visitor",
        }
        
        permissions = DashboardConfigService.get_permissions_for_role(role_type)
        
        return DashboardConfig(
            role_type=role_type.value,
            display_name=role_display_names.get(role_type, role_type.value),
            description=role_descriptions.get(role_type, ""),
            menu_items=DashboardConfigService.get_menu_for_role(role_type),
            widgets=DashboardConfigService.get_widgets_for_role(role_type),
            quick_actions=DashboardConfigService.get_quick_actions_for_role(role_type),
            permissions=permissions,
            visible_metrics=[
                "alert:count:active",
                "incident:count:open",
                "system:uptime:percentage",
                "risk:score:average",
            ],
        )
