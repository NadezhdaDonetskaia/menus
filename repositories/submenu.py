from uuid import UUID, uuid4

from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_db
from logger_config import logger
from models.submenu import SubMenu
from schemas.submenu import BaseSubMenu, SubMenuShow


class SubMenuRepository:

    def __init__(self, session: AsyncSession = Depends(get_async_db)):
        self.session = session
        self.model = SubMenu

    async def get_all(self, menu_id: UUID) -> list[SubMenuShow]:
        query = select(
            self.model.id,
            self.model.title,
            self.model.description,
            self.model.dishes_count,
        ).where(self.model.menu_id == menu_id)
        logger.debug(f'query submenu all {query}')
        submenus = await self.session.execute(query)
        await self.session.commit()
        return submenus.all()

    async def get_by_id(self,
                        submenu_id: UUID) -> SubMenuShow:
        query = select(
            self.model.id,
            self.model.title,
            self.model.description,
            self.model.dishes_count
        ).where(self.model.id == submenu_id)
        submenu = await self.session.execute(query)
        submenu = submenu.first()
        await self.session.commit()
        if not submenu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='submenu not found')
        return submenu

    async def create(self,
                     menu_id: UUID,
                     submenu_data: BaseSubMenu,
                     id: None | UUID = None) -> SubMenuShow:
        if not id:
            id = uuid4()
        stmt = insert(self.model).values(
            **submenu_data.model_dump(),
            menu_id=menu_id, id=id)
        await self.session.execute(stmt)
        await self.session.commit()
        query = select(
            self.model.id,
            self.model.title,
            self.model.description,
            self.model.dishes_count
        ).where(self.model.title == submenu_data.title)
        new_submenu = await self.session.execute(query)
        await self.session.commit()
        return new_submenu.first()

    async def update(self,
                     submenu_id: UUID,
                     submenu_data: BaseSubMenu) -> SubMenuShow:
        stmt = update(
            self.model).where(
            self.model.id == submenu_id).values(
            **submenu_data.model_dump())
        submenu = await self.session.execute(stmt)
        if not submenu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='menu not found')
        await self.session.commit()
        update_submenu = await self.get_by_id(submenu_id)
        return update_submenu

    async def delete(self,
                     submenu_id: UUID) -> JSONResponse:
        stmt = delete(self.model).where(self.model.id == submenu_id)
        submenu = await self.session.execute(stmt)
        if not submenu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='submenu not found')

        await self.session.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder({
                'status': True,
                'message': 'The submenu has been deleted'
            })
        )

    async def update_data_from_file(
            self,
            submenu_data: dict
    ) -> None:
        all_submenu_id = await self.session.execute(
            select(
                self.model.id
            )
        )
        await self.session.commit()
        for submenu_id in all_submenu_id.all():
            submenu_id = submenu_id[0]
            # update submenu
            if submenu_id in submenu_data:
                current_data = submenu_data[submenu_id]
                logger.info(f'Current data submenu {current_data}')
                current_data.pop('menu_id')
                await self.update(
                    submenu_id=submenu_id,
                    submenu_data=BaseSubMenu(**current_data)
                )
                submenu_data.pop(submenu_id)
            # delete submenu
            else:
                await self.delete(submenu_id=submenu_id)
        #  create submenu
        logger.info(f' ALL ADDED SUBMENU {submenu_data}')
        for submenu_id, data in submenu_data.items():
            logger.info(f'Submenu DATA to ADD {data}')
            menu_id = data.pop('menu_id')
            await self.create(
                menu_id=menu_id,
                submenu_data=BaseSubMenu(**data),
                id=submenu_id
            )
