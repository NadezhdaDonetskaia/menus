from pydantic import BaseModel
from .dish import Dish


class SubMenuCreate(BaseModel):
    title: str
    menu_id: int


class SubMenu(BaseModel):
    id: int
    title: str
    description: str
    menu_id: int
    dishes: list[Dish] = []

    class Config:
        orm_mode = True


class SubMenuDetail(BaseModel):
    id: int
    title: str
    description: str
    menu_id: int
    dishes_count: int
