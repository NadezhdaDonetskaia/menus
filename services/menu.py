from uuid import UUID

from fastapi import BackgroundTasks, Depends
from fastapi.responses import JSONResponse

from logger_config import logger
from repositories.menu import MenuRepository
from schemas.menu import BaseMenu, MenuShow
from services.cache import MENU_CACHE_NAME, CacheRepositoryMenu


class MenuService:
    def __init__(self, menu_repository=Depends(MenuRepository)):
        self.menu_repository = menu_repository
        self._redis = CacheRepositoryMenu()
        self.key = MENU_CACHE_NAME
        self.background_tasks: BackgroundTasks = BackgroundTasks()

    async def create(self, menu_data: BaseMenu) -> MenuShow:
        new_menu = await self.menu_repository.create(menu_data)
        logger.debug(f'new_menu {new_menu}')
        self.background_tasks.add_task(
            self._redis.create_update(menu_id=new_menu.id, data=new_menu))
        return new_menu

    async def update(self,
                     menu_id: UUID,
                     menu_data: BaseMenu) -> MenuShow:
        update_menu = await self.menu_repository.update(menu_id, menu_data)
        self.background_tasks.add_task(
            self._redis.create_update(menu_id=menu_id, data=update_menu)
        )
        return update_menu

    async def get_all(self) -> list[MenuShow]:
        if self._redis.exists(self.key):
            return self._redis.get(self.key)
        menus = await self.menu_repository.get_all()
        self.background_tasks.add_task(
            self._redis.set_all(self.key, menus)
        )
        return menus

    async def get_by_id(self, menu_id: UUID) -> MenuShow:
        if self._redis.exists(f'{self.key}{menu_id}'):
            return self._redis.get(f'{self.key}{menu_id}')
        menu = await self.menu_repository.get_by_id(menu_id)
        self.background_tasks.add_task(
            self._redis.set(f'{self.key}{menu_id}', menu)
        )
        return menu

    async def delete(self, menu_id: UUID) -> JSONResponse:
        response = await self.menu_repository.delete(menu_id)
        self.background_tasks.add_task(
            self._redis.delete(menu_id=menu_id)
        )
        return response
