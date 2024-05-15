from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware
from typing import List

from loguru import logger

from infra.config import config
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from starlette.responses import JSONResponse
from starlette.status import HTTP_401_UNAUTHORIZED
from api.routes import main_router
from api.exceptions import CustomException
from shared.db.db_session import engine
from shared.db.models import UserDBModel
from .middlewares import AuthMiddleware, AuthBackend
from core.on_startup import hsn_create_admin, hsn_create_role_doctor, create_med_prescriptions


def init_routers(application: FastAPI) -> None:
    application.include_router(main_router)


def on_auth_error(request: Request, exc: Exception):
    status_code, error_code, message = 401, None, str(exc)
    if isinstance(exc, CustomException):
        status_code = int(exc.code)
        error_code = exc.error_code
        message = exc.message

    return JSONResponse(
        status_code=status_code,
        content={"error_code": error_code, "message": message}
    )


def init_middlewares() -> List[Middleware]:
    middlewares: List[Middleware] = [
        Middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:5174", "http://hsn_admin:5174",
                           "http://localhost:1111", "http://localhost:3000", "http://62.109.31.151:3000"],
            allow_credentials=True,
            allow_methods=["PUT", "POST", "GET", "DELETE", "OPTIONS", "PATCH"],
            allow_headers=["*"]
        ),
        Middleware(
            AuthMiddleware,
            backend=AuthBackend(),
            on_error=on_auth_error
        )
    ]
    return middlewares


def init_listeners(app: FastAPI) -> None:
    @app.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        logger.error(f'Exception: {exc.error_code}; Message: {exc.message}')
        return JSONResponse(
            status_code=exc.code,
            content={"error_code": exc.error_code, "message": exc.message}
        )


def init_tasks_on_startup(app_: FastAPI) -> None:
    @app_.on_event("startup")
    async def init_startup():
        await hsn_create_admin()
        await hsn_create_role_doctor()
        await create_med_prescriptions()


def init_secure_on_swagger(app_: FastAPI) -> None:
    security = HTTPBasic()

    @app_.get('/api/docs', include_in_schema=False, dependencies=[Depends(security)])
    async def get_documentation(credentials: HTTPBasicCredentials = Depends(security)):
        if credentials.username != config.DOCS_USERNAME or credentials.password != config.DOCS_PASSWORD:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Basic"},
            )
        else:
            return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")


def init_application() -> FastAPI:
    application = FastAPI(
        title="HSN",
        description="HSN_API",
        version="1.0.0",
        middleware=init_middlewares()
    )

    init_secure_on_swagger(application)
    init_routers(application)
    init_listeners(application)
    init_tasks_on_startup(app_=application)

    return application


app: FastAPI = init_application()
