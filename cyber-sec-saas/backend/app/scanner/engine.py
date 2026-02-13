import socket
from urllib.parse import urlparse, urlunparse, urlencode, parse_qs

import requests

from ..models import Severity

SQL_ERRORS = [
    "sql syntax",
    "mysql",
    "sqlite",
    "psql",
    "postgres",
    "unterminated",
    "odbc",
]


def _parse_host(target_url: str) -> str:
    parsed = urlparse(target_url)
    return parsed.hostname or target_url


def scan_ports(host: str) -> list[int]:
    open_ports: list[int] = []
    for port in range(1, 1025):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.1)
            if sock.connect_ex((host, port)) == 0:
                open_ports.append(port)
    return open_ports


def check_headers(target_url: str) -> list[dict]:
    findings = []
    try:
        response = requests.get(target_url, timeout=5)
    except requests.RequestException:
        return findings

    headers = {k.lower(): v for k, v in response.headers.items()}
    if "content-security-policy" not in headers:
        findings.append(
            {
                "name": "Missing Content-Security-Policy",
                "severity": Severity.medium,
                "description": "CSP header is missing.",
                "recommendation": "Add a strict Content-Security-Policy header.",
            }
        )
    if "x-frame-options" not in headers:
        findings.append(
            {
                "name": "Missing X-Frame-Options",
                "severity": Severity.low,
                "description": "X-Frame-Options header is missing.",
                "recommendation": "Add X-Frame-Options: DENY or SAMEORIGIN.",
            }
        )
    if "strict-transport-security" not in headers:
        findings.append(
            {
                "name": "Missing HSTS",
                "severity": Severity.high,
                "description": "HSTS header is missing.",
                "recommendation": "Add Strict-Transport-Security for HTTPS.",
            }
        )
    return findings


def test_sqli(target_url: str) -> list[dict]:
    parsed = urlparse(target_url)
    query = parse_qs(parsed.query)
    query["q"] = ["' OR '1'='1"]
    test_url = urlunparse(parsed._replace(query=urlencode(query, doseq=True)))

    try:
        response = requests.get(test_url, timeout=5)
    except requests.RequestException:
        return []

    body = response.text.lower()
    if any(error in body for error in SQL_ERRORS):
        return [
            {
                "name": "Possible SQL Injection",
                "severity": Severity.high,
                "description": "SQL error signatures detected in response.",
                "recommendation": "Use parameterized queries and input validation.",
            }
        ]
    return []


def run_scan(target_url: str) -> list[dict]:
    host = _parse_host(target_url)
    findings = []

    for port in scan_ports(host):
        findings.append(
            {
                "name": f"Open port detected: {port}",
                "severity": Severity.low,
                "description": f"Port {port} is open on the target host.",
                "recommendation": "Close unused ports and restrict network access.",
            }
        )

    findings.extend(check_headers(target_url))
    findings.extend(test_sqli(target_url))
    return findings
