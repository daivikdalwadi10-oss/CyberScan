from datetime import datetime

from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..models import Scan, ScanStatus, Severity, Vulnerability
from ..scanner import run_scan
from ..utils.risk import calculate_risk_score
from .audit_service import log_action


def start_scan(db: Session, project_id: int, tenant_id: int, user_id: int) -> Scan:
    scan = Scan(project_id=project_id, tenant_id=tenant_id, status=ScanStatus.pending)
    db.add(scan)
    db.commit()
    db.refresh(scan)
    log_action(db, user_id=user_id, tenant_id=tenant_id, action=f"Started scan {scan.id}")
    return scan


def execute_scan(scan_id: int) -> None:
    db = SessionLocal()
    try:
        scan = db.query(Scan).filter(Scan.id == scan_id).first()
        if not scan:
            return
        scan.status = ScanStatus.running
        scan.started_at = datetime.utcnow()
        db.commit()

        target_url = scan.project.target_url
        findings = run_scan(target_url)
        severities: list[Severity] = []

        for finding in findings:
            severity = finding["severity"]
            severities.append(severity)
            vulnerability = Vulnerability(
                scan_id=scan.id,
                tenant_id=scan.tenant_id,
                name=finding["name"],
                severity=severity,
                description=finding["description"],
                recommendation=finding["recommendation"],
            )
            db.add(vulnerability)

        scan.risk_score = calculate_risk_score(severities)
        scan.status = ScanStatus.completed
        scan.completed_at = datetime.utcnow()
        db.commit()
    except Exception:
        scan = db.query(Scan).filter(Scan.id == scan_id).first()
        if scan:
            scan.status = ScanStatus.failed
            db.commit()
    finally:
        db.close()
