from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from schemas.submenu import BaseSubMenu, SubMenuShow
from services.submenu import SubMenuService

router = APIRouter(
    prefix='/api/v1/menus/{menu_id}/submenus',
    tags=['Submenus']
)
SUBMENU = Depends(SubMenuService)


@router.get(
    '',
    response_model=list[SubMenuShow],
    name='get_submenus'
)
async def get_submenus(menu_id: UUID, submenu=SUBMENU) -> list[SubMenuShow]:
    return await submenu.get_all(menu_id)


@router.post('',
             status_code=status.HTTP_201_CREATED,
             name='create_submenu')
async def create_submenu(menu_id: UUID,
                         submenu_data: BaseSubMenu,
                         submenu=SUBMENU) -> SubMenuShow:
    return await submenu.create(menu_id, submenu_data)


@router.get('/{submenu_id}',
            name='get_submenu')
async def get_submenu(submenu_id: UUID,
                      menu_id: UUID,
                      submenu=SUBMENU) -> SubMenuShow:
    return await submenu.get_by_id(menu_id, submenu_id)


@router.patch('/{submenu_id}',
              name='update_submenu')
async def update_submenu(submenu_id: UUID,
                         menu_id: UUID,
                         submenu_data: BaseSubMenu,
                         submenu=SUBMENU) -> BaseSubMenu:
    return await submenu.update(menu_id, submenu_id, submenu_data)


@router.delete('/{submenu_id}',
               name='update_submenu')
async def delete_submenu(menu_id: UUID,
                         submenu_id: UUID,
                         submenu=SUBMENU) -> JSONResponse:
    return await submenu.delete(menu_id, submenu_id)
