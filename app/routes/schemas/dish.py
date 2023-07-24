from pydantic import BaseModel


class DishCreate(BaseModel):
    title: str
    description: str
    price: str


class Dish(BaseModel):
    title: str
    description: str
    price: str

    class Config:
        orm_mode = True
