from app.models import Severity
from app.utils.risk import calculate_risk_score


def test_calculate_risk_score_caps_at_100():
    severities = [Severity.critical, Severity.critical, Severity.high]
    assert calculate_risk_score(severities) == 100


def test_calculate_risk_score_sums():
    severities = [Severity.high, Severity.medium, Severity.low]
    assert calculate_risk_score(severities) == 40
