from pydantic import BaseModel
from .submenu import SubMenu


class MenuCreate(BaseModel):
    name: str


class Menu(BaseModel):
    id: int
    name: str
    submenus: list[SubMenu] = []

    class Config:
        orm_mode = True


class MenuDetail(BaseModel):
    id: int
    name: str
    submenus_count: int
    dishes_count: int
