from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Menu(Base):
    __tablename__ = 'menus'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), unique=True, index=True)

    submenus = relationship("SubMenu", back_populates="menu",
                            cascade="all, delete-orphan")
