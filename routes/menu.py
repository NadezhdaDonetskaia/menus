from uuid import UUID

from fastapi import APIRouter, Depends, status

from schemas.menu import BaseMenu, MenuChange, MenuCreate, MenuShow
from servises.menu import MenuService

router = APIRouter()
MENU = Depends(MenuService)


@router.get('/api/v1/menus', response_model=list[MenuShow],
            name='show_menus')
def get_menus(menu=MENU) -> list[MenuShow]:
    return menu.get_all()


@router.post('/api/v1/menus',
             status_code=status.HTTP_201_CREATED,
             name='create_menu')
def create_menu(menu_data: MenuChange, menu=MENU) -> MenuCreate:
    return menu.create(menu_data)


@router.get('/api/v1/menus/{menu_id}',
            name='get_menu')
def get_menu(menu_id: UUID, menu=MENU) -> MenuShow:
    return menu.get_by_id(menu_id)


@router.patch('/api/v1/menus/{menu_id}',
              name='update_menu')
def update_menu(menu_id: UUID,
                menu_data: MenuChange,
                menu=MENU) -> BaseMenu:
    return menu.update(menu_id, menu_data)


@router.delete('/api/v1/menus/{menu_id}',
               name='delete_menu')
def delete_menu(menu_id: UUID, menu=MENU) -> None:
    return menu.delete(menu_id)
