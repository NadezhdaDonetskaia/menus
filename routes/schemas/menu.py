from pydantic import BaseModel


class MenuCreate(BaseModel):
    name: str


class MenuDetail(BaseModel):
    id: int
    name: str
    submenus_count: int
