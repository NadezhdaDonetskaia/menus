from pydantic import BaseModel


class DishCreate(BaseModel):
    title: str
    description: str
    price: str
    # submenu_id: int


class Dish(BaseModel):
    # id: str
    # submenu_id: str
    title: str
    description: str
    price: str

    class Config:
        orm_mode = True