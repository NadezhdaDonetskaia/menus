from uuid import UUID

from fastapi import APIRouter, Depends, status

from schemas.menu import MenuChange, MenuShow
from servises.menu import MenuService

router = APIRouter()
MENU = Depends(MenuService)


@router.get('/api/v1/menus', response_model=list[MenuShow],
            name='show_menus')
def get_menus(menu=MENU):
    return menu.get_all()


@router.post('/api/v1/menus',
             status_code=status.HTTP_201_CREATED)
def create_menu(menu_data: MenuChange, menu=MENU):
    return menu.create(menu_data)


@router.get('/api/v1/menus/{menu_id}')
def get_menu(menu_id: UUID, menu=MENU):
    return menu.get_by_id(menu_id)


@router.patch('/api/v1/menus/{menu_id}')
def update_menu(menu_id: UUID,
                menu_data: MenuChange,
                menu=MENU):
    return menu.update(menu_id, menu_data)


@router.delete('/api/v1/menus/{menu_id}')
def delete_menu(menu_id: UUID, menu=MENU):
    return menu.delete(menu_id)
