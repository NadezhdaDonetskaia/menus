from pydantic import BaseModel


class DishCreate(BaseModel):
    name: str
    price: float
    submenu_id: int


class DishDetail(BaseModel):
    id: int
    name: str
    price: float
