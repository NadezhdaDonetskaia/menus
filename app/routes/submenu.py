import uuid
from fastapi import APIRouter, HTTPException
from app.database import get_connection
from .schemas.submenu import SubMenu, SubMenuCreate

router = APIRouter()


@router.get('/api/v1/menus/{menu_id}/submenus')
async def get_sub_menus(menu_id: str):
    query = """
        SELECT * FROM submenus
        WHERE menu_id=$1
    """
    async with get_connection() as conn:
        return await conn.fetch(query, menu_id)


@router.post('/api/v1/menus/{menu_id}/submenus')
async def create_submenu(menu_id: str, args: SubMenuCreate):
    query = """
        INSERT INTO submenus(id, menu_id, title, description)
        VALUES ($1, $2, $3, $4)
    """
    async with get_connection() as conn:
        await conn.fetch(
            query,
            uuid.uuid4(),
            menu_id,
            args.title,
            args.description
            )
        query_get = """
            SELECT * FROM submenus WHERE title=$1
        """
        response = await conn.fetch(query_get, args.title)
        return response[0]


@router.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
async def get_submenu(submenu_id: str):
    query = """
        SELECT * FROM submenus WHERE id=$1
    """
    async with get_connection() as conn:
        response = await conn.fetch(query, submenu_id)
        if not response:
            raise HTTPException(status_code=404, detail="submenu not found")
        return response[0]


@router.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
async def update_submenu(submenu_id: str, args: SubMenu):
    query = """
        UPDATE submenus
        SET title=$1, description=$2
        WHERE id=$3
    """
    async with get_connection() as conn:
        response = await conn.fetch(query,
                                    args.title,
                                    args.description,
                                    submenu_id)
        query_get = """
            SELECT * FROM submenus WHERE id=$1
        """
        response = await conn.fetch(query_get, submenu_id)
        return response[0]


@router.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
async def delete_submenu(submenu_id: str):
    query = """
        DELETE FROM submenus
        WHERE id=$1
    """
    async with get_connection() as conn:
        return await conn.fetch(query, submenu_id)
