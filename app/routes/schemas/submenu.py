from pydantic import BaseModel


class SubMenuCreate(BaseModel):
    title: str
    description: str


class SubMenu(BaseModel):
    # id: int
    title: str
    description: str

    class Config:
        orm_mode = True


class SubMenuDetail(BaseModel):
    title: str
    description: str
    menu_id: str
