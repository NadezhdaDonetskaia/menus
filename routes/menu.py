from fastapi import APIRouter
from routes.schemas.menu import Menu, MenuCreate, MenuDetail

router = APIRouter


@router.get('/api/v1/menus/')
async def get_menus(args: MenuDetail):
    return []


@router.post('/api/v1/menus/')
async def create_menu(args: MenuCreate):
    return []


@router.patch('/api/v1/menus/<menu_id>')
async def update_menu(menu_id: int, args: Menu):
    return []


@router.delete('/api/v1/menus/<menu_id>')
async def delete_menu(menu_id: int, args: Menu):
    return []
