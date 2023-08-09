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
    def invalidate_cache(self, **cache_keys: UUID) -> None:
        self.redis.delete(MENU_CACHE_NAME)

    def create_update(self,
                      data: MenuChange,
                      **cache_keys: UUID) -> None:
        json_data = json.dumps(jsonable_encoder(data))
        self.invalidate_cache()
        self.redis.set(f'{MENU_CACHE_NAME}{cache_keys["menu_id"]}',
                       json_data)

    def delete(self, **cache_keys: UUID) -> None:
        self.invalidate_cache()
        self.redis.delete(f'{MENU_CACHE_NAME}{cache_keys["menu_id"]}')


class CacheRepositorySubMenu(CacheRepositoryMenu):
    def invalidate_cache(self, **cache_keys: UUID) -> None:
        super().invalidate_cache()
        self.redis.delete(f'{MENU_CACHE_NAME}{cache_keys["menu_id"]}')
        self.redis.delete(f'{MENU_CACHE_NAME}{cache_keys["menu_id"]}'
                          f'{SUBMENU_CACHE_NAME}')

    def create_update(self,
                      data: SubMenuChange,
                      **cache_keys: UUID
                      ) -> None:
        json_data = json.dumps(jsonable_encoder(data))
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
    def invalidate_cache(self, **cache_keys: UUID) -> None:
        super().invalidate_cache(**cache_keys)
        self.redis.delete(f'{MENU_CACHE_NAME}{cache_keys["menu_id"]}'
                          f'{SUBMENU_CACHE_NAME}{cache_keys["submenu_id"]}')
        self.redis.delete(
            f'{MENU_CACHE_NAME}{cache_keys["menu_id"]}'
            f'{SUBMENU_CACHE_NAME}{cache_keys["submenu_id"]}{DISH_CACHE_NAME}')

    def create_update(self, data: DishChange, **cache_keys: UUID) -> None:
        json_data = json.dumps(jsonable_encoder(data))
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
