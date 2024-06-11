from integra_python_connect.src.adapters.ProcessorAdapter import ProcessorAdapter
from fastapi import HTTPException


class ProcessorHandler:
    @classmethod
    async def execute(cls, exchange, processor_title: str):
        processor_adapter = await cls.get_processor_by_processor_title(processor_title)
        return await processor_adapter.execute(exchange)

    @classmethod
    async def validate(cls, processor, processor_title: str):
        processor_validation = await cls.get_processor_by_processor_title(processor_title)
        return await processor_validation.processor_validation(processor)

    @classmethod
    async def get_processor_by_processor_title(cls, processor_title: str) -> ProcessorAdapter:
        for processor_adapter in ProcessorAdapter.get_processor_adapters():
            processor_view = await processor_adapter.get_processor_view()
            if processor_view.processor_title == processor_title:
                return processor_adapter
        raise HTTPException(status_code=404, detail=f'Processor not found: {processor_title} ')
