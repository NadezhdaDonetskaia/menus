from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship


Base = declarative_base()


class Dish(Base):
    __tablename__ = 'dishes'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    submenu_id = Column(Integer, ForeignKey("submenus.id"))
    title = Column(String(64), index=True)
    description = Column(String(128))
    price = Column(Float())

    submenu = relationship("SubMenu", back_populates="dishes")
