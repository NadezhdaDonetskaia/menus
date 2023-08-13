from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from schemas.dish import BaseDish, DishShow
from services.dish import DishService

router = APIRouter(
    prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
    tags=['Dishes']
)
DISH = Depends(DishService)


@router.get(
    '',
    response_model=list[DishShow])
async def get_dishes(menu_id: UUID,
                     submenu_id: UUID,
                     dish=DISH) -> list[DishShow]:
    return await dish.get_all(menu_id, submenu_id)


@router.post('',
             status_code=status.HTTP_201_CREATED)
async def create_dish(menu_id: UUID,
                      submenu_id: UUID,
                      dish_data: BaseDish,
                      dish=DISH) -> DishShow:
    return await dish.create(menu_id, submenu_id, dish_data)


@router.get('/{dish_id}')
async def get_dish(menu_id: UUID,
                   submenu_id: UUID,
                   dish_id: UUID,
                   dish=DISH) -> DishShow:
    return await dish.get_by_id(menu_id, submenu_id, dish_id)


@router.patch('/{dish_id}')
async def update_dish(menu_id: UUID,
                      submenu_id: UUID,
                      dish_id: UUID,
                      dish_data: BaseDish,
                      dish=DISH) -> DishShow:
    return await dish.update(menu_id, submenu_id, dish_id, dish_data)


@router.delete('/{dish_id}')
async def delete_submenu(menu_id: UUID,
                         submenu_id: UUID,
                         dish_id: UUID,
                         dish=DISH) -> JSONResponse:
    return await dish.delete(menu_id, submenu_id, dish_id)
