from uuid import UUID

from fastapi import APIRouter, Depends, status

from schemas.dish import BaseDish, DishChange, DishCreate, DishShow
from services.dish import DishService

router = APIRouter()
DISH = Depends(DishService)


@router.get(
    '/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
    response_model=list[DishShow])
def get_dishes(menu_id: UUID, submenu_id: UUID, dish=DISH) -> list[DishShow]:
    return dish.get_all(menu_id, submenu_id)


@router.post('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
             status_code=status.HTTP_201_CREATED)
def create_dish(menu_id: UUID,
                submenu_id: UUID,
                dish_data: DishChange,
                dish=DISH) -> DishCreate:
    return dish.create(menu_id, submenu_id, dish_data)


@router.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
def get_dish(menu_id: UUID,
             submenu_id: UUID,
             dish_id: UUID,
             dish=DISH) -> DishShow:
    return dish.get_by_id(menu_id, submenu_id, dish_id)


@router.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
def update_dish(menu_id: UUID,
                submenu_id: UUID,
                dish_id: UUID,
                dish_data: DishChange,
                dish=DISH) -> BaseDish:
    return dish.update(menu_id, submenu_id, dish_id, dish_data)


@router.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
def delete_submenu(menu_id: UUID,
                   submenu_id: UUID,
                   dish_id: UUID,
                   dish=DISH) -> None:
    return dish.delete(menu_id, submenu_id, dish_id)
