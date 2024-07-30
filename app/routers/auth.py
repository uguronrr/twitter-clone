from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from passlib.context import CryptContext
from sqlmodel import Session, select
from ..database import get_session
from ..models import User
from pydantic import BaseModel
from starlette import status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta


router = APIRouter()
SECRET_KEY = "197b2c37c658bed93fe80344fe73b806947a65e35461e54a2a52e5df45684gs3"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="auth/token")

class UserCreate(BaseModel):
    Username: str
    Email: str
    Password: str

class token(BaseModel):
    access_token: str
    token_type: str

class UserRead(BaseModel):
    UserID: int
    Username: str
    Email: str
    ProfilePicture: str = None
    Bio: str = None
    CreatedAt: str

class Login(BaseModel):
    Email: str
    Password: str

db_dependancy = Depends(get_session)
    

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, session: Session = db_dependancy):
        hashed_password = bcrypt_context.hash(user.Password)
        db_user = User(
            Username=user.Username,
            Email=user.Email,
            PasswordHash=hashed_password,
        )
        session.add(db_user)
        session.commit()

@router.post("/login", response_model=token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = db_dependancy):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(user.Username, expires_delta=access_token_expires)
    
def authenticate_user(username: str, password: str, session: Session):
    user = session.exec(select(User).where(User.Username == username)).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.PasswordHash):
          return False
    return user

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt