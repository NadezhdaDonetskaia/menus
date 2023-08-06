from pydantic import BaseModel


class BaseSubMenu(BaseModel):
    title: str
    description: str

    class ConfigDict:
        from_attributes = True


class SubMenuChange(BaseSubMenu):
    pass


class SubMenuShow(BaseSubMenu):
    dishes_count: int
