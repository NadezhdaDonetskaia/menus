import uuid
from fastapi import APIRouter, HTTPException
from app.database import get_connection
from .schemas.dish import Dish, DishCreate

router = APIRouter()


@router.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
async def get_dishes(submenu_id: str):
    query = """
        SELECT * FROM dishes
        WHERE submenu_id=$1
    """
    async with get_connection() as conn:
        return await conn.fetch(query, submenu_id)


@router.post('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', status_code=201)
async def create_dish(submenu_id: str, args: DishCreate):
    query = """
        INSERT INTO dishes(id, submenu_id, title, description, price)
        VALUES ($1, $2, $3, $4, $5)
    """
    async with get_connection() as conn:
        await conn.fetch(
            query,
            uuid.uuid4(),
            submenu_id,
            args.title,
            args.description,
            # f'{args.price:.2f}'
            f'{args.price}'
            )
        query_get = """
            SELECT * FROM dishes WHERE title=$1
        """
        response = await conn.fetch(query_get, args.title)
        return response[0]


@router.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
async def get_dish(dish_id: str):
    query = """
        SELECT * FROM dishes WHERE id=$1
    """
    async with get_connection() as conn:
        response = await conn.fetch(query, dish_id)
        if not response:
            raise HTTPException(status_code=404, detail="dish not found")
        return response[0]


@router.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
async def update_dish(dish_id: str, args: Dish):
    query = """
        UPDATE dishes
        SET title=$1, description=$2, price=$3
        WHERE id=$4
    """
    async with get_connection() as conn:
        response = await conn.fetch(query,
                                    args.title,
                                    args.description,
                                    args.price,
                                    dish_id)
        query_get = """
            SELECT * FROM dishes WHERE id=$1
        """
        response = await conn.fetch(query_get, dish_id)
        return response[0]


@router.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
async def delete_submenu(dish_id: str):
    query = """
        DELETE FROM dishes
        WHERE id=$1
    """
    async with get_connection() as conn:
        return await conn.fetch(query, dish_id)
