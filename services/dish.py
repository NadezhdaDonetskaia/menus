from uuid import UUID

from fastapi import Depends

from repositories.dish import DishRepository
from schemas.dish import BaseDish, DishChange, DishCreate, DishShow

from .cache import (
    DISH_CACHE_NAME,
    MENU_CACHE_NAME,
    SUBMENU_CACHE_NAME,
    CacheRepositoryDish,
)


class DishService:
    def __init__(self, dish_repository=Depends(DishRepository)):
        self.dish_repository = dish_repository
        self._redis = CacheRepositoryDish()

    def create(self,
               menu_id: UUID,
               submenu_id: UUID,
               dish_data: DishChange) -> DishCreate:
        new_dish = self.dish_repository.create(submenu_id, dish_data)
        self._redis.create_update(menu_id, submenu_id, new_dish.id, new_dish)
        return new_dish

    def update(self,
               menu_id: UUID,
               submenu_id: UUID,
               dish_id: UUID,
               dish_data: DishChange) -> BaseDish:
        update_dish = self.dish_repository.update(submenu_id,
                                                  dish_id, dish_data)
        self._redis.create_update(menu_id, submenu_id, dish_id, update_dish)
        return update_dish

    def get_all(self, menu_id: UUID, submenu_id: UUID) -> list[DishShow]:
        key_dish = f'{MENU_CACHE_NAME}{menu_id}{SUBMENU_CACHE_NAME}{submenu_id}{DISH_CACHE_NAME}'
        if self._redis.exists(key_dish):
            return self._redis.get(key_dish)
        dishes = self.dish_repository.get_all(submenu_id)
        self._redis.set(key_dish, dishes)
        return dishes

    def get_by_id(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID) -> DishShow:
        key_submenu = f'{MENU_CACHE_NAME}{menu_id}{SUBMENU_CACHE_NAME}{submenu_id}{DISH_CACHE_NAME}{dish_id}'
        if self._redis.exists(key_submenu):
            return self._redis.get(key_submenu)
        submenu = self.dish_repository.get_by_id(submenu_id, dish_id)
        self._redis.set(key_submenu, submenu)
        return submenu

    def delete(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID) -> None:
        self.dish_repository.delete(submenu_id, dish_id)
        self._redis.delete(menu_id, submenu_id, dish_id)
