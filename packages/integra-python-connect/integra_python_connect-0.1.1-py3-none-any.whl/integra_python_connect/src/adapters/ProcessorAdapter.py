from abc import ABC, abstractmethod


class ProcessorAdapter(ABC):
    _instances = set()

    def __init__(self, service_name: str = "", service_address: str = ""):
        self.__service_name = service_name
        self.__service_address = service_address
        self.__processor_view = None
        ProcessorAdapter.add_processor_adapter(self)

    def __del__(self):
        ProcessorAdapter.remove_processor_adapter(self)

    @abstractmethod
    async def execute(self, exchange: str = None):
        ...

    @abstractmethod
    async def validate(self, exchange: str = None):
        ...

    @abstractmethod
    async def get_processor_view(self):
        ...

    @classmethod
    def get_processor_adapters(cls) -> list:
        return cls._instances

    @classmethod
    def add_processor_adapter(cls, service):
        cls._instances.add(service)

    @classmethod
    def remove_processor_adapter(cls, service):
        cls._instances.remove(service)

    def register(self):
        ProcessorAdapter.add_processor_adapter(self)

    @property
    def serve_name(self):
        return self.__service_name

    @property
    def serve_address(self):
        return self.__service_address
