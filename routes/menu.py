from fastapi import APIRouter
from routes.schemas.menu import Menu, MenuCreate

router = APIRouter


@router.get('/menus/')
async def get_menus(args: Menu):
    return []


@router.put('/menus/')
async def create_menu(args: MenuCreate):
    return []


@router.patch('/menus/<menu_id>')
async def update_menu(args: Menu):
    return []


@router.delete('/menus/<menu_id>')
async def delete_menu(args: Menu):
    return []
