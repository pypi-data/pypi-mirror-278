import uuid

from pydantic import BaseModel, UUID4, Field, StrictStr

from integra_python_connector import SkeletonConnector


class ConnectorView(BaseModel):
    connector_id: UUID4 = Field(default_factory=uuid.uuid4)
    connector_title: StrictStr
    input_connector_desctiption: StrictStr | None = None
    output_connector_desctiption: StrictStr | None = None
    skeleton_input_connector: SkeletonConnector | None = None
    skeleton_output_connector: SkeletonConnector | None = None
