from fastapi import APIRouter
from routes.schemas.dish import Dish, DishCreate

router = APIRouter


@router.get('/menus/')
async def get_dishes(args: Dish):
    return []


@router.put('/menus/')
async def create_dish(args: DishCreate):
    return []


@router.patch('/menus/<menu_id>')
async def update_dish(args: Dish):
    return []


@router.delete('/menus/<menu_id>')
async def delete_dish(args: Dish):
    return []
