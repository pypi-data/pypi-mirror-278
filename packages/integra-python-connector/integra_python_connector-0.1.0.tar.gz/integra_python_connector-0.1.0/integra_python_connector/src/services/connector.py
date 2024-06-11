from integra_python_connector import ExternalService


class Connector(ExternalService):
    def __init__(self):
        super().__init__()

    async def execute(self):
        return 'Hello World'
