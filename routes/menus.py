from fastapi import APIRouter
from routes.schemas.menu import 

router = APIRouter


@router.get('/menus/')
async def get_menus():
    return []


@router.update('/menus/<menu_id>')
async def update_menu(args: Menu):
    return []