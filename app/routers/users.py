from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import get_session

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_session)):
    db_user = models.User(user_name=user.user_name, user_pass=user.user_pass)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/", response_model=List[schemas.UserResponse])
def read_users(db: Session = Depends(get_session)):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=404, detail="Пользователи не найдены")
    return users

@router.get("/{username}", response_model=schemas.UserResponse)
def read_user_by_username(username: str, db: Session = Depends(get_session)):
    user = db.query(models.User).filter(models.User.user_name == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

@router.delete("/{user_id}", response_model=schemas.UserResponse)
def delete_user(user_id: int, db: Session = Depends(get_session)):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    db.delete(user)
    db.commit()
    return user
