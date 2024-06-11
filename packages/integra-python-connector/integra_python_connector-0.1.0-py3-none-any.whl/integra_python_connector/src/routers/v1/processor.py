from typing import Annotated

from fastapi import APIRouter, Request, Query
from integra_python_connector import ProcessorHandler

processor_router = APIRouter(prefix="/processor", tags=["Процессоры"])


@processor_router.post(
    path='/execute'
)
async def execute(
        request: Request,
        processor_title: Annotated[str, Query(...)]
):
    try:
        exchange = await request.json()
    except Exception as e:
        # raise HTTPException(status_code=500, detail=str(e))
        exchange = {1: 2}
    return await ProcessorHandler.execute(exchange=exchange, processor_title=processor_title)



@processor_router.post(
    path='/validate'
)
async def validate(request: Request, processor_title: str):
    try:
        exchange = await request.json()
    except Exception as e:
        # raise HTTPException(status_code=500, detail=str(e))
        exchange = {1: 2}
    result = await ProcessorHandler.validate(exchange=exchange, processor_title=processor_title)
    return result
