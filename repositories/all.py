from fastapi import Depends
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_db
from logger_config import logger
from models.menu import Dish, Menu, SubMenu


class AllRepository:

    def __init__(self, session: AsyncSession = Depends(get_async_db)):
        self.session = session
        self.menu = Menu
        self.submenu = SubMenu
        self.dish = Dish

    def serialize_all(self, data):
        all_menus = dict()

        for data in data:
            menu_title, menu_descroption, submenu_title, submenu_description, dish_title, dish_description, dish_price = data

            if menu_title not in all_menus:
                all_menus[menu_title] = {'description': menu_descroption}
            menu_info = all_menus[menu_title]

            if not submenu_title:
                continue
            if submenu_title not in menu_info:
                menu_info[submenu_title] = {'description': submenu_description}

            submenu_info = menu_info[submenu_title]
            if not dish_title:
                continue
            if dish_title not in submenu_info:
                submenu_info[dish_title] = {'description': dish_description}

            dish_info = submenu_info[dish_title]
            dish_info['price'] = dish_price

        return all_menus

    async def get_all(
            self) -> JSONResponse:
        query = select(
            self.menu.title,
            self.menu.description,
            self.submenu.title,
            self.submenu.description,
            self.dish.title,
            self.dish.description,
            self.dish.price
        ).select_from(Menu).outerjoin(SubMenu).outerjoin(Dish)
        logger.info(f'query menu all {query}')
        all = await self.session.execute(query)
        await self.session.commit()
        all = self.serialize_all(all.all())
        return all
