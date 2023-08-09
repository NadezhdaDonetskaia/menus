from uuid import UUID, uuid4

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models.dish import Dish
from schemas.dish import BaseDish, DishChange, DishCreate, DishShow


class DishRepository:

    def __init__(self, session: Session = Depends(get_db)) -> None:
        self.session = session
        self.model = Dish

    def get_all(self, submenu_id: UUID) -> list[DishShow]:
        dishes = self.session.query(Dish).filter(
            Dish.submenu_id == submenu_id).all()

        return dishes

    def get_by_id(self, submenu_id: UUID, dish_id: UUID) -> DishShow:
        dish = self.session.query(Dish).filter(
            Dish.id == dish_id, Dish.submenu_id == submenu_id
        ).first()
        if not dish:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='dish not found')
        return dish

    def create(self, submenu_id: UUID, dish_data: DishChange) -> DishCreate:
        new_dish = Dish(**dish_data.model_dump(),
                        id=uuid4(),
                        submenu_id=submenu_id)
        self.session.add(new_dish)
        self.session.commit()
        self.session.refresh(new_dish)
        return new_dish

    def update(self, submenu_id: UUID,
               dish_id: UUID, dish_data: DishChange) -> BaseDish:
        dish = self.session.query(Dish).filter(
            Dish.id == dish_id, Dish.submenu_id == submenu_id).first()
        if not dish:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='dish not found')

        for key, value in dish_data.model_dump().items():
            setattr(dish, key, value)

        self.session.commit()
        self.session.refresh(dish)

        return dish

    def delete(self, submenu_id: UUID, dish_id: UUID) -> None:
        dish = self.session.query(Dish).filter(
            Dish.id == dish_id, Dish.submenu_id == submenu_id).first()
        if not dish:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='dish not found')

        self.session.delete(dish)
        self.session.commit()
