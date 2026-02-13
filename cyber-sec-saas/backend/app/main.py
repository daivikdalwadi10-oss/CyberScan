from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from .config import settings
from .database import init_db
from .routes import (
    enterprise_auth_router,
    dashboard_router,
    alerts_ws_router,
    alerts_router,
    incidents_router,
    public_router,
    risk_router,
    metrics_router,
    operations_router,
)
from .scheduler import create_scheduler
from .utils.errors import add_exception_handlers
from .utils.logging import RequestLoggingMiddleware, configure_logging
from .utils.rate_limit import RateLimiter, RateLimitMiddleware
from .utils.security_headers import SecurityHeadersMiddleware
from .utils.metrics_middleware import MetricsMiddleware

configure_logging(settings.log_level)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    scheduler = create_scheduler()
    scheduler.start()
    app.state.scheduler = scheduler
    try:
        yield
    finally:
        scheduler.shutdown(wait=False)


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

allowed_hosts = [host.strip() for host in settings.allowed_hosts.split(",") if host.strip()]
if allowed_hosts:
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)

if settings.security_headers_enabled:
    app.add_middleware(SecurityHeadersMiddleware, hsts=settings.hsts_enabled)

rate_limiter = RateLimiter(settings.rate_limit_requests, settings.rate_limit_window_seconds)
app.add_middleware(RateLimitMiddleware, limiter=rate_limiter)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(MetricsMiddleware)

add_exception_handlers(app)

# Include enterprise routes
app.include_router(enterprise_auth_router)
app.include_router(dashboard_router)
app.include_router(alerts_ws_router)
app.include_router(alerts_router)
app.include_router(incidents_router)
app.include_router(public_router)
app.include_router(risk_router)
app.include_router(metrics_router)
app.include_router(operations_router)


# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok", "service": "CyberSecurity SaaS Backend"}
