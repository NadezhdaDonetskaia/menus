from uuid import UUID

from pydantic import BaseModel


class BaseDish(BaseModel):
    title: str
    description: str
    price: str

    class ConfigDict:
        from_attributes = True


class DishShow(BaseDish):
    id: UUID
