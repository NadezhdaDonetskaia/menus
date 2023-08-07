from uuid import UUID, uuid4

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models.submenu import SubMenu
from schemas.submenu import BaseSubMenu, SubMenuChange, SubMenuCreate, SubMenuShow


class SubMenuRepository:

    def __init__(self, session: Session = Depends(get_db)):
        self.session = session
        self.model = SubMenu

    def get_all(self, menu_id: UUID) -> list[SubMenuShow]:
        submenus = self.session.query(SubMenu).filter(
            SubMenu.menu_id == menu_id).all()

        for submenu in submenus:
            submenu.dishes_count = submenu.dishes_count

        return submenus

    def get_by_id(self, menu_id: UUID, submenu_id: UUID) -> SubMenuShow:
        submenu = self.session.query(SubMenu).filter(
            SubMenu.id == submenu_id, SubMenu.menu_id == menu_id).first()
        if not submenu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='submenu not found')
        submenu.dishes_count = submenu.dishes_count
        return submenu

    def create(self, menu_id, submenu_data: SubMenuChange) -> SubMenuCreate:
        new_submenu = SubMenu(**submenu_data.model_dump(),
                              id=uuid4(),
                              menu_id=menu_id)
        self.session.add(new_submenu)
        self.session.commit()
        self.session.refresh(new_submenu)
        return new_submenu

    def update(self, menu_id: UUID, submenu_id: UUID,
               submenu_data: SubMenuChange) -> BaseSubMenu:
        submenu = self.session.query(SubMenu).filter(
            SubMenu.id == submenu_id, SubMenu.menu_id == menu_id).first()
        if not submenu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='submenu not found')

        for key, value in submenu_data.model_dump().items():
            setattr(submenu, key, value)

        self.session.commit()
        self.session.refresh(submenu)

        return submenu

    def delete(self, menu_id: UUID, submenu_id: UUID) -> None:
        submenu = self.session.query(SubMenu).filter(
            SubMenu.id == submenu_id, SubMenu.menu_id == menu_id).first()
        if not submenu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='submenu not found')

        self.session.delete(submenu)
        self.session.commit()
