from uuid import UUID, uuid4

from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_db
from logger_config import logger
from models.dish import Dish
from schemas.dish import BaseDish, DishShow


class DishRepository:

    def __init__(self, session: AsyncSession = Depends(get_async_db)) -> None:
        self.session = session
        self.model = Dish

    async def get_all(self, submenu_id: UUID) -> list[DishShow]:
        query = select(
            self.model.id,
            self.model.title,
            self.model.description,
            self.model.price,
        ).where(self.model.submenu_id == submenu_id)
        logger.debug(f'query dish all {query}')
        dishes = await self.session.execute(query)
        await self.session.commit()
        return dishes.all()

    async def get_by_id(self, dish_id: UUID) -> DishShow:
        query = select(
            self.model.id,
            self.model.title,
            self.model.description,
            self.model.price
        ).where(self.model.id == dish_id)
        dish = await self.session.execute(query)
        dish = dish.first()
        await self.session.commit()
        if not dish:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='dish not found')
        return dish

    async def create(self,
                     submenu_id: UUID,
                     dish_data: BaseDish,
                     id: None | UUID = None) -> DishShow:
        if not id:
            id = uuid4()
        stmt = insert(self.model).values(
            **dish_data.model_dump(),
            submenu_id=submenu_id, id=id)
        await self.session.execute(stmt)
        await self.session.commit()
        query = select(
            self.model.id,
            self.model.title,
            self.model.description,
            self.model.price
        ).where(self.model.title == dish_data.title)
        new_submenu = await self.session.execute(query)
        await self.session.commit()
        return new_submenu.first()

    async def update(self,
                     dish_id: UUID, dish_data: BaseDish) -> DishShow:
        stmt = update(
            self.model).where(
            self.model.id == dish_id).values(
            **dish_data.model_dump())
        dish = await self.session.execute(stmt)
        if not dish:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='menu not found')
        await self.session.commit()
        update_dish = await self.get_by_id(dish_id)
        return update_dish

    async def delete(self, dish_id: UUID) -> JSONResponse:
        stmt = delete(self.model).where(self.model.id == dish_id)
        dish = await self.session.execute(stmt)
        if not dish:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='dish not found')

        await self.session.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder({
                'status': True,
                'message': 'The dish has been deleted'
            })
        )

    async def update_data_from_file(
            self,
            dish_data: dict
    ) -> None:
        all_dish_id = await self.session.execute(
            select(
                self.model.id
            )
        )
        await self.session.commit()
        all_dish_id = all_dish_id.all()
        for dish_id in all_dish_id:
            dish_id = dish_id[0]
            # update dish
            if dish_id in dish_data:
                current_data = dish_data[dish_id]
                logger.info(f'Current data dish {current_data}')
                current_data.pop('submenu_id')
                await self.update(
                    dish_id=dish_id,
                    dish_data=BaseDish(**current_data)
                )
                dish_data.pop(dish_id)
            # delete dish
            else:
                await self.delete(dish_id=dish_id)
            # create dish
        for dish_id, data in dish_data.items():
            submenu_id = data.pop('submenu_id')
            await self.create(
                submenu_id=submenu_id,
                dish_data=BaseDish(**data),
                id=dish_id
            )
