from sqlalchemy import UUID, Column, String, func, select
from sqlalchemy.orm import column_property, relationship

from database import BaseDBModel

from .dish import Dish
from .submenu import SubMenu


class Menu(BaseDBModel):
    __tablename__ = 'menus'

    id = Column(UUID, primary_key=True, index=True)
    title = Column(String(64), unique=True, index=True)
    description = Column(String(128))

    submenus = relationship('SubMenu', back_populates='menu',
                            cascade='all, delete-orphan')

    submenus_count = column_property(
        select(func.count(SubMenu.id)).where(
            SubMenu.menu_id == id).correlate_except(SubMenu).scalar_subquery()
    )

    dishes_count = column_property(
        select(func.count(Dish.id)).where(Dish.submenu_id.in_(
            select(SubMenu.id).where(SubMenu.menu_id == id)
        )).correlate_except(Dish).scalar_subquery()
    )
