from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.core.config import settings
from app.api.v1.health import router as health_router
from app.api.v1.reports import router as reports_router
from app.api.v1.schema import router as schema_router
from app.api.v1.mcp import router as mcp_router
from app.core.app_instance import app

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unexpected error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )

app.include_router(health_router, prefix="/health")
from app.api.v1.users import router as users_router
app.include_router(users_router, prefix="/api/v1/users")
app.include_router(reports_router, prefix="/api/v1/reports")
app.include_router(schema_router, prefix="/schema", tags=["schema"])
from app.api.v1.admin import router as admin_router
app.include_router(admin_router, prefix="/api/v1/admin")
app.include_router(mcp_router, prefix="/mcp", tags=["mcp"])

