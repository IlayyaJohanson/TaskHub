import enum
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from jose import jwt
from modules import config, db
from passlib.context import CryptContext
from sqlalchemy import Column, DateTime, Enum, Integer, String
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Роли пользователей
class UserRole(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    user = "user"


# Модель пользователя
class User(db.Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(Enum(UserRole), default=UserRole.user)
    created_at = Column(DateTime, default=datetime.utcnow)


# Хелперы
def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str):
    return pwd_context.verify(password, hashed)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=config.JWT_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, config.JWT_SECRET, algorithm="HS256")


# Регистрация
@router.post("/register")
def register(
    username: str, email: str, password: str, db_sess: Session = Depends(db.get_db)
):
    if db_sess.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(username=username, email=email, password_hash=hash_password(password))
    db_sess.add(user)
    db_sess.commit()
    db_sess.refresh(user)
    return {"id": user.id, "username": user.username}


# Логин
@router.post("/login")
def login(email: str, password: str, db_sess: Session = Depends(db.get_db)):
    user = db_sess.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token}
