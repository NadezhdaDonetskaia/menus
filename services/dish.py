from typing import Any
from uuid import UUID

from fastapi import BackgroundTasks, Depends
from fastapi.responses import JSONResponse
from logger import logger

from repositories.dish import DishRepository
from schemas.dish import BaseDish, DishShow
from services.cache import (
    DISH_CACHE_NAME,
    MENU_CACHE_NAME,
    SUBMENU_CACHE_NAME,
    CacheRepositoryDish,
)


class DishService:
    def __init__(self, dish_repository: DishRepository = Depends(DishRepository)):
        self.dish_repository = dish_repository
        self._redis = CacheRepositoryDish()
        self.background_tasks = BackgroundTasks()

    async def create(self,
                     menu_id: UUID,
                     submenu_id: UUID,
                     dish_data: BaseDish,
                     id: UUID | None = None) -> DishShow:
        new_dish = await self.dish_repository.create(
            submenu_id=submenu_id,
            dish_data=dish_data,
            id=id
        )
        self._redis.create_update(menu_id=menu_id,
                                  submenu_id=submenu_id,
                                  dish_id=new_dish.id,
                                  data=new_dish)
        logger.info(f'Return new dish {new_dish}')
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
            return self._redis.get(key_dish)
        dishes = await self.dish_repository.get_all(submenu_id)
        self.background_tasks.add_task(
            self._redis.set_all(key=key_dish, data=dishes)
        )
        logger.info(f'Return new all dish {dishes}')
        return dishes

    async def get_by_id(self,
                        menu_id: UUID,
                        submenu_id: UUID,
                        dish_id: UUID) -> DishShow | Any:
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

    async def update_data_from_file(
            self,
            dish_data: dict
    ) -> None:
        all_dish_id = await self.dish_repository.get_all_dish_id()
        for dish_id in all_dish_id:
            dish_id = dish_id[0]
            # update dish
            if dish_id in dish_data:
                current_data = dish_data[dish_id]
                logger.info(f'Current data dish {current_data}')
                submenu_id = current_data.pop('submenu_id')
                menu_id = current_data.pop('menu_id')
                await self.update(
                    menu_id=menu_id,
                    submenu_id=submenu_id,
                    dish_id=dish_id,
                    dish_data=BaseDish(**current_data)
                )
                dish_data.pop(dish_id)
            # delete dish
            else:
                submenu_id = await self.dish_repository.get_submenu_id(dish_id=dish_id)
                menu_id = await self.dish_repository.get_menu_id(submenu_id)
                await self.delete(
                    menu_id=menu_id,
                    submenu_id=submenu_id,
                    dish_id=dish_id)
            # create dish
        for dish_id, data in dish_data.items():
            menu_id = data.pop('menu_id')
            submenu_id = data.pop('submenu_id')
            await self.create(
                menu_id=menu_id,
                submenu_id=submenu_id,
                dish_data=BaseDish(**data),
                id=dish_id
            )
