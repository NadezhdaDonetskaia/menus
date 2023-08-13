import json
from typing import Any
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from redis import Redis

from config import REDIS_HOST, REDIS_PORT
from schemas.dish import BaseDish, DishShow
from schemas.menu import BaseMenu, MenuShow
from schemas.submenu import BaseSubMenu, SubMenuShow

MENU_CACHE_NAME = 'menu'
SUBMENU_CACHE_NAME = 'submenu'
DISH_CACHE_NAME = 'dish'
ALL_CACHE_NAME = 'all'


class CacheRepository:
    def __init__(self):
        self.redis = Redis(host=REDIS_HOST,
                           port=REDIS_PORT,
                           decode_responses=True)

    def set(self, key: str, data: BaseModel) -> None:
        json_data = json.dumps(data)
        self.redis.set(key, json_data)

    def get(self, key: str) -> BaseModel | list[BaseModel]:
        json_data = self.redis.get(key)
        serialized_item_data = json.loads(json_data)
        return serialized_item_data

    def exists(self, key: str) -> bool:
        return self.redis.exists(key)


class CacheRepositoryMenu(CacheRepository):

    def serialize_menu(self, menu_data: MenuShow) -> dict:
        return {
            'id': str(menu_data.id),
            'title': menu_data.title,
            'description': menu_data.description,
            'submenus_count': menu_data.submenus_count,
            'dishes_count': menu_data.dishes_count
        }

    def invalidate_cache(self, **cache_keys: UUID) -> None:
        self.redis.delete(MENU_CACHE_NAME)
        self.redis.delete(ALL_CACHE_NAME)

    def set_all(self, key: str, data: list[MenuShow] | Any) -> None:
        if data:
            data = [self.serialize_menu(menu) for menu in data]
        json_data = json.dumps(data)
        self.redis.set(key, json_data)

    def set(self, key: str, data: BaseMenu | Any) -> None:
        if data:
            data = self.serialize_menu(data)
        json_data = json.dumps(data)
        self.redis.set(key, json_data)

    def create_update(self,
                      data: BaseMenu,
                      **cache_keys: UUID) -> None:
        json_data = json.dumps(jsonable_encoder(self.serialize_menu(data)))
        self.invalidate_cache()
        self.redis.set(f'{MENU_CACHE_NAME}{cache_keys["menu_id"]}',
                       json_data)

    def delete(self, **cache_keys: UUID) -> None:
        self.invalidate_cache()
        self.redis.delete(f'{MENU_CACHE_NAME}{cache_keys["menu_id"]}')


class CacheRepositorySubMenu(CacheRepositoryMenu):
    def serialize_submenu(self, submenu_data: MenuShow) -> dict:
        return {
            'id': str(submenu_data.id),
            'title': submenu_data.title,
            'description': submenu_data.description,
            'dishes_count': submenu_data.dishes_count
        }

    def invalidate_cache(self,
                         **cache_keys: UUID) -> None:
        super().invalidate_cache()
        self.redis.delete(f'{MENU_CACHE_NAME}{cache_keys["menu_id"]}')
        self.redis.delete(f'{MENU_CACHE_NAME}{cache_keys["menu_id"]}'
                          f'{SUBMENU_CACHE_NAME}')

    def set_all(self, key: str, data: list[SubMenuShow] | Any) -> None:
        if data:
            data = [self.serialize_submenu(submenu) for submenu in data]
        json_data = json.dumps(data)
        self.redis.set(key, json_data)

    def set(self, key: str, data: BaseSubMenu | Any) -> None:
        if data:
            data = self.serialize_submenu(data)
        json_data = json.dumps(data)
        self.redis.set(key, json_data)

    def create_update(self,
                      data: BaseSubMenu,
                      **cache_keys: UUID
                      ) -> None:
        json_data = json.dumps(jsonable_encoder(self.serialize_submenu(data)))
        self.invalidate_cache(**cache_keys)
        self.redis.set(
            f'{MENU_CACHE_NAME}{cache_keys["menu_id"]}'
            f'{SUBMENU_CACHE_NAME}{cache_keys["submenu_id"]}',
            json_data)

    def delete(self, **cache_keys: UUID) -> None:
        self.invalidate_cache(**cache_keys)
        self.redis.delete(f'{MENU_CACHE_NAME}{cache_keys["menu_id"]}'
                          f'{SUBMENU_CACHE_NAME}{cache_keys["submenu_id"]}')


class CacheRepositoryDish(CacheRepositorySubMenu):
    def serialize_dish(self, dish_data: DishShow) -> dict:
        return {
            'id': str(dish_data.id),
            'title': dish_data.title,
            'description': dish_data.description,
            'price': dish_data.price
        }

    def set_all(self, key: str, data: list[DishShow] | Any) -> None:
        if data:
            data = [self.serialize_dish(dish) for dish in data]
        json_data = json.dumps(data)
        self.redis.set(key, json_data)

    def set(self, key: str, data: DishShow | Any) -> None:
        if data:
            data = self.serialize_dish(data)
        json_data = json.dumps(data)
        self.redis.set(key, json_data)

    def invalidate_cache(self, **cache_keys: UUID) -> None:
        super().invalidate_cache(**cache_keys)
        self.redis.delete(f'{MENU_CACHE_NAME}{cache_keys["menu_id"]}'
                          f'{SUBMENU_CACHE_NAME}{cache_keys["submenu_id"]}')
        self.redis.delete(
            f'{MENU_CACHE_NAME}{cache_keys["menu_id"]}'
            f'{SUBMENU_CACHE_NAME}{cache_keys["submenu_id"]}{DISH_CACHE_NAME}')

    def create_update(self,
                      data: BaseDish,
                      **cache_keys: UUID) -> None:
        json_data = json.dumps(jsonable_encoder(self.serialize_dish(data)))
        self.invalidate_cache(**cache_keys)
        self.redis.set(
            f'{MENU_CACHE_NAME}{cache_keys["menu_id"]}'
            f'{SUBMENU_CACHE_NAME}{cache_keys["submenu_id"]}'
            f'{DISH_CACHE_NAME}{cache_keys["dish_id"]}',
            json_data)

    def delete(self, **cache_keys: UUID) -> None:
        self.invalidate_cache(**cache_keys)
        self.redis.delete(
            f'{MENU_CACHE_NAME}{cache_keys["menu_id"]}'
            f'{SUBMENU_CACHE_NAME}{cache_keys["submenu_id"]}'
            f'{DISH_CACHE_NAME}{cache_keys["dish_id"]}')


class CacheRepositoryAll(CacheRepository):

    pass
