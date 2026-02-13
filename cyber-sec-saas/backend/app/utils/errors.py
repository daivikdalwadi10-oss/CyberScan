import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse


def add_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        logging.getLogger("app").warning("http_error", extra={"detail": exc.detail})
        return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logging.getLogger("app").exception("unhandled_exception")
        return JSONResponse(status_code=500, content={"error": "Internal server error"})
