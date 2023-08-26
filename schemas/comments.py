from pydantic import BaseModel
from typing import List
import datetime

# comment schemas -----------

class CommentBase(BaseModel):
    text : str
    user_id : int
    post_id : int

class CommentOut(CommentBase):
    id : int
    timestamp : str or datetime
    class config:
        orm_mode = True
