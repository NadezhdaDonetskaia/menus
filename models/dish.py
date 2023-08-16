import uuid

from sqlalchemy import UUID, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import BaseDBModel


class Dish(BaseDBModel):
    __tablename__ = 'dishes'

    id: UUID = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    submenu_id: UUID = Column(UUID, ForeignKey('submenus.id',
                                               ondelete='CASCADE'))
    title: str = Column(String(), unique=True, index=True)
    description: str = Column(String())
    price: str = Column(String(8))
    discount: int = Column(Integer())

    submenu = relationship('SubMenu', back_populates='dishes')
