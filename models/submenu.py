from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


Base = declarative_base()


class SubMenu(Base):
    __tablename__ = 'submenus'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    menu_id = Column(Integer, ForeignKey("menus.id"))
    title = Column(String(64), index=True)
    description = Column(String(128))

    menu = relationship("Menu", back_populates="submenus")
    dishes = relationship("Dish", back_populates="submenu",
                          cascade="all, delete-orphan")
