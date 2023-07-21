from pydantic import BaseModel


class DishCreate(BaseModel):
    name: str
    price: float
    submenu_id: int


class Dish(BaseModel):
    id: int
    submenu_id: int
    name: str
    price: float

    class Config:
        orm_mode = True
