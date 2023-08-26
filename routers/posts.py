from fastapi import APIRouter,Depends, HTTPException, UploadFile,File
from typing import List
from sqlalchemy.orm import Session
from models import users as models
from schemas import posts as schemas
from dependencies.get_db import get_db
from fastapi.responses import JSONResponse
import datetime
from string import ascii_letters
import shutil
import random


router = APIRouter()

@router.get("/post", response_model=list[schemas.PostOut])
def get_all_post(db:Session = Depends(get_db)): 
    posts = db.query(models.Post).all()
    return posts

@router.get("/post/{post_id}")
def get_one_post(post_id:int, db:Session = Depends(get_db)): 
    post_exist = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post_exist is None:
        raise HTTPException(detail="post not found with this id", status_code=404)
    return {
        "post_exist":post_exist,
        }

image_url_types = ["url","uploaded"]
@router.post("/post", response_model=schemas.PostOut)
def create_post(post:schemas.PostBase, db: Session = Depends(get_db)):
    if post.image_url_type not in image_url_types:
        raise HTTPException(detail="image type must be url or uploaded", status_code=400)
    post = models.Post(
        image_url=post.image_url,
        image_url_type=post.image_url_type,
        caption= post.caption,
        timestamp= datetime.datetime.now(),
        user_id= post.user_id
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.post("/upload_file")
def upload_file(file:UploadFile=File(...)):
    rand_str = ''.join(random.choice(ascii_letters) for _ in range(6))
    new_name = f"_{rand_str}.".join(file.filename.rsplit(".",1))
    path_file = f"uploaded_file/{new_name}"
    with open(path_file, "w+b") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"path_file":path_file}

@router.put("/post/{post_id}")
def update_post(post_id:int,post:schemas.PostBase, db:Session = Depends(get_db)):
    if post.image_url_type not in image_url_types:
        raise HTTPException(detail="image type must be url or uploaded", status_code=400)
    post_data = {
        models.Post.image_url: post.image_url,
        models.Post.image_url_type: post.image_url_type,
        models.Post.caption: post.caption,
        models.Post.timestamp: datetime.datetime.now(),
        models.Post.user_id: post.user_id
    }
    db.query(models.Post).filter(models.Post.id == post_id).update(post_data)
    db.commit()
    return JSONResponse(content="post successfully updated")

@router.delete("/post/{post_id}")
def delete_post(post_id:int, db:Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(detail="post not found with this id", status_code=404)
    db.delete(post)
    db.commit()
    return JSONResponse(content="post successfully deleted  ")
