import os

from celery import Celery
from fastapi import Depends
from logger import logger
from sqlalchemy.ext.asyncio import AsyncSession

from config import BACKEND_URL
from config import BROKER_URL as broker_url
from database import get_async_db
from repositories.dish import DishRepository
from repositories.menu import MenuRepository
from repositories.submenu import SubMenuRepository
from schemas.dish import BaseDish
from schemas.menu import BaseMenu
from schemas.submenu import BaseSubMenu
from tasks.read_files import get_data_from_excel_file, is_change_file

relative_path = '../admin/Menu.xlsx'
current_directory = os.path.dirname(__file__)
PATH_FIFE_EXCEL = os.path.join(current_directory, relative_path)


# @router.get('')
# async def test(session: AsyncSession = Depends(get_async_db)):
#     return await check_and_update_excel_file(PATH_FIFE_EXCEL, session)

celery_app = Celery(
    'worker',
    broker=broker_url,
    backend=BACKEND_URL,
    set_as_current=True
)


celery_app.conf.beat_schedule = {
    'check-and-update-every-15-seconds': {
        'task': 'tasks.tasks.check_and_update_excel_file',
        'schedule': 15.0,
        'args': (PATH_FIFE_EXCEL,),
    },
}


celery_app.conf.update(task_track_started=True)


async def update_menu(menu_data, session):
    menu_repo = MenuRepository(session)
    for menu in menu_data:
        await menu_repo.update(menu.pop('id'), BaseMenu(**menu))


async def update_submenu(submenu_data, session):
    submenu_repo = SubMenuRepository(session)
    for submenu in submenu_data:
        await submenu_repo.update(submenu.pop('id'), BaseSubMenu(**submenu))


async def update_dish(dish_data, session):
    dish_repo = DishRepository(session)
    for dish in dish_data:
        await dish_repo.update(dish.pop('id'), BaseDish(**dish))


# задача реализована только на изменение,
# иначе нужна двусторонняя настройка (что в базе -> то в файле)

async def update_data(data, session):
    menu_data, submenu_data, dish_data = data
    await update_menu(menu_data, session)
    await update_submenu(submenu_data, session)
    await update_dish(dish_data, session)


@celery_app.task
def check_and_update_excel_file(excel_file_path,
                                session: AsyncSession = Depends(get_async_db)):
    logger.info('start check_and_update_excel_file')
    if is_change_file(excel_file_path):
        new_data = get_data_from_excel_file(excel_file_path)
        logger.info(f'new_data {new_data}')
        update_data(new_data, session)
        return 'Database data updated successfully'
    return 'No data to change'


if __name__ == '__main__':
    beat = celery_app.Beat(loglevel='debug')
    beat.start_scheduler()
