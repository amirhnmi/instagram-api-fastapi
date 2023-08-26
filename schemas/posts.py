from pydantic import BaseModel
from typing import List
from schemas.comments import CommentOut

#post schema -------

class PostBase(BaseModel):
    image_url : str
    image_url_type : str
    caption : str
    user_id : int


class PostOut(PostBase):
    id : int
    comments : List[CommentOut]

    class config:
        orm_mode = True

