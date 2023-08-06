from uuid import UUID

from fastapi import Depends

from models.menu import Menu
from repositories.menu import MenuRepository
from schemas.menu import MenuChange, MenuShow

from .cache import MENU_CACHE_NAME, CacheRepository


class MenuService:
    def __init__(self, menu_repository=Depends(MenuRepository)):
        self.menu_repository = menu_repository
        self.cache_name = MENU_CACHE_NAME
        self._redis = CacheRepository().get_redis()

    def create(self, menu_data: MenuChange) -> Menu:
        new_menu = self.menu_repository.create(menu_data)
        self._redis.set(f'{self.cache_name}{new_menu.id}',
                        new_menu)
        self._redis.delete(self.cache_name)
        return new_menu

    def update(self, menu_id: UUID,
               menu_data: MenuChange) -> Menu:
        update_menu = self.menu_repository.update(menu_id, menu_data)
        self._redis.set(f'{self.cache_name}{menu_id}',
                        update_menu)
        self._redis.delete(self.cache_name)
        return update_menu

    def get_all(self) -> list[MenuShow]:
        if self._redis.exists(self.cache_name):
            return self._redis.get(self.cache_name)
        menus = self.menu_repository.get_all()
        self._redis.set(self.cache_name, menus)
        return menus

    def get_by_id(self, menu_id: UUID) -> Menu:
        if self._redis.exists(f'{self.cache_name}{menu_id}'):
            return self._redis.get(f'{self.cache_name}{menu_id}')
        menu = self.menu_repository.get_by_id(menu_id)
        self._redis.set(f'{self.cache_name}{menu_id}', menu)
        return menu

    def delete(self, menu_id: UUID) -> None:
        self.menu_repository.delete(menu_id)
        self._redis.del_all()
