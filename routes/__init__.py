from fastapi import FastAPI

from .menu import router as menu_router
from .submenu import router as sub_menu_router

app = FastAPI()

app.include_router(menu_router)
app.include_router(sub_menu_router)
