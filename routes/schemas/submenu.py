from pydantic import BaseModel


class SubMenuCreate(BaseModel):
    name: str
    menu_id: int


class SubMenuDetail(BaseModel):
    id: int
    name: str
    menu_id: int
    dishes_count: int
