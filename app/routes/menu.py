from fastapi import APIRouter

from app.database import get_connection
from .schemas.menu import Menu, MenuCreate, MenuDetail

router = APIRouter()


@router.get('/api/v1/menus')
async def get_menus(args: MenuDetail):
    query = """
        SELECT * FROM menus
    """
    async with get_connection() as conn:
        return await conn.fetch(query)


@router.post('/api/v1/menus')
async def create_menu(args: MenuCreate):
    query = """
        INSERT INTO menus(title, dicsription)
        VALUES ($1, $2)
    """
    async with get_connection() as conn:
        return await conn.fetch(
            query,
            args.title,
            args.description
            )


@router.patch('/api/v1/menus/<menu_id>')
async def update_menu(menu_id: int, args: Menu):
    return []


@router.delete('/api/v1/menus/<menu_id>')
async def delete_menu(menu_id: int, args: Menu):
    return []
