from fastapi import BackgroundTasks, Depends
from fastapi.responses import JSONResponse

from repositories.all import AllRepository
from services.cache import ALL_CACHE_NAME, CacheRepositoryAll


class AllService:
    def __init__(self, repository=Depends(AllRepository)):
        self.repository = repository
        self._redis = CacheRepositoryAll()
        self.key = ALL_CACHE_NAME
        self.background_tasks = BackgroundTasks()

    async def get_all(
            self) -> JSONResponse:
        if self._redis.exists(self.key):
            return self._redis.get(self.key)
        all = await self.repository.get_all()
        self.background_tasks.add_task(
            self._redis.set(self.key, all)
        )
        return all
