import sys
from contextlib import asynccontextmanager
from http import HTTPStatus
from lib2to3.btm_utils import reduce_tree

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware
from typing import List

from loguru import logger
from prometheus_client import Counter
from prometheus_fastapi_instrumentator import Instrumentator

from infra.config import config
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from starlette.responses import JSONResponse
from starlette.status import HTTP_401_UNAUTHORIZED
from api.routes import main_router
from api.exceptions import CustomException
from shared.db.db_session import engine
from shared.db.models import UserDBModel
from shared.redis import redis_service
from .middlewares import AuthMiddleware, AuthBackend
from core.on_startup import (
    hsn_create_admin,
    hsn_create_role_doctor,
)

error_counter = Counter(
    "http_errors_total",
    "Count of HTTP errors by endpoint and status",
    ["endpoint", "status"],
)


def init_routers(app_: FastAPI) -> None:
    app_.include_router(main_router)


def on_auth_error(request: Request, exc: Exception) -> JSONResponse:
    status_code, error_code, message = 401, None, str(exc)
    if isinstance(exc, CustomException):
        status_code: int = int(exc.code)
        error_code: HTTPStatus | None = exc.error_code
        message: str = exc.message

    
    error_counter.labels(request.url.path, exc.error_code).inc()

    return JSONResponse(
        status_code=status_code, content={"error_code": error_code, "message": message}
    )


def init_middlewares() -> List[Middleware]:
    middlewares: List[Middleware] = [
        Middleware(
            CORSMiddleware,
            allow_origins=[
                "http://localhost:5174",
                "http://hsn_admin:5174",
                "http://localhost:1111",
                "http://localhost:3000",
                "http://5.35.99.226:3000",
            ],
            allow_credentials=True,
            allow_methods=["PUT", "POST", "GET", "DELETE", "OPTIONS", "PATCH"],
            allow_headers=["*"],
        ),
        Middleware(AuthMiddleware, backend=AuthBackend(), on_error=on_auth_error),
    ]
    return middlewares


def init_listeners(app_: FastAPI) -> None:
    @app_.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        logger.error(f"Exception: {exc.error_code}; Message: {exc.message}")
        error_counter.labels(request.url.path, exc.error_code).inc()
        return JSONResponse(
            status_code=exc.code,
            content={"error_code": exc.error_code, "message": exc.message},
        )


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await hsn_create_admin()
    await hsn_create_role_doctor()
    # await redis_service.connect()
    yield
    # await redis_service.close()


def init_application() -> FastAPI:
    application = FastAPI(
        title="HSN",
        description="HSN_API",
        version="1.0.0",
        docs_url="/api/v1/docs",
        middleware=init_middlewares(),
        lifespan=lifespan,
    )

    init_routers(app_=application)
    init_listeners(app_=application)

    return application


app: FastAPI = init_application()

Instrumentator().instrument(app=app).expose(app)

http_request_total = Counter("http_request_total", "Total HTTP Requests", ["method", "endpoint"])

@app.middleware("http")
async def count_requests(request: Request, call_next):
    response = await call_next(request)
    if request.url.path != "/metrics" and not request.url.path.endswith("/fields"):
        http_request_total.labels(request.method, request.url.path).inc()
    return response
