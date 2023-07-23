from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import BaseDBModel


class Menu(BaseDBModel):
    __tablename__ = 'menus'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(64), unique=True, index=True)
    description = Column(String(128))

    submenus = relationship("SubMenu", back_populates="menu",
                            cascade="all, delete-orphan")
