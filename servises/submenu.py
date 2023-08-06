from uuid import UUID

from fastapi import Depends

from models.submenu import SubMenu
from repositories.submenu import SubMenuRepository
from schemas.submenu import SubMenuChange, SubMenuShow

from .cache import MENU_CACHE_NAME, SUBMENU_CACHE_NAME, CacheRepository


class SubMenuService:
    def __init__(self, submenu_repository=Depends(SubMenuRepository)):
        self.submenu_repository = submenu_repository
        self.cache_name = SUBMENU_CACHE_NAME
        self._redis = CacheRepository().get_redis()

    def create(self, menu_id, submenu_data: SubMenuChange) -> SubMenu:
        new_submenu = self.submenu_repository.create(menu_id, submenu_data)
        self._redis.set(
            f'{MENU_CACHE_NAME}{menu_id}{self.cache_name}{new_submenu.id}',
            new_submenu)
        self._redis.delete(MENU_CACHE_NAME)
        return new_submenu

    def update(self, menu_id: UUID,
               submenu_id: UUID,
               submenu_data: SubMenuChange) -> SubMenu:
        update_submenu = self.submenu_repository.update(menu_id,
                                                        submenu_id,
                                                        submenu_data)
        self._redis.set(
            f'{MENU_CACHE_NAME}{menu_id}{self.cache_name}{submenu_id}',
            update_submenu)
        self._redis.delete(MENU_CACHE_NAME)
        return update_submenu

    def get_all(self, munu_id: UUID) -> list[SubMenuShow]:
        key_submenus = f'{MENU_CACHE_NAME}{munu_id}{self.cache_name}'
        if self._redis.exists(key_submenus):
            self._redis.get(key_submenus)
        submenus = self.submenu_repository.get_all(munu_id)
        self._redis.set(key_submenus, submenus)
        return submenus

    def get_by_id(self, menu_id: UUID, submenu_id: UUID) -> SubMenu:
        key_submenu = f'{MENU_CACHE_NAME}{menu_id}{self.cache_name}{submenu_id}'
        if self._redis.exists(key_submenu):
            return self._redis.get(key_submenu)
        submenu = self.submenu_repository.get_by_id(menu_id, submenu_id)
        self._redis.set(key_submenu, submenu)
        return submenu

    def delete(self, menu_id: UUID, submenu_id: UUID) -> None:
        self.submenu_repository.delete(menu_id, submenu_id)
        self._redis.del_all()
