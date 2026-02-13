from ..models import Severity

SCORES = {
    Severity.critical: 40,
    Severity.high: 25,
    Severity.medium: 10,
    Severity.low: 5,
}


def calculate_risk_score(severities: list[Severity]) -> int:
    total = sum(SCORES.get(severity, 0) for severity in severities)
    return min(total, 100)
