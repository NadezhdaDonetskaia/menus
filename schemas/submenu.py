from uuid import UUID

from pydantic import BaseModel


class BaseSubMenu(BaseModel):
    title: str
    description: str

    class ConfigDict:
        from_attributes = True


class SubMenuCreate(BaseSubMenu):
    id: UUID


class SubMenuChange(BaseSubMenu):
    pass


class SubMenuShow(SubMenuCreate):
    dishes_count: int
