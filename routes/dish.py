from uuid import UUID

from fastapi import APIRouter, Depends

from repositories.dish import DishRepository
from schemas.dish import DishChange, DishShow

router = APIRouter()
DISH = Depends(DishRepository)


@router.get(
    '/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
    response_model=list[DishShow])
def get_dishes(submenu_id: UUID, dish=DISH):
    return dish.get_all(submenu_id)


@router.post('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
             status_code=201)
def create_dish(submenu_id: UUID,
                dish_data: DishChange,
                dish=DISH):
    return dish.create(submenu_id, dish_data)


@router.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
def get_dish(dish_id: UUID,
             submenu_id: UUID,
             dish=DISH):
    return dish.get_by_id(submenu_id, dish_id)


@router.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
def update_dish(dish_id: UUID,
                submenu_id: UUID,
                dish_data: DishChange,
                dish=DISH):
    return dish.update(submenu_id, dish_id, dish_data)


@router.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
def delete_submenu(submenu_id: str,
                   dish_id: str,
                   dish=DISH):
    return dish.delete(submenu_id, dish_id)
