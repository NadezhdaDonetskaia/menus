from pydantic import BaseModel
from .submenu import SubMenu


class MenuCreate(BaseModel):
    title: str
    description: str


class Menu(BaseModel):
    id: int
    title: str
    description: str
    submenus: list[SubMenu] = []

    class Config:
        orm_mode = True


class MenuDetail(BaseModel):
    id: int
    title: str
    description: str
    submenus_count: int
    dishes_count: int
