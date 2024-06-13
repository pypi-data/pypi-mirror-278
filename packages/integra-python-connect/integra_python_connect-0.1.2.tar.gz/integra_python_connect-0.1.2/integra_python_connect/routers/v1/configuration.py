from fastapi.responses import JSONResponse, FileResponse
from integra_python_connect.api_router import APIRouter
from integra_python_connect.dto.responces.external_service import ExternalServiceConfigResponse
from integra_python_connect.adapters.ProcessorAdapter import ProcessorAdapter
from integra_python_connect.common.dependency_manager import dm
import os

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
        serviceName=dm.title,
        serviceAddress=dm.address,
        applicationStartDate=dm.application_start_date,
        processorViews=proc_views,
        manualFileName=""
    )
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
    manual_path = dm.manual_path
    print(manual_path)
    if os.path.exists(manual_path):
        return FileResponse(manual_path, media_type='application/octet-stream', filename=os.path.basename(manual_path))
    else:
        return {"error": "File not found"}

