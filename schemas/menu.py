from uuid import UUID

from pydantic import BaseModel


class BaseMenu(BaseModel):
    title: str
    description: str

    class ConfigDict:
        from_attributes = True


class MenuShow(BaseMenu):
    id: UUID
    submenus_count: int
    dishes_count: int
