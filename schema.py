from pydantic import BaseModel, EmailStr
from enum import Enum

class Role(str, Enum):
    ops = "ops"
    client = "client"

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class User(BaseModel):
    name: str
    email: EmailStr
    role: Role
    verified: bool
