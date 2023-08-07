from uuid import UUID

from pydantic import BaseModel


class BaseMenu(BaseModel):
    title: str
    description: str

    class ConfigDict:
        from_attributes = True


class MenuCreate(BaseMenu):
    id: UUID


class MenuChange(BaseMenu):
    pass


class MenuShow(MenuCreate):
    submenus_count: int
    dishes_count: int
