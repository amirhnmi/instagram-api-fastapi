from pydantic import BaseModel

class Token(BaseModel):
    access_token : str

class UserAuth(BaseModel):
    id : int
    username : str 
    email : str 

class UserRegister(BaseModel):
    email : str
    username : str
    password : str

class UserLogin(BaseModel):
    username : str
    password : str
