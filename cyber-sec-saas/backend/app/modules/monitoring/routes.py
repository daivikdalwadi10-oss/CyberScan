from fastapi import APIRouter
import socket
import requests

router = APIRouter(prefix="/integration-status", tags=["IntegrationStatus"])

@router.get("/")
import os
def get_integration_status():
    API_HOST = os.getenv("API_HOST", "localhost")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    METRICS_HOST = os.getenv("METRICS_HOST", "localhost")
    METRICS_PORT = int(os.getenv("METRICS_PORT", "9000"))
    WEBSOCKET_HOST = os.getenv("WEBSOCKET_HOST", "localhost")
    WEBSOCKET_PORT = int(os.getenv("WEBSOCKET_PORT", "8080"))
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "5432"))
    status = {
        "metrics_engine": check_tcp(METRICS_HOST, METRICS_PORT),
        "threat_feed": check_http(f"http://{API_HOST}:{API_PORT}/api/threats"),
        "websocket": check_tcp(WEBSOCKET_HOST, WEBSOCKET_PORT),
        "uptime_monitor": check_http(f"http://{API_HOST}:{API_PORT}/api/uptime"),
        "database": check_tcp(DB_HOST, DB_PORT),
        "auth_service": check_http(f"http://{API_HOST}:{API_PORT}/api/auth/health"),
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
