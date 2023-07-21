from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import BaseDBModel


class Menu(BaseDBModel):
    __tablename__ = 'menus'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(64), unique=True, index=True)

    submenus = relationship("SubMenu", back_populates="menu",
                            cascade="all, delete-orphan")
