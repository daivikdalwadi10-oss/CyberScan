from datetime import datetime
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from sqlalchemy.orm import Session

from ..models import Scan


def generate_report_pdf(db: Session, scan: Scan) -> BytesIO:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    elements = []
    elements.append(Paragraph("Web Vulnerability Scan Report", styles["Title"]))
    elements.append(Paragraph("Company Logo Placeholder", styles["Heading3"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Executive Summary", styles["Heading2"]))
    elements.append(
        Paragraph(
            f"Scan completed at {scan.completed_at or datetime.utcnow()}.",
            styles["BodyText"],
        )
    )
    elements.append(Paragraph(f"Risk score: {scan.risk_score}", styles["BodyText"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Vulnerabilities", styles["Heading2"]))
    data = [["Name", "Severity", "Description", "Recommendation"]]
    for vuln in scan.vulnerabilities:
        data.append([vuln.name, vuln.severity.value, vuln.description, vuln.recommendation])

    table = Table(data, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    elements.append(table)
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Recommendations", styles["Heading2"]))
    elements.append(
        Paragraph(
            "Prioritize critical and high findings, then address medium and low severity issues.",
            styles["BodyText"],
        )
    )
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Generated: {datetime.utcnow()}", styles["BodyText"]))

    doc.build(elements)
    buffer.seek(0)
    return buffer
