import json

from fastapi.encoders import jsonable_encoder
from redis import Redis

MENU_CACHE_NAME = 'menu'
SUBMENU_CACHE_NAME = 'submenu'
DISH_CACHE_NAME = 'dish'


class CacheRepository:
    def __init__(self):
        self.redis = Redis(host='localhost', port=6379, decode_responses=True)

    def get_redis(self):
        return self

    def set(self, key, data):
        json_data = json.dumps(jsonable_encoder(data))
        self.redis.set(key, json_data)

    def get(self, key):
        json_data = self.redis.get(key)
        serialized_item_data = json.loads(json_data)
        return serialized_item_data

    def exists(self, key):
        return self.redis.exists(key)

    def delete(self, key):
        self.redis.delete(key)

    def del_all(self):
        self.redis.flushall()
