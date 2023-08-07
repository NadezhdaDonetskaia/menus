from uuid import UUID, uuid4

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models.menu import Menu
from schemas.menu import BaseMenu, MenuChange, MenuCreate, MenuShow


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

    def get_by_id(self, menu_id: UUID) -> MenuShow:
        menu = self.session.query(Menu).filter(Menu.id == menu_id).first()
        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='menu not found')
        menu.submenus_count = menu.submenus_count
        menu.dishes_count = menu.dishes_count
        return menu

    def create(self, menu_data: MenuChange) -> MenuCreate:
        new_menu = Menu(**menu_data.model_dump(), id=uuid4())
        self.session.add(new_menu)
        self.session.commit()
        self.session.refresh(new_menu)
        return new_menu

    def update(self, menu_id: UUID, menu_data: MenuChange) -> BaseMenu:
        menu = self.session.query(Menu).filter(Menu.id == menu_id).first()
        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='menu not found')

        for key, value in menu_data.model_dump().items():
            setattr(menu, key, value)

        self.session.commit()
        self.session.refresh(menu)

        return menu

    def delete(self, menu_id: UUID) -> None:
        menu = self.session.query(Menu).filter(Menu.id == menu_id).first()
        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='menu not found')

        self.session.delete(menu)
        self.session.commit()
