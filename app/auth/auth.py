from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from sqlmodel import Session, select
from ..database import get_session
from ..models import User
from pydantic import BaseModel

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user_by_email(db: Session, email: str):
    statement = select(User).where(User.Email == email)
    return db.exec(statement).first()

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    email: str

class Login(BaseModel):
    email: str
    password: str

@router.post("/register", response_model=UserRead)
def register_user(user: UserCreate, session: Session = Depends(get_session)):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        Username=user.username,
        Email=user.email,
        PasswordHash=hashed_password,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.post("/login", response_model=UserRead)
def login_user(login: Login, session: Session = Depends(get_session)):
    user = get_user_by_email(session, login.email)
    if not user or not verify_password(login.password, user.PasswordHash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return user
