
from pydantic import BaseModel

from integra_python_connect.src.entity.parametr import Parameter


class SkeletonProcessor(BaseModel):
    typeProcessor: str
    parameterList: list[Parameter] = []
    queryParameterList: list[Parameter] = []
    stepToStepList: list = []
