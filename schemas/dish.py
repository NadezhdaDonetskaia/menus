from uuid import UUID

from pydantic import BaseModel


class BaseDish(BaseModel):
    title: str
    description: str
    price: str

    class ConfigDict:
        from_attributes = True


class DishCreate(BaseDish):
    id: UUID


class DishChange(BaseDish):
    pass


class DishShow(DishCreate):
    pass
