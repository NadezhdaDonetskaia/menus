# mypy: ignore-errors

import json
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from redis import Redis

from config import REDIS_HOST, REDIS_PORT
from schemas.dish import DishChange
from schemas.menu import MenuChange
from schemas.submenu import SubMenuChange

MENU_CACHE_NAME = 'menu'
SUBMENU_CACHE_NAME = 'submenu'
DISH_CACHE_NAME = 'dish'


class CacheRepository:
    def __init__(self):
        self.redis = Redis(host=REDIS_HOST, port=REDIS_PORT,
                           decode_responses=True)

    def set(self, key: str, data: BaseModel) -> None:
        json_data = json.dumps(jsonable_encoder(data))
        self.redis.set(key, json_data)

    def get(self, key: str) -> BaseModel:
        json_data = self.redis.get(key)
        serialized_item_data = json.loads(json_data)
        return serialized_item_data

    def exists(self, key: str) -> bool:
        return self.redis.exists(key)

    def del_all(self) -> None:
        self.redis.flushall()


class CacheRepositoryMenu(CacheRepository):
    def invalidate_cache(self, *cache_keys: UUID) -> None:
        self.redis.delete(MENU_CACHE_NAME)

    def create_update(self, menu_id: UUID,
                      data: MenuChange) -> None:
        json_data = json.dumps(jsonable_encoder(data))
        self.invalidate_cache()
        self.redis.set(f'{MENU_CACHE_NAME}{menu_id}',
                       json_data)

    def delete(self, menu_id: UUID, *cache_keys: UUID) -> None:
        self.invalidate_cache()
        self.redis.delete(f'{MENU_CACHE_NAME}{menu_id}')


class CacheRepositorySubMenu(CacheRepositoryMenu):
    def invalidate_cache(self, menu_id: UUID) -> None:
        super().invalidate_cache()
        self.redis.delete(f'{MENU_CACHE_NAME}{menu_id}')
        self.redis.delete(f'{MENU_CACHE_NAME}{menu_id}{SUBMENU_CACHE_NAME}')

    def create_update(self, menu_id: UUID, submenu_id: UUID,
                      data: SubMenuChange) -> None:
        json_data = json.dumps(jsonable_encoder(data))
        self.invalidate_cache(menu_id)
        self.redis.set(f'{MENU_CACHE_NAME}{menu_id}{SUBMENU_CACHE_NAME}{submenu_id}',
                       json_data)

    def delete(self, menu_id: UUID, submenu_id: UUID) -> None:
        self.invalidate_cache(menu_id)
        self.redis.delete(f'{MENU_CACHE_NAME}{menu_id}{SUBMENU_CACHE_NAME}{submenu_id}')


class CacheRepositoryDish(CacheRepositorySubMenu):
    def invalidate_cache(self, menu_id: UUID, submenu_id: UUID) -> None:
        super().invalidate_cache(menu_id)
        self.redis.delete(f'{MENU_CACHE_NAME}{menu_id}{SUBMENU_CACHE_NAME}{submenu_id}')
        self.redis.delete(f'{MENU_CACHE_NAME}{menu_id}{SUBMENU_CACHE_NAME}{submenu_id}{DISH_CACHE_NAME}')

    def create_update(self, menu_id: UUID,
                      submenu_id: UUID, dish_id: UUID,
                      data: DishChange) -> None:
        json_data = json.dumps(jsonable_encoder(data))
        self.invalidate_cache(menu_id, submenu_id)
        self.redis.set(f'{MENU_CACHE_NAME}{menu_id}{SUBMENU_CACHE_NAME}{submenu_id}{DISH_CACHE_NAME}{dish_id}',
                       json_data)

    def delete(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID) -> None:
        self.invalidate_cache(menu_id, submenu_id)
        self.redis.delete(f'{MENU_CACHE_NAME}{menu_id}{SUBMENU_CACHE_NAME}{submenu_id}{DISH_CACHE_NAME}{dish_id}')
