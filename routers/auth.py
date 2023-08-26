from fastapi import APIRouter,Depends,HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime,timedelta
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from dependencies.get_db import get_db
from dependencies.hash import Hash
from models import users as models
from schemas import auth as schemas


hash = Hash()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "a4ccf8e58dcc5ebc6ce1637d362c2ced20f4dcc030a3e985c97d7f9dfbe29616"  # openssl rand -hex 32
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(request):
    error_credential = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid credential",
        headers={"WWW-authenticate":"bearer"})
    try:
        _dict = jwt.decode(request.access_token, SECRET_KEY, algorithms=ALGORITHM)
        username = _dict.get("sub")
        if not username:
            raise error_credential
    except JWTError:
        raise error_credential
    return username

router = APIRouter(prefix="/auth")

@router.post("/register")
def register(request:schemas.UserRegister, db: Session = Depends(get_db)):
    email_exist = db.query(models.User).filter(models.User.email == request.email).first()
    if email_exist:
        raise HTTPException(detail="Email already exist", status_code=400)
    user = models.User(
        email=request.email,
        username=request.username,
        password=hash.bcrypt(request.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login")
def login(request:schemas.UserLogin, db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if not user:
        raise HTTPException(detail="invalid credential", status_code=404)
    
    if not hash.verify(user.password, request.password):
        raise HTTPException(detail="invalid username or password", status_code=404)
    

    access_token = create_access_token(data={"sub":request.username}) 
    return {
        "access_token": access_token,
        "type_token": "bearer",
        "user_id": user.id,
        "username": user.username
    }


@router.post("/usertoken", response_model=schemas.UserAuth)
def usertoken(request:schemas.Token, db:Session=Depends(get_db)):
    current_user = get_current_user(request) 
    print(current_user)
    # user = db.query(models.User).filter(models.User.username == current_user.username).first()
    # if user is None:
    #     raise HTTPException(detail="User not found with this username", status_code=404)
    # return user


