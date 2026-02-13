from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/docs-panel", tags=["DocsPanel"])

# Example: role-based documentation content (replace with real markdown/docs engine)
ROLE_GUIDES = {
    "SuperAdmin": "## SuperAdmin Guide\n- Overview of system health\n- How to assign incidents\n- How to manage users",
    "SOCAnalyst": "## SOC Analyst Guide\n- How to handle alerts\n- How to escalate incidents",
    "InfraAdmin": "## Infra Guide\n- How to analyze performance metrics\n- How to interpret uptime data",
    "ComplianceOfficer": "## Compliance Guide\n- How to export reports\n- How to view audit logs",
    "Auditor": "## Auditor Guide\n- How to review audit logs",
    "InternalUser": "## Internal User Guide\n- How to view dashboards",
    "PublicVisitor": "## Public Portal Guide\n- How to interpret public metrics"
}

@router.get("/{role}")
def get_role_guide(role: str):
    guide = ROLE_GUIDES.get(role, "No guide available for this role.")
    return JSONResponse(content={"role": role, "guide": guide})
