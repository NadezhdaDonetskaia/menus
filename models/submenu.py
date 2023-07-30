from sqlalchemy import Column, String, ForeignKey, UUID
from sqlalchemy import func, select
from sqlalchemy.orm import column_property
from sqlalchemy.orm import relationship
from database import BaseDBModel
from .dish import Dish


class SubMenu(BaseDBModel):
    __tablename__ = 'submenus'

    id = Column(UUID, primary_key=True, index=True)
    menu_id = Column(UUID, ForeignKey("menus.id"))
    title = Column(String(64), unique=True, index=True)
    description = Column(String(128))

    menu = relationship("Menu", back_populates="submenus")
    dishes = relationship("Dish", back_populates="submenu",
                          cascade="all, delete-orphan")

    dishes_count = column_property(
       select(
           func.count(Dish.id)).where(
               Dish.submenu_id == id).correlate_except(Dish).scalar_subquery())
