from pydantic import BaseModel


class BaseMenu(BaseModel):
    title: str
    description: str

    class ConfigDict:
        from_attributes = True


class MenuChange(BaseMenu):
    pass


class MenuShow(BaseMenu):
    submenus_count: int
    dishes_count: int
