from uuid import UUID

from fastapi import Depends

from repositories.menu import MenuRepository
from schemas.menu import BaseMenu, MenuChange, MenuCreate, MenuShow

from .cache import MENU_CACHE_NAME, CacheRepositoryMenu


class MenuService:
    def __init__(self, menu_repository=Depends(MenuRepository)):
        self.menu_repository = menu_repository
        self._redis = CacheRepositoryMenu()
        self.key = MENU_CACHE_NAME

    def create(self, menu_data: MenuChange) -> MenuCreate:
        new_menu = self.menu_repository.create(menu_data)
        self._redis.create_update(menu_id=new_menu.id, menu_data=new_menu)
        return new_menu

    def update(self, menu_id: UUID,
               menu_data: MenuChange) -> BaseMenu:
        update_menu = self.menu_repository.update(menu_id, menu_data)
        self._redis.create_update(menu_id=menu_id, menu_data=update_menu)
        return update_menu

    def get_all(self) -> list[MenuShow]:
        if self._redis.exists(self.key):
            return self._redis.get(self.key)
        menus = self.menu_repository.get_all()
        self._redis.set(self.key, menus)
        return menus

    def get_by_id(self, menu_id: UUID) -> MenuShow:
        if self._redis.exists(f'{self.key}{menu_id}'):
            return self._redis.get(f'{self.key}{menu_id}')
        menu = self.menu_repository.get_by_id(menu_id)
        self._redis.set(f'{self.key}{menu_id}', menu)
        return menu

    def delete(self, menu_id: UUID) -> None:
        self.menu_repository.delete(menu_id)
        self._redis.delete(menu_id=menu_id)
