from pydantic import BaseModel
from pydantic import StrictStr
from datetime import datetime

from integra_python_connect.src.dto.views.connector_view import ConnectorView
from integra_python_connect.src.dto.views.processor_view import ProcessorView


class ExternalServiceConfigResponse(BaseModel):
    serviceName: StrictStr | None = ""
    serviceAddress: StrictStr | None = ""
    applicationStartDate: datetime | None = None
    connectorViews: list[ConnectorView] | None = []
    processorViews: list[ProcessorView] | None = []
    manualFileName: StrictStr | None = ""
