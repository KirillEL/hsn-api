from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware
from typing import List

from starlette.responses import JSONResponse

from api.routes import main_router
from api.exceptions import CustomException
from .middlewares import AuthMiddleware, AuthBackend


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
            allow_origins=["http://localhost:5173"],
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
        return JSONResponse(
            status_code=exc.code,
            content={"error_code": exc.error_code, "message": exc.message}
        )


def init_application() -> FastAPI:
    application = FastAPI(
        title="HSN",
        description="HSN_API",
        version="1.0.0",
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
        middleware=init_middlewares()
    )

    init_routers(application)
    init_listeners(application)

    return application


app: FastAPI = init_application()
