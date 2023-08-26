from fastapi import APIRouter,Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import users as models
from schemas import comments as schemas
from schemas.auth import UserAuth
from routers.auth import oauth2_scheme
from dependencies.get_db import get_db
from fastapi.responses import JSONResponse
import datetime


router = APIRouter()

@router.get("/comment", response_model=list[schemas.CommentOut])
def get_all_comment(db:Session = Depends(get_db)): 
    comments = db.query(models.Comment).all()
    return comments

@router.get("/comment/{comment_id}")
def get_comment_by_post_id(comment_id:int, db:Session = Depends(get_db)): 
    comment_exist = db.query(models.Comment).filter(models.Comment.post_id == comment_id).first()
    if comment_exist is None:
        raise HTTPException(detail="comment not found with this id", status_code=404)
    return {
        "comment_exist":comment_exist,
        }


@router.post("/comment", response_model=schemas.CommentOut)
def create_comment(comment:schemas.CommentBase, db: Session = Depends(get_db)):
    comment = models.Comment(
        text = comment.text,
        timestamp= datetime.datetime.now(),
        user_id= comment.user_id,
        post_id = comment.post_id
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


@router.put("/comment/{comment_id}")
def update_comment(comment_id:int,comment:schemas.CommentBase, db:Session = Depends(get_db)):
    comment_data = {
        models.Comment.text: comment.text,
        models.Comment.timestamp: datetime.datetime.now(),
        models.Comment.user_id: comment.user_id,
        models.Comment.post_id: comment.post_id
    }
    db.query(models.Comment).filter(models.Comment.id == comment_id).update(comment_data)
    db.commit()
    return JSONResponse(content="comment successfully updated")


@router.delete("/comment/{comment_id}")
def delete_comment(comment_id:int, db:Session = Depends(get_db), current_user:UserAuth=Depends(oauth2_scheme)):
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if comment is None:
        raise HTTPException(detail="comment not found with this id", status_code=404)
    if comment.user_id == current_user.id or comment.posts.user_id == current_user.id:
        db.delete(comment)
        db.commit()
        return JSONResponse(content="comment successfully deleted  ")
    return HTTPException(detail="you can not delete this comment", status_code=status.HTTP_403_FORBIDDEN)
