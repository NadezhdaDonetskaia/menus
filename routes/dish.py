from typing import List
import uuid
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .schemas.dish import DishChange, DishShow
from models.dish import Dish
from database import get_db

router = APIRouter()
db: Session = Depends(get_db)


@router.get(
        '/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
        response_model=List[DishShow])
def get_dishes(submenu_id: str, db=db):
    dishes = db.query(Dish).filter(
        Dish.submenu_id == submenu_id).all()

    return dishes


@router.post('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
             status_code=201)
def create_dish(submenu_id: str,
                dish_data: DishChange,
                db=db):
    new_dish = Dish(**dish_data.model_dump(),
                    id=uuid.uuid4(),
                    submenu_id=submenu_id)
    db.add(new_dish)
    db.commit()
    db.refresh(new_dish)
    return new_dish


@router.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def get_dish(dish_id: str,
             submenu_id: str,
             db=db):
    dish = db.query(Dish).filter(
        Dish.id == dish_id, Dish.submenu_id == submenu_id
    ).first()
    if not dish:
        raise HTTPException(status_code=404, detail="dish not found")
    return dish


@router.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
def update_dish(dish_id: str,
                submenu_id: str,
                dish_data: DishChange,
                db=db):
    dish = db.query(Dish).filter(
        Dish.id == dish_id, Dish.submenu_id == submenu_id).first()
    if not dish:
        raise HTTPException(status_code=404, detail="dish not found")

    for key, value in dish_data.model_dump().items():
        setattr(dish, key, value)

    db.commit()
    db.refresh(dish)

    return dish


@router.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
def delete_submenu(submenu_id: str,
                   dish_id: str,
                   db=db):
    dish = db.query(Dish).filter(
        Dish.id == dish_id, Dish.submenu_id == submenu_id).first()
    if not dish:
        raise HTTPException(status_code=404, detail="dish not found")

    db.delete(dish)
    db.commit()
