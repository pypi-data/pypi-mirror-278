from abc import ABC, abstractmethod


class ProcessorAdapter(ABC):
    _instances = set()

    def __init__(self, processor_title: str = "", processor_description: str = ""):
        self.__processor_title = processor_title
        self.__processor_description = processor_description
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
        return list(cls._instances)

    @classmethod
    def add_processor_adapter(cls, service):
        cls._instances.add(service)

    @classmethod
    def remove_processor_adapter(cls, service):
        cls._instances.remove(service)

    @property
    def processor_title(self):
        return self.__processor_title

    @property
    def processor_description(self):
        return self.__processor_description
