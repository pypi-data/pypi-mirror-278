from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from integra_python_connect.src.common.settings import SETTINGS
from integra_python_connect.src.routers.v1.base import base_router


class Builder:
    @classmethod
    def start(cls):
        application = FastAPI(
            lifespan=cls.lifespan,
            title="Python-bridge",
            description="Инструмент Integra предназначенный для подключения внешних Python сервисов",
            docs_url=f"{SETTINGS.API_PREFIX}/docs",
            redoc_url=f"{SETTINGS.API_PREFIX}/redoc",
            openapi_url=f"{SETTINGS.API_PREFIX}/openapi.json"
        )

        application.add_middleware(
            CORSMiddleware,
            allow_credentials=True,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )
        application.include_router(router=base_router)

        # # Add prometheus metrics
        # Instrumentator().instrument(application).expose(
        #     application,
        #     endpoint=f'{SETTINGS.API_PREFIX}/services/metrics',
        #     tags=["Сервис"]
        # )
        # self.register_exception_handlers(application)

        return application

    @classmethod
    @asynccontextmanager
    async def lifespan(cls, app: FastAPI):
        await cls.on_startup()
        yield
        await cls.on_shutdown()

    @classmethod
    async def on_startup(cls):
        ...

    @classmethod
    async def on_shutdown(cls):
        ...
