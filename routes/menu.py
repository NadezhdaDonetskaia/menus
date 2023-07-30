from typing import List
import uuid
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .schemas.menu import MenuChange, MenuShow
from models.menu import Menu
from database import get_db

router = APIRouter()

db: Session = Depends(get_db)


@router.get('/api/v1/menus', response_model=List[MenuShow])
def get_menus(db=db):
    menus = db.query(Menu).all()

    for menu in menus:
        menu.submenus_count = menu.submenus_count
        menu.dishes_count = menu.dishes_count

    return menus


@router.post('/api/v1/menus', status_code=201)
def create_menu(menu_data: MenuChange, db=db):
    new_menu = Menu(**menu_data.dict(), id=uuid.uuid4())
    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)
    return new_menu


@router.get("/api/v1/menus/{menu_id}")
def get_menu(menu_id: str, db=db):
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="menu not found")
    return menu


@router.patch("/api/v1/menus/{menu_id}")
def update_menu(menu_id: str,
                menu_data: MenuChange,
                db=db):
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="menu not found")

    for key, value in menu_data.dict().items():
        setattr(menu, key, value)

    db.commit()
    db.refresh(menu)

    return menu


@router.delete("/api/v1/menus/{menu_id}")
def delete_menu(menu_id: str, db=db):
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="menu not found")

    db.delete(menu)
    db.commit()
