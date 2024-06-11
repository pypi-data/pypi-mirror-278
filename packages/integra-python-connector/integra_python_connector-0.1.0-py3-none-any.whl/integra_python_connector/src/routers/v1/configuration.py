
from fastapi.responses import JSONResponse

from integra_python_connector import APIRouter
from integra_python_connector import dm
from integra_python_connector import ExternalServiceConfigResponse
from integra_python_connector import ProcessorAdapter

configuration_router = APIRouter(prefix='/configuration', tags=["Работа с конфигурациями внешних сервисов"])


@configuration_router.get(
    path='/',
    response_model=ExternalServiceConfigResponse
)
async def get_configurations():
    # Получаем список всех сервисов
    # Для каждого сервиса получаем все обработчики и коннекторы этого сервиса их view и skeletons
    # Получаем файл .pdf сервиса
    # Возвращаем ответ с получившейся структурой

    processors = ProcessorAdapter.get_processor_adapters()
    proc_views = []
    for proc in processors:
        proc_view = await proc.get_processor_view()
        proc_views.append(proc_view)

    response = ExternalServiceConfigResponse(
        serviceName="",
        serviceAddress="",
        applicationStartDate=dm.get_application_start_date(),
        processorViews=proc_views,
        manualFileName=""
    )
    print(response)
    return response


@configuration_router.get(
    path='/user'
)
async def get_configurations():
    return JSONResponse('user')


@configuration_router.get(
    path='/manual'
)
async def get_configurations():
    return JSONResponse('manual')
