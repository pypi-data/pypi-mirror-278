from pydantic import BaseModel, StrictStr

from integra_python_connect.src.dto.skeletons.processor import SkeletonProcessor


class ProcessorView(BaseModel):
    processorTitle: StrictStr | None = ""
    processorDescription: StrictStr | None = ""
    skeletonProcessor: SkeletonProcessor
