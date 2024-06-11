from pydantic import BaseModel, StrictStr

from integra_python_connector import SkeletonProcessor


class ProcessorView(BaseModel):
    processorTitle: StrictStr | None = ""
    processorDescription: StrictStr | None = ""
    skeletonProcessor: SkeletonProcessor
