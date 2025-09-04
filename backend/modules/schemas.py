from datetime import datetime

from pydantic import BaseModel, EmailStr, constr

# Pydantic v2 compatible config
try:
    from pydantic import ConfigDict  # v2

    V2 = True
except Exception:  # pragma: no cover
    V2 = False


class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: EmailStr
    password: constr(min_length=6, max_length=128)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    if "ConfigDict" in globals():
        model_config = ConfigDict(from_attributes=True)  # pydantic v2
    else:

        class Config:
            orm_mode = True  # pydantic v1


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
