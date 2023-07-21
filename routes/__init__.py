from fastapi import FastAPI, APIRouter

from .menus import router as menu_router

app = FastAPI()

app.include_router(menu_router)
