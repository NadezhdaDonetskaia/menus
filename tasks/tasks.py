import requests
from celery import Celery
from fastapi import APIRouter, Depends
from logger import logger
from sqlalchemy.ext.asyncio import AsyncSession

from config import APP_URL, BACKEND_URL
from config import BROKER_URL as broker_url
from database import get_async_db
from repositories.dish import DishRepository
from repositories.menu import MenuRepository
from repositories.submenu import SubMenuRepository
from schemas.dish import BaseDish
from schemas.menu import BaseMenu
from schemas.submenu import BaseSubMenu
from tasks.read_files import PATH_FILE_EXCEL as path
from tasks.read_files import get_data_from_excel_file, is_change_file

task_router = APIRouter(
    prefix='/api/v1/update_from_file',
    tags=['Updates']
)


@task_router.get('')
async def test(session: AsyncSession = Depends(get_async_db)):
    return await check_and_update_base_excel_file(path, session)


# задача реализована только на изменение,
# иначе нужна двусторонняя настройка (что в базе -> то в файле)
async def check_and_update_base_excel_file(excel_file_path, session):
    logger.info('start check_and_update_excel_file')
    if is_change_file(excel_file_path):
        new_data = get_data_from_excel_file()
        return await update_data(new_data, session)
    return 'No data to change'


async def update_data(data, session):
    menu_data, submenu_data, dish_data = data
    await update_menu(menu_data, session)
    await update_submenu(submenu_data, session)
    await update_dish(dish_data, session)
    return 'Database data updated successfully'


async def update_menu(menu_data, session):
    logger.info('Start update menu')
    menu_repo = MenuRepository(session)
    for menu in menu_data:
        await menu_repo.update(menu.pop('id'), BaseMenu(**menu))


async def update_submenu(submenu_data, session):
    logger.info('Start update submenu')
    submenu_repo = SubMenuRepository(session)
    for submenu in submenu_data:
        await submenu_repo.update(submenu.pop('id'), BaseSubMenu(**submenu))


async def update_dish(dish_data, session):
    logger.info('Start update dish')
    dish_repo = DishRepository(session)
    for dish in dish_data:
        await dish_repo.update(dish.pop('id'), BaseDish(**dish))


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
        # 'args': (path,),
    },
}

celery_app.conf.update(task_track_started=True)


@celery_app.task
def check_and_update_excel_file():
    requests.get(f'{APP_URL}/api/v1/update_from_file')


if __name__ == '__main__':
    beat = celery_app.Beat(loglevel='debug')
    beat.start_scheduler()
