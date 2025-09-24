from typing import TYPE_CHECKING, Optional
from pydantic import BaseModel, EmailStr, Field, constr

class UserCreate(BaseModel):
    name: str
    username : str
    password: str
    email: EmailStr
    bio: Optional[str] = None
    profile_image: Optional[str] = None

class UserFetch(BaseModel):
    id: int
    name: str
    username : str
    email: EmailStr
    bio: Optional[str] = None
    profile_image: Optional[str] = None

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    name: Optional[str] = None
    username : Optional[str] = None
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    bio: Optional[str] = None
    profile_image: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

