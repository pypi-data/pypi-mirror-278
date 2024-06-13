from fastapi import APIRouter

from integra_python_connect.common.settings import SETTINGS
from integra_python_connect.routers.v1.configuration import configuration_router
from integra_python_connect.routers.v1.processor import processor_router

base_router = APIRouter(prefix=SETTINGS.API_PREFIX)

base_router.include_router(configuration_router)
base_router.include_router(processor_router)
