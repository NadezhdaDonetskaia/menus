from pydantic import BaseModel


class BaseSubMenu(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class SubMenuChange(BaseSubMenu):
    pass


class SubMenuShow(BaseSubMenu):
    dish_count: int
