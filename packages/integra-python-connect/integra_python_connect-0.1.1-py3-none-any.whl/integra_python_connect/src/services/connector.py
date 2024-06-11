from integra_python_connect.src.services.external_service import ExternalService


class Connector(ExternalService):
    def __init__(self):
        super().__init__()

    async def execute(self):
        return 'Hello World'
