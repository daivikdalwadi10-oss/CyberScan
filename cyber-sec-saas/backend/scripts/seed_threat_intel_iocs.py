"""
Seed threat intelligence records and IOC alerts.
"""
import asyncio
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.models.enterprise_models import Alert, AlertSeverity, AlertStatus, ThreatIntelRecord

THREAT_INTEL = [
    {
        "cve_id": "CVE-2026-10231",
        "title": "Heap overflow in enterprise VPN gateway",
        "description": "A heap overflow in the VPN gateway allows remote attackers to execute code via crafted packets.",
        "severity": AlertSeverity.CRITICAL,
        "cvss_score": 9.8,
        "published_days_ago": 4,
        "affected_products": ["EdgeSecure VPN 5.2", "EdgeSecure VPN 5.3"],
        "references": ["https://example.com/advisories/CVE-2026-10231"],
        "mitigations": "Apply hotfix ES-2026-02 or disable legacy packet inspection.",
    },
    {
        "cve_id": "CVE-2026-09412",
        "title": "Improper auth bypass in container registry",
        "description": "Authentication bypass in registry API allows access to private images under certain headers.",
        "severity": AlertSeverity.HIGH,
        "cvss_score": 8.2,
        "published_days_ago": 12,
        "affected_products": ["CloudRegistry 3.9"],
        "references": ["https://example.com/advisories/CVE-2026-09412"],
        "mitigations": "Upgrade to CloudRegistry 3.9.4 or block the vulnerable endpoint.",
    },
    {
        "cve_id": "CVE-2026-08177",
        "title": "Privilege escalation in endpoint agent",
        "description": "Local privilege escalation due to insecure service permissions in the endpoint agent.",
        "severity": AlertSeverity.MEDIUM,
        "cvss_score": 6.7,
        "published_days_ago": 21,
        "affected_products": ["Sentinel Agent 7.1"],
        "references": ["https://example.com/advisories/CVE-2026-08177"],
        "mitigations": "Update to Sentinel Agent 7.1.3 and review service permissions.",
    },
    {
        "cve_id": "CVE-2026-07305",
        "title": "Weak token generation in SSO broker",
        "description": "Weak randomness in SSO broker token generation could allow token prediction.",
        "severity": AlertSeverity.LOW,
        "cvss_score": 4.3,
        "published_days_ago": 35,
        "affected_products": ["SSO Broker 2.4"],
        "references": ["https://example.com/advisories/CVE-2026-07305"],
        "mitigations": "Rotate tokens and update to SSO Broker 2.4.2.",
    },
]

IOC_ALERTS = [
    {
        "title": "Suspicious domain beaconing",
        "description": "Beaconing detected to a known command-and-control domain.",
        "severity": AlertSeverity.HIGH,
        "status": AlertStatus.NEW,
        "source": "ioc",
        "alert_data": {"indicator": "malicious-telemetry.net", "type": "domain"},
        "created_minutes_ago": 18,
    },
    {
        "title": "Known ransomware hash detected",
        "description": "Endpoint flagged a binary matching a ransomware IOC hash.",
        "severity": AlertSeverity.CRITICAL,
        "status": AlertStatus.ACKNOWLEDGED,
        "source": "ioc",
        "alert_data": {"indicator": "2f9d2f5b7c8e1a9f8d2c3b4a5e6f7a8b", "type": "hash"},
        "created_minutes_ago": 42,
    },
    {
        "title": "Suspicious outbound IP",
        "description": "Outbound traffic to IP associated with recent intrusion campaigns.",
        "severity": AlertSeverity.MEDIUM,
        "status": AlertStatus.IN_PROGRESS,
        "source": "ioc",
        "alert_data": {"indicator": "203.0.113.45", "type": "ip"},
        "created_minutes_ago": 75,
    },
]


async def seed_threat_intel_and_iocs() -> None:
    async with AsyncSessionLocal() as db:
        created_intel = 0
        updated_intel = 0
        created_iocs = 0
        updated_iocs = 0

        now = datetime.now(timezone.utc)

        for record in THREAT_INTEL:
            existing_result = await db.execute(
                select(ThreatIntelRecord).where(ThreatIntelRecord.cve_id == record["cve_id"])
            )
            existing = existing_result.scalar_one_or_none()

            published_date = now - timedelta(days=record["published_days_ago"])

            if existing:
                existing.title = record["title"]
                existing.description = record["description"]
                existing.severity = record["severity"]
                existing.cvss_score = record["cvss_score"]
                existing.published_date = published_date
                existing.last_modified_date = now
                existing.affected_products = record["affected_products"]
                existing.references = record["references"]
                existing.mitigations = record["mitigations"]
                updated_intel += 1
            else:
                db.add(
                    ThreatIntelRecord(
                        id=uuid.uuid4(),
                        cve_id=record["cve_id"],
                        title=record["title"],
                        description=record["description"],
                        severity=record["severity"],
                        cvss_score=record["cvss_score"],
                        published_date=published_date,
                        last_modified_date=now,
                        affected_products=record["affected_products"],
                        references=record["references"],
                        mitigations=record["mitigations"],
                    )
                )
                created_intel += 1

        for alert in IOC_ALERTS:
            existing_result = await db.execute(
                select(Alert).where(Alert.source == "ioc", Alert.title == alert["title"])
            )
            existing = existing_result.scalar_one_or_none()
            created_at = now - timedelta(minutes=alert["created_minutes_ago"])

            if existing:
                existing.description = alert["description"]
                existing.severity = alert["severity"]
                existing.status = alert["status"]
                existing.alert_data = alert["alert_data"]
                existing.created_at = created_at
                existing.updated_at = now
                updated_iocs += 1
            else:
                db.add(
                    Alert(
                        id=uuid.uuid4(),
                        title=alert["title"],
                        description=alert["description"],
                        severity=alert["severity"],
                        status=alert["status"],
                        source=alert["source"],
                        source_id=None,
                        alert_data=alert["alert_data"],
                        created_at=created_at,
                        updated_at=now,
                    )
                )
                created_iocs += 1

        await db.commit()

        print("=" * 70)
        print("Threat intel seeding complete")
        print("=" * 70)
        print(f"Created intel records: {created_intel}")
        print(f"Updated intel records: {updated_intel}")
        print(f"Created IOC alerts: {created_iocs}")
        print(f"Updated IOC alerts: {updated_iocs}")


if __name__ == "__main__":
    asyncio.run(seed_threat_intel_and_iocs())
