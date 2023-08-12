import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ValidationException
from fastapi.responses import JSONResponse

from routes import dish_router, menu_router, sub_menu_router
from services.cache import CacheRepository

app = FastAPI(
    title='Menus App'
)


@app.exception_handler(ValidationException)
async def validation_exeption_handler(request: Request, exc: ValidationException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({'detail': exc.errors})
    )


app.include_router(menu_router)
app.include_router(sub_menu_router)
app.include_router(dish_router)
app.add_event_handler('shutdown', CacheRepository().del_all)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
