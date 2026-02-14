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


# Validate environment for production hardening
settings.validate_for_production()
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


# Harden CORS in production
if settings.environment == "production":
    cors_origins = [origin.strip() for origin in settings.cors_origins.split(",") if origin.strip() and not origin.startswith("http://localhost")]
else:
    cors_origins = [origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)


allowed_hosts = [host.strip() for host in settings.allowed_hosts.split(",") if host.strip()]
if settings.environment == "production":
    allowed_hosts = [h for h in allowed_hosts if h not in ("localhost", "127.0.0.1")]
if allowed_hosts:
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)


if settings.security_headers_enabled:
    app.add_middleware(SecurityHeadersMiddleware, hsts=settings.hsts_enabled)

# Enforce HTTPS in production if HSTS is enabled
from fastapi import Request
from fastapi.responses import RedirectResponse
@app.middleware("http")
async def enforce_https(request: Request, call_next):
    if settings.environment == "production" and settings.hsts_enabled:
        if request.url.scheme != "https":
            return RedirectResponse(url=str(request.url.replace(scheme="https")), status_code=307)
    return await call_next(request)

rate_limiter = RateLimiter(settings.rate_limit_requests, settings.rate_limit_window_seconds)
app.add_middleware(RateLimitMiddleware, limiter=rate_limiter)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(MetricsMiddleware)


add_exception_handlers(app, production=(settings.environment == "production"))

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
