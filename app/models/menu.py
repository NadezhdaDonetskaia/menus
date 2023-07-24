from sqlalchemy import Column, String, UUID
from sqlalchemy.orm import relationship

from database import BaseDBModel


class Menu(BaseDBModel):
    __tablename__ = 'menus'

    id = Column(UUID, primary_key=True, index=True)
    title = Column(String(64), unique=True, index=True)
    description = Column(String(128))

    submenus = relationship("SubMenu", back_populates="menu",
                            cascade="all, delete-orphan")
