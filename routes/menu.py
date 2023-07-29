from fastapi import APIRouter, HTTPException
import uuid
from ..database import get_connection
from .schemas.menu import Menu, MenuCreate

router = APIRouter()


@router.get('/api/v1/menus')
async def get_menus():
    query = """
        SELECT * FROM menus
    """
    async with get_connection() as conn:
        return await conn.fetch(query)


@router.post('/api/v1/menus', status_code=201)
async def create_menu(args: MenuCreate):
    query = """
        INSERT INTO menus(id, title, description)
        VALUES ($1, $2, $3)
    """
    async with get_connection() as conn:
        await conn.fetch(
            query,
            uuid.uuid4(),
            args.title,
            args.description
            )
        query_get = """
            SELECT * FROM menus WHERE title=$1
        """
        response = await conn.fetch(query_get, args.title)
        return response[0]


@router.get("/api/v1/menus/{menu_id}")
async def get_menu(menu_id: str):
    query = """
        SELECT * FROM menus WHERE id=$1
    """
    async with get_connection() as conn:
        response = await conn.fetch(query, menu_id)
        if not response:
            raise HTTPException(status_code=404, detail="menu not found")
        return response[0]


@router.patch("/api/v1/menus/{menu_id}")
async def update_menu(menu_id: str, args: Menu):
    query = """
        UPDATE menus
        SET title=$1, description=$2
        WHERE id=$3
    """
    async with get_connection() as conn:
        response = await conn.fetch(query,
                                    args.title,
                                    args.description,
                                    menu_id)
        query_get = """
            SELECT * FROM menus WHERE id=$1
        """
        response = await conn.fetch(query_get, menu_id)
        return response[0]


@router.delete("/api/v1/menus/{menu_id}")
async def delete_menu(menu_id: str):
    query = """
        DELETE FROM menus
        WHERE id=$1
    """
    async with get_connection() as conn:
        return await conn.fetch(query, menu_id)
