import time
from typing import Dict

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int) -> None:
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.clients: Dict[str, tuple[int, float]] = {}

    def check(self, client_id: str) -> bool:
        now = time.time()
        count, reset_at = self.clients.get(client_id, (0, now + self.window_seconds))
        if now > reset_at:
            count, reset_at = 0, now + self.window_seconds
        count += 1
        self.clients[client_id] = (count, reset_at)
        return count <= self.max_requests


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limiter: RateLimiter):
        super().__init__(app)
        self.limiter = limiter

    async def dispatch(self, request: Request, call_next):
        client_id = request.client.host if request.client else "unknown"
        if not self.limiter.check(client_id):
            return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})
        return await call_next(request)
