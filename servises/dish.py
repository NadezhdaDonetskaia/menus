from uuid import UUID

from fastapi import Depends

from models.dish import Dish
from repositories.dish import DishRepository
from schemas.dish import DishChange, DishShow

from .cache import DISH_CACHE_NAME, SUBMENU_CACHE_NAME, CacheRepository


class DishService:
    def __init__(self, dish_repository=Depends(DishRepository)):
        self.dish_repository = dish_repository
        self.cache_name = DISH_CACHE_NAME
        self._redis = CacheRepository().get_redis()

    def create(self,
               submenu_id: UUID,
               dish_data: DishChange) -> Dish:
        new_dish = self.dish_repository.create(submenu_id, dish_data)
        self._redis.del_all()
        self._redis.set(
            f'{SUBMENU_CACHE_NAME}{submenu_id}{self.cache_name}{new_dish.id}',
            new_dish)
        return new_dish

    def update(self,
               submenu_id: UUID,
               dish_id: UUID,
               dish_data: DishChange) -> Dish:
        update_dish = self.dish_repository.update(submenu_id,
                                                  dish_id, dish_data)
        self._redis.set(
            f'{SUBMENU_CACHE_NAME}{submenu_id}{self.cache_name}{dish_id}',
            update_dish)
        self._redis.delete(f'{SUBMENU_CACHE_NAME}{submenu_id}{self.cache_name}')
        return update_dish

    def get_all(self, submenu_id: UUID) -> list[DishShow]:
        key_dish = f'{SUBMENU_CACHE_NAME}{submenu_id}{self.cache_name}'
        if self._redis.exists(key_dish):
            self._redis.get(key_dish)
        dishes = self.dish_repository.get_all(submenu_id)
        self._redis.set(key_dish, dishes)
        return dishes

    def get_by_id(self, submenu_id: UUID, dish_id: UUID) -> Dish:
        key_submenu = f'{SUBMENU_CACHE_NAME}{submenu_id}{self.cache_name}{dish_id}'
        if self._redis.exists(key_submenu):
            return self._redis.get(key_submenu)
        submenu = self.dish_repository.get_by_id(submenu_id, dish_id)
        self._redis.set(key_submenu, submenu)
        return submenu

    def delete(self, submenu_id: UUID, dish_id: UUID) -> None:
        self.dish_repository.delete(submenu_id, dish_id)
        self._redis.del_all()
