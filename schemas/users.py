from pydantic import BaseModel
from typing import List

# users schemas -----
class UserBase(BaseModel):
    email : str
    username : str

class UserCreate(UserBase):
    password : str

class UserOut(UserBase):
    id : int

    class config:
        orm_mode = True


