from uuid import UUID

from fastapi import APIRouter, Depends, status

from schemas.submenu import BaseSubMenu, SubMenuChange, SubMenuShow
from servises.submenu import SubMenuService

router = APIRouter()
SUBMENU = Depends(SubMenuService)


@router.get(
    '/api/v1/menus/{menu_id}/submenus',
    response_model=list[SubMenuShow],
    name='get_submenus'
)
def get_submenus(menu_id: UUID, submenu=SUBMENU) -> list[SubMenuShow]:
    return submenu.get_all(menu_id)


@router.post('/api/v1/menus/{menu_id}/submenus',
             status_code=status.HTTP_201_CREATED,
             name='create_submenu')
def create_submenu(menu_id: UUID,
                   submenu_data: SubMenuChange,
                   submenu=SUBMENU) -> BaseSubMenu:
    return submenu.create(menu_id, submenu_data)


@router.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}',
            name='get_submenu')
def get_submenu(submenu_id: UUID,
                menu_id: UUID,
                submenu=SUBMENU) -> BaseSubMenu:
    return submenu.get_by_id(menu_id, submenu_id)


@router.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}',
              name='update_submenu')
def update_submenu(submenu_id: str,
                   menu_id: str,
                   submenu_data: SubMenuChange,
                   submenu=SUBMENU) -> BaseSubMenu:
    return submenu.update(menu_id, submenu_id, submenu_data)


@router.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}',
               name='update_submenu')
def delete_submenu(menu_id: str, submenu_id: str, submenu=SUBMENU) -> None:
    return submenu.delete(menu_id, submenu_id)
