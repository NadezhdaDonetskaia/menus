from uuid import UUID

from fastapi import Depends

from repositories.submenu import SubMenuRepository
from schemas.submenu import BaseSubMenu, SubMenuChange, SubMenuCreate, SubMenuShow

from .cache import MENU_CACHE_NAME, SUBMENU_CACHE_NAME, CacheRepositorySubMenu


class SubMenuService:
    def __init__(self, submenu_repository=Depends(SubMenuRepository)):
        self.submenu_repository = submenu_repository
        self._redis = CacheRepositorySubMenu()

    def create(self, menu_id: UUID, submenu_data: SubMenuChange) -> SubMenuCreate:
        new_submenu = self.submenu_repository.create(menu_id, submenu_data)
        self._redis.create_update(menu_id=menu_id,
                                  submenu_id=new_submenu.id,
                                  data=new_submenu)
        return new_submenu

    def update(self, menu_id: UUID,
               submenu_id: UUID,
               submenu_data: SubMenuChange) -> BaseSubMenu:
        update_submenu = self.submenu_repository.update(menu_id,
                                                        submenu_id,
                                                        submenu_data)
        self._redis.create_update(menu_id=menu_id,
                                  submenu_id=submenu_id,
                                  data=update_submenu)
        return update_submenu

    def get_all(self, menu_id: UUID) -> list[SubMenuShow]:
        key_submenus = f'{MENU_CACHE_NAME}{menu_id}{SUBMENU_CACHE_NAME}'
        if self._redis.exists(key_submenus):
            return self._redis.get(key_submenus)
        submenus = self.submenu_repository.get_all(menu_id)
        self._redis.set(key=key_submenus, data=submenus)
        return submenus

    def get_by_id(self, menu_id: UUID, submenu_id: UUID) -> SubMenuShow:
        key_submenu = f'{MENU_CACHE_NAME}{menu_id}' \
                      f'{SUBMENU_CACHE_NAME}{submenu_id}'
        if self._redis.exists(key_submenu):
            return self._redis.get(key_submenu)
        submenu = self.submenu_repository.get_by_id(menu_id, submenu_id)
        self._redis.set(key=key_submenu, data=submenu)
        return submenu

    def delete(self, menu_id: UUID, submenu_id: UUID) -> None:
        self.submenu_repository.delete(menu_id, submenu_id)
        self._redis.delete(menu_id=menu_id, submenu_id=submenu_id)
