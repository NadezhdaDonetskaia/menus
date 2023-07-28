from pydantic import BaseModel


class MenuCreate(BaseModel):
    title: str
    description: str


class Menu(BaseModel):
    # id: str
    title: str
    description: str

    class Config:
        orm_mode = True
