from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_db
from logger_config import logger
from models.menu import Menu
from schemas.menu import BaseMenu, MenuShow


class MenuRepository:

    def __init__(self, session: AsyncSession = Depends(get_async_db)):
        self.session = session
        self.model = Menu

    async def get_all(self) -> list[MenuShow]:
        query = select(
            self.model.id,
            self.model.title,
            self.model.description,
            self.model.submenus_count,
            self.model.dishes_count
        )
        logger.debug(f'query menu all {query}')
        menus = await self.session.execute(query)
        await self.session.commit()
        return menus.all()

    async def get_by_id(self, menu_id: UUID) -> MenuShow:
        query = select(
            self.model.id,
            self.model.title,
            self.model.description,
            self.model.submenus_count,
            self.model.dishes_count
        ).where(self.model.id == menu_id)
        menu = await self.session.execute(query)
        menu = menu.first()
        await self.session.commit()
        if not menu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='menu not found')
        return menu

    async def create(self, menu_data: BaseMenu) -> MenuShow:
        stmt = insert(self.model).values(**menu_data.model_dump())
        await self.session.execute(stmt)
        await self.session.commit()
        query = select(
            self.model.id,
            self.model.title,
            self.model.description,
            self.model.submenus_count,
            self.model.dishes_count
        ).where(self.model.title == menu_data.title)
        new_menu = await self.session.execute(query)
        await self.session.commit()
        return new_menu.first()

    async def update(self, menu_id: UUID, menu_data: BaseMenu) -> MenuShow:
        logger.info(f'Update NENU {menu_id}')
        stmt = update(
            self.model).where(
            self.model.id == menu_id).values(
            **menu_data.model_dump())
        menu = await self.session.execute(stmt)
        if not menu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='menu not found')
        await self.session.commit()
        update_menu = await self.get_by_id(menu_id)
        return update_menu

    async def delete(self, menu_id: UUID) -> JSONResponse:
        stmt = delete(self.model).where(self.model.id == menu_id)
        menu = await self.session.execute(stmt)
        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='menu not found')

        await self.session.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder({
                'status': True,
                'message': 'The menu has been deleted'
            })
        )
