from fastapi import APIRouter
import socket
import requests

router = APIRouter(prefix="/integration-status", tags=["IntegrationStatus"])

@router.get("/")
def get_integration_status():
    # Example checks (replace with real checks as needed)
    status = {
        "metrics_engine": check_tcp("localhost", 9000),
        "threat_feed": check_http("http://localhost:8000/api/threats"),
        "websocket": check_tcp("localhost", 8080),
        "uptime_monitor": check_http("http://localhost:8000/api/uptime"),
        "database": check_tcp("localhost", 5432),
        "auth_service": check_http("http://localhost:8000/api/auth/health"),
    }
    return status

def check_tcp(host, port, timeout=2):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return "green"
    except Exception:
        return "red"

def check_http(url, timeout=2):
    try:
        r = requests.get(url, timeout=timeout)
        return "green" if r.status_code == 200 else "yellow"
    except Exception:
        return "red"
