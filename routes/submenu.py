from fastapi import APIRouter
from routes.schemas.submenu import SubMenu, SubMenuCreate, SubMenuDetail

router = APIRouter


@router.get('/menus/')
async def get_sub_menus(args: SubMenuDetail):
    return []


@router.put('/menus/')
async def create_submenu(args: SubMenuCreate):
    return []


@router.patch('/menus/<menu_id>')
async def update_submenu(args: SubMenu):
    return []


@router.delete('/menus/<menu_id>')
async def delete_submenu(args: SubMenu):
    return []
