from pydantic import BaseModel
# from .dish import Dish


class SubMenuCreate(BaseModel):
    title: str
    description: str
    # menu_id: str


class SubMenu(BaseModel):
    # id: int
    title: str
    description: str
    # menu_id: int
    # dishes: list[Dish] = []

    class Config:
        orm_mode = True


class SubMenuDetail(BaseModel):
    # id: str
    title: str
    description: str
    menu_id: str
    # dishes_count: str
