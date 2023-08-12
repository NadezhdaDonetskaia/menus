import uuid

from sqlalchemy import UUID, Column, ForeignKey, String, func, select
from sqlalchemy.orm import column_property, relationship

from database import BaseDBModel

from .dish import Dish


class SubMenu(BaseDBModel):
    __tablename__ = 'submenus'

    id: UUID = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    menu_id: UUID = Column(UUID, ForeignKey('menus.id',
                                            ondelete='CASCADE'))
    title: str = Column(String(64), unique=True, index=True)
    description: str = Column(String(128))

    menu = relationship('Menu', back_populates='submenus')
    dishes = relationship('Dish', back_populates='submenu',
                          cascade='all, delete-orphan')

    dishes_count = column_property(
        select(
            func.count(Dish.id)).where(
            Dish.submenu_id == id).correlate_except(Dish).scalar_subquery())
