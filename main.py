import uvicorn
from fastapi import FastAPI

from database import BaseDBModel, engine
from routes import dish_router, menu_router, sub_menu_router
from services.cache import CacheRepository

BaseDBModel.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(menu_router)
app.include_router(sub_menu_router)
app.include_router(dish_router)
app.add_event_handler('shutdown', CacheRepository().del_all)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
