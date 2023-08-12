from uuid import UUID

from pydantic import BaseModel


class BaseSubMenu(BaseModel):
    title: str
    description: str

    class ConfigDict:
        from_attributes = True


class SubMenuShow(BaseSubMenu):
    id: UUID
    dishes_count: int
