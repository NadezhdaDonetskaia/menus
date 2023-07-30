from pydantic import BaseModel


class BaseDish(BaseModel):
    title: str
    description: str
    price: str

    class Config:
        orm_mode = True


class DishChange(BaseDish):
    pass


class DishShow(BaseDish):
    pass
