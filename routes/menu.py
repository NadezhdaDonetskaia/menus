from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from schemas.menu import BaseMenu, MenuShow
from services.menu import MenuService

router = APIRouter(
    prefix='/api/v1/menus',
    tags=['Menus']
)
MENU = Depends(MenuService)


@router.get('', response_model=list[MenuShow],
            name='show_menus')
async def get_menus(menu=MENU) -> list[MenuShow]:
    return await menu.get_all()


@router.post('',
             status_code=status.HTTP_201_CREATED,
             name='create_menu')
async def create_menu(menu_data: BaseMenu, menu=MENU) -> MenuShow:
    new_menu = await menu.create(menu_data)
    return new_menu


@router.get('/{menu_id}',
            name='get_menu')
async def get_menu(menu_id: UUID, menu=MENU) -> MenuShow:
    return await menu.get_by_id(menu_id)


@router.patch('/{menu_id}',
              name='update_menu')
async def update_menu(menu_id: UUID,
                      menu_data: BaseMenu,
                      menu=MENU) -> MenuShow:
    return await menu.update(menu_id, menu_data)


@router.delete('/{menu_id}',
               name='delete_menu')
async def delete_menu(menu_id: UUID, menu=MENU) -> JSONResponse:
    return await menu.delete(menu_id)
