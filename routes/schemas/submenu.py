from pydantic import BaseModel
from .dish import Dish


class SubMenuCreate(BaseModel):
    name: str
    menu_id: int


class SubMenu(BaseModel):
    id: int
    name: str
    menu_id: int
    dishes: list[Dish] = []

    class Config:
        orm_mode = True
