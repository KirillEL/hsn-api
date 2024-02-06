from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware
from typing import List
from api.routes import main_router


def init_routers(application: FastAPI) -> None:
    application.include_router(main_router)


def init_middlewares() -> List[Middleware]:
    middlewares: List[Middleware] = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"]
        ),
    ]
    return middlewares


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

    return application


app: FastAPI = init_application()
