from pydantic import BaseModel


class BaseDish(BaseModel):
    title: str
    description: str
    price: str

    class ConfigDict:
        from_attributes = True


class DishChange(BaseDish):
    pass


class DishShow(BaseDish):
    pass
