from dependencies.database import Base
from sqlalchemy import Column,String,Integer,Boolean,ForeignKey, DateTime
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    username = Column(String)
    password = Column(String)
    posts = relationship("Post", back_populates="users")

class Post(Base):
    __tablename__="posts"

    id = Column(Integer, primary_key=True)
    image_url = Column(String)
    image_url_type = Column(String)
    caption = Column(String)
    timestamp = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))
    users = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="posts")

class Comment(Base):
    __tablename__="comments"

    id = Column(Integer, primary_key=True)
    text = Column(String)
    timestamp = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    users = relationship("User")
    posts = relationship("Post", back_populates="comments")