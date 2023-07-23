from pydantic import BaseModel


class DishCreate(BaseModel):
    title: str
    description: str
    price: float
    submenu_id: int


class Dish(BaseModel):
    id: int
    submenu_id: int
    title: str
    description: str
    price: float

    class Config:
        orm_mode = True
