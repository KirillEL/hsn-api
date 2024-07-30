from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware

from starlette.responses import JSONResponse
from api.routes import main_router
from api.exceptions import CustomException
from .dependencies import Logging
from .middlewares import AuthMiddleware, AuthBackend, SQLAlchemyMiddleware
from utils.on_startup import (
    hsn_create_admin,
    hsn_create_role_doctor,
    create_med_prescriptions,
)


def init_cors(_app: FastAPI) -> None:
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def init_routers(_app: FastAPI) -> None:
    _app.include_router(main_router)


def on_auth_error(request: Request, exc: Exception) -> JSONResponse:
    status_code, error_code, message = 401, None, str(exc)
    if isinstance(exc, CustomException):
        status_code = int(exc.code)
        error_code = exc.error_code
        message = exc.message

    return JSONResponse(
        status_code=status_code, content={"error_code": error_code, "message": message}
    )


def init_middlewares(_app: FastAPI) -> None:
    _app.add_middleware(AuthMiddleware, backend=AuthBackend(), on_error=on_auth_error)
    _app.add_middleware(SQLAlchemyMiddleware)


def init_listeners(_app: FastAPI) -> None:
    @_app.exception_handler(CustomException)
    async def custom_exception_handler(
        request: Request, exc: CustomException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.code,
            content={"error_code": exc.error_code, "message": exc.message},
        )


@asynccontextmanager
async def lifespan(_app: FastAPI) -> None:
    await hsn_create_admin()
    await hsn_create_role_doctor()
    await create_med_prescriptions()
    yield


def init_application() -> FastAPI:
    _app = FastAPI(
        title="HSN",
        description="HSN_API",
        version="1.0.0",
        docs_url="/api/v1/docs",
        dependencies=[Depends(Logging)],
        lifespan=lifespan,
    )

    init_cors(_app)
    init_middlewares(_app)
    init_listeners(_app)
    init_routers(_app)

    return _app


app: FastAPI = init_application()
