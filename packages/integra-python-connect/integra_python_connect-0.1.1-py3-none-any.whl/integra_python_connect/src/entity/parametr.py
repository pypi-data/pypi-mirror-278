from enum import Enum
from typing import Any

from pydantic import BaseModel, StrictStr

from integra_python_connect.src.common.enums import ParameterType


class Parameter(BaseModel):
    name: StrictStr
    label: StrictStr | None = None
    # Стиль элемента, где рендерятся внутренние элементы
    childrenBoxStyle: dict[str, Any] | None = None
    # Стиль элемента
    style: dict[str, Any] | None = None
    # Стиль контейнера, где находится элемент
    boxStyle: dict[str, dict] | None = None
    props: dict[str, dict] | None = None

    description: StrictStr | None = None
    defaultValue: StrictStr | None = None
    # Для настроек, текущее значение
    value: StrictStr | None = None

    # list of Parameter
    parameterList: list[Any] | None = None

    defaultOption: StrictStr | None = None
    options: list[str] | None = None
    objectOptions: list[Any] | None = None

    bottomText: StrictStr | None = None
    isAddValue: bool

    isChange: bool = True
    isRequired: bool = False
    isVisible: bool = True
    isDisabled: bool = False
    isExternal: bool = False
    type: Enum = ParameterType.TextField
