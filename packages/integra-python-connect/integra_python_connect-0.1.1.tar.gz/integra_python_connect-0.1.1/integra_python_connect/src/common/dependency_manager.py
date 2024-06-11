from dataclasses import dataclass
from datetime import datetime, UTC

from integra_python_connect.src.services.external_service import ExternalService


@dataclass
class DependencyManager:
    def __init__(self):
        self.__services = []
        self.__application_start_date = datetime.now(UTC)

    def get_application_start_date(self) -> datetime:
        return self.__application_start_date

    @property
    def services(self) -> list[ExternalService]:
        return self.__services


dm = DependencyManager()
