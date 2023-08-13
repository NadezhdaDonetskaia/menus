from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from services.all import AllService

router = APIRouter(
    prefix='/api/v1',
    tags=['All']
)
ALL = Depends(AllService)


@router.get('/',
            name='show_all')
async def get_all(all=ALL) -> JSONResponse:
    return await all.get_all()
