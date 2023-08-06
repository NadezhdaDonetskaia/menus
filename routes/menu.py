from uuid import UUID

from fastapi import APIRouter, Depends

from repositories.menu import MenuRepository
from schemas.menu import MenuChange, MenuShow

router = APIRouter()
MENU = Depends(MenuRepository)


@router.get('/api/v1/menus', response_model=list[MenuShow])
def get_menus(menu=MENU):
    return menu.get_all()


@router.post('/api/v1/menus', status_code=201)
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
