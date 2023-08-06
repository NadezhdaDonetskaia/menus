from uuid import UUID, uuid4

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.menu import Menu
from schemas.menu import MenuChange, MenuShow


class MenuRepository:

    def __init__(self, session: Session = Depends(get_db)):
        self.session = session
        self.model = Menu

    def get_all(self) -> list[MenuShow]:
        menus = self.session.query(self.model).all()

        for menu in menus:
            menu.submenus_count = menu.submenus_count
            menu.dishes_count = menu.dishes_count

        return menus

    def get_by_id(self, menu_id: UUID) -> Menu:
        menu = self.session.query(Menu).filter(Menu.id == menu_id).first()
        if not menu:
            raise HTTPException(status_code=404, detail='menu not found')
        return menu

    def create(self, menu_data: MenuChange) -> Menu:
        new_menu = Menu(**menu_data.model_dump(), id=uuid4())
        self.session.add(new_menu)
        self.session.commit()
        self.session.refresh(new_menu)
        return new_menu

    def update(self, menu_id: UUID, menu_data: MenuChange) -> Menu:
        menu = self.session.query(Menu).filter(Menu.id == menu_id).first()
        if not menu:
            raise HTTPException(status_code=404, detail='menu not found')

        for key, value in menu_data.model_dump().items():
            setattr(menu, key, value)

        self.session.commit()
        self.session.refresh(menu)

        return menu

    def delete(self, menu_id: UUID) -> None:
        menu = self.session.query(Menu).filter(Menu.id == menu_id).first()
        if not menu:
            raise HTTPException(status_code=404, detail='menu not found')

        self.session.delete(menu)
        self.session.commit()
