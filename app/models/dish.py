from sqlalchemy import Column, String, ForeignKey, Float, UUID
from sqlalchemy.orm import relationship

from database import BaseDBModel


class Dish(BaseDBModel):
    __tablename__ = 'dishes'

    id = Column(UUID, primary_key=True, index=True)
    submenu_id = Column(UUID, ForeignKey("submenus.id"))
    title = Column(String(64), unique=True, index=True)
    description = Column(String(128))
    price = Column(Float())

    submenu = relationship("SubMenu", back_populates="dishes")
