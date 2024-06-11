from fastapi import APIRouter

from integra_python_connect.src.common.settings import SETTINGS
from integra_python_connect.src.routers.v1.configuration import configuration_router
from integra_python_connect.src.routers.v1.processor import processor_router

base_router = APIRouter(prefix=SETTINGS.API_PREFIX)

base_router.include_router(configuration_router)
base_router.include_router(processor_router)
