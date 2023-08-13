from uuid import UUID

from fastapi import BackgroundTasks, Depends
from fastapi.responses import JSONResponse

from repositories.dish import DishRepository
from schemas.dish import BaseDish, DishShow
from services.cache import (
    DISH_CACHE_NAME,
    MENU_CACHE_NAME,
    SUBMENU_CACHE_NAME,
    CacheRepositoryDish,
)


class DishService:
    def __init__(self, dish_repository=Depends(DishRepository)):
        self.dish_repository = dish_repository
        self._redis = CacheRepositoryDish()
        self.background_tasks = BackgroundTasks()

    async def create(self,
                     menu_id: UUID,
                     submenu_id: UUID,
                     dish_data: BaseDish) -> DishShow:
        new_dish = await self.dish_repository.create(submenu_id, dish_data)
        self._redis.create_update(menu_id=menu_id,
                                  submenu_id=submenu_id,
                                  dish_id=new_dish.id,
                                  data=new_dish)
        return new_dish

    async def update(self,
                     menu_id: UUID,
                     submenu_id: UUID,
                     dish_id: UUID,
                     dish_data: BaseDish) -> DishShow:
        update_dish = await self.dish_repository.update(dish_id, dish_data)
        self.background_tasks.add_task(
            self._redis.create_update(
                menu_id=menu_id,
                submenu_id=submenu_id,
                dish_id=dish_id,
                data=update_dish)
        )
        return update_dish

    async def get_all(self,
                      menu_id: UUID,
                      submenu_id: UUID) -> list[DishShow]:
        key_dish = f'{MENU_CACHE_NAME}{menu_id}' \
                   f'{SUBMENU_CACHE_NAME}{submenu_id}' \
                   f'{DISH_CACHE_NAME}'
        if self._redis.exists(key_dish):
            return self._redis.get_all(key_dish)
        dishes = await self.dish_repository.get_all(submenu_id)
        self.background_tasks.add_task(
            self._redis.set_all(key=key_dish, data=dishes)
        )
        return dishes

    async def get_by_id(self,
                        menu_id: UUID,
                        submenu_id: UUID,
                        dish_id: UUID) -> DishShow:
        key_submenu = f'{MENU_CACHE_NAME}{menu_id}' \
                      f'{SUBMENU_CACHE_NAME}{submenu_id}' \
                      f'{DISH_CACHE_NAME}{dish_id}'
        if self._redis.exists(key_submenu):
            return self._redis.get(key_submenu)
        submenu = await self.dish_repository.get_by_id(dish_id)
        self.background_tasks.add_task(
            self._redis.set(key=key_submenu, data=submenu)
        )
        return submenu

    async def delete(self,
                     menu_id: UUID,
                     submenu_id: UUID,
                     dish_id: UUID) -> JSONResponse:
        response = await self.dish_repository.delete(dish_id)
        self.background_tasks.add_task(
            self._redis.delete(
                menu_id=menu_id,
                submenu_id=submenu_id,
                dish_id=dish_id)
        )
        return response
