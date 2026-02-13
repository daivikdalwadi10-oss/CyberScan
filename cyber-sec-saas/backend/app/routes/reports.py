from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from ..auth.dependencies import require_roles
from ..database import get_db
from ..models import Role, Scan
from ..services.report_service import generate_report_pdf

router = APIRouter(tags=["reports"])


@router.get("/report/{scan_id}")
def get_report(
    scan_id: int,
    user=Depends(require_roles(Role.admin, Role.analyst, Role.viewer)),
    db: Session = Depends(get_db),
):
    scan = (
        db.query(Scan)
        .filter(Scan.id == scan_id, Scan.tenant_id == user.tenant_id)
        .first()
    )
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")

    pdf_bytes = generate_report_pdf(db, scan)
    return StreamingResponse(
        pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=scan-{scan_id}.pdf"},
    )
