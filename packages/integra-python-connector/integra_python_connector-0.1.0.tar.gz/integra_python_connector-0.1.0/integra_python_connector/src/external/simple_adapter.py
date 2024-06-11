from integra_python_connector import ProcessorAdapter
from integra_python_connector import SkeletonProcessor
from integra_python_connector import ProcessorView


class SimpleService(ProcessorAdapter):
    async def execute(self, exchange: str = None):
        return "EXECUTED!"

    async def get_processor_view(self) -> ProcessorView:
        skeleton = SkeletonProcessor(typeProcessor='Example type')

        self.processor_view = ProcessorView(
            processorTitle='Test processor',
            processorDescription='Нужен чтобы протестить сервис',
            skeletonProcessor=skeleton
        )
        return self.processor_view

    async def validate(self, exchange: str = None):
        return "VALIDATED!"
