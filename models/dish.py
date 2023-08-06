from sqlalchemy import UUID, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from database import BaseDBModel


class Dish(BaseDBModel):
    __tablename__ = 'dishes'

    id: UUID = Column(UUID, primary_key=True, index=True)
    submenu_id: UUID = Column(UUID, ForeignKey('submenus.id'))
    title: str = Column(String(64), unique=True, index=True)
    description: str = Column(String(128))
    price: str = Column(String(8))

    submenu = relationship('SubMenu', back_populates='dishes')
