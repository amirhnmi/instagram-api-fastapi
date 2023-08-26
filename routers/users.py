from fastapi import APIRouter
from typing import List
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from models import users as models
from schemas import users as schemas
from dependencies.get_db import get_db
from dependencies.hash import Hash
from fastapi.responses import JSONResponse
hash = Hash()

router = APIRouter()

@router.get("/user", response_model=list[schemas.UserOut])
def get_all_user(db:Session = Depends(get_db)): 
    users = db.query(models.User).all()
    return users

@router.get("/user/{user_id}")
def get_one_user(user_id:int, db:Session = Depends(get_db)): 
    user_exist = db.query(models.User).filter(models.User.id == user_id).first()
    if user_exist is None:
        raise HTTPException(detail="User not found with this id", status_code=404)
    return {
        "user_exist":user_exist,
        }

@router.post("/user", response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate, db: Session = Depends(get_db)):
    email_exist = db.query(models.User).filter(models.User.email == user.email).first()
    if email_exist:
        raise HTTPException(detail="Email already exist", status_code=400)
    user = models.User(
        email=user.email,
        username=user.username,
        password=hash.bcrypt(user.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.put("/user/{user_id}")
def update_user(user_id:int,user:schemas.UserCreate, db:Session = Depends(get_db)):
    user_exist = db.query(models.User).filter(models.User.id == user_id).first()
    if user_exist is None:
        raise HTTPException(detail="User not found with this id", status_code=404)
    user_data = {
        models.User.email: user.email,
        models.User.username: user.username,
        models.User.password: hash.bcrypt(user.password),
    }
    db.query(models.User).filter(models.User.id == user_id).update(user_data)
    db.commit()
    return JSONResponse(content="user successfully updated")

@router.delete("/user/{user_id}")
def delete_user(user_id:int, db:Session = Depends(get_db)):
    user_exist = db.query(models.User).filter(models.User.id == user_id).first()
    if user_exist is None:
        raise HTTPException(detail="User not found with this id", status_code=404)
    db.delete(user_exist)
    db.commit()
    return JSONResponse(content="user successfully deleted  ")

