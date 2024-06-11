from fastapi import APIRouter

from integra_python_connector import SETTINGS
from integra_python_connector import configuration_router
from integra_python_connector import processor_router

base_router = APIRouter(prefix=SETTINGS.API_PREFIX)

base_router.include_router(configuration_router)
base_router.include_router(processor_router)
