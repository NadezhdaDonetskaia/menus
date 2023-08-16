from typing import Any
from uuid import UUID

from fastapi import BackgroundTasks, Depends
from fastapi.responses import JSONResponse

from repositories.submenu import SubMenuRepository
from schemas.submenu import BaseSubMenu, SubMenuShow
from services.cache import MENU_CACHE_NAME, SUBMENU_CACHE_NAME, CacheRepositorySubMenu


class SubMenuService:
    def __init__(self, submenu_repository: SubMenuRepository = Depends(SubMenuRepository)):
        self.submenu_repository = submenu_repository
        self._redis = CacheRepositorySubMenu()
        self.background_tasks = BackgroundTasks()

    async def create(self,
                     menu_id: UUID,
                     submenu_data: BaseSubMenu,
                     id: UUID | None = None) -> SubMenuShow:
        new_submenu = await self.submenu_repository.create(
            menu_id,
            submenu_data)
        self.background_tasks.add_task(
            self._redis.create_update(
                menu_id=menu_id,
                submenu_id=new_submenu.id,
                data=new_submenu)
        )
        return new_submenu

    async def update(self,
                     menu_id: UUID,
                     submenu_id: UUID,
                     submenu_data: BaseSubMenu) -> SubMenuShow:
        update_submenu = await self.submenu_repository.update(submenu_id,
                                                              submenu_data)
        self.background_tasks.add_task(
            self._redis.create_update(
                menu_id=menu_id,
                submenu_id=submenu_id,
                data=update_submenu)
        )
        return update_submenu

    async def get_all(self, menu_id: UUID) -> list[SubMenuShow]:
        key_submenus = f'{MENU_CACHE_NAME}{menu_id}{SUBMENU_CACHE_NAME}'
        if self._redis.exists(key_submenus):
            return self._redis.get(key_submenus)
        submenus = await self.submenu_repository.get_all(menu_id)
        self.background_tasks.add_task(
            self._redis.set_all(key=key_submenus, data=submenus)
        )
        return submenus

    async def get_by_id(self,
                        menu_id: UUID,
                        submenu_id: UUID) -> SubMenuShow | Any:
        key_submenu = f'{MENU_CACHE_NAME}{menu_id}' \
                      f'{SUBMENU_CACHE_NAME}{submenu_id}'
        if self._redis.exists(key_submenu):
            return self._redis.get(key_submenu)
        submenu = await self.submenu_repository.get_by_id(submenu_id)
        self.background_tasks.add_task(
            self._redis.set(key=key_submenu, data=submenu)
        )
        return submenu

    async def delete(self, menu_id: UUID, submenu_id: UUID) -> JSONResponse:
        response = await self.submenu_repository.delete(submenu_id)
        self.background_tasks.add_task(
            self._redis.delete(menu_id=menu_id, submenu_id=submenu_id)
        )
        return response

    async def update_data_from_file(
            self,
            submenu_data: dict
    ) -> None:
        all_submenu_id = await self.submenu_repository.get_all_submenu_id()
        for submenu_id in all_submenu_id:
            submenu_id = submenu_id[0]
            # update submenu
            if submenu_id in submenu_data:
                current_data = submenu_data[submenu_id]
                menu_id = current_data.pop('menu_id')
                await self.update(
                    menu_id=menu_id,
                    submenu_id=submenu_id,
                    submenu_data=BaseSubMenu(**current_data)
                )
                submenu_data.pop(submenu_id)
            # delete submenu
            else:
                submenu = await self.submenu_repository.get_by_id(
                    submenu_id=submenu_id)
                submenu_id = submenu.id
                menu_id = await self.submenu_repository.get_menu_id(submenu_id)
                await self.delete(submenu_id=submenu_id,
                                  menu_id=menu_id)
        #  create submenu
        for submenu_id, data in submenu_data.items():
            menu_id = data.pop('menu_id')
            await self.create(
                menu_id=menu_id,
                submenu_data=BaseSubMenu(**data),
                id=submenu_id
            )
