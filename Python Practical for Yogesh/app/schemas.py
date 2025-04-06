from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    profilepic: Optional[str]
    name: str
    cellnumber: str
    password: str
    email: str
    roleId: int

class UserResponse(BaseModel):
    id: int
    name: str
    cellnumber: str
    email: str
    profilepic: Optional[str]
    roleId: int
    created: datetime

    class Config:
        orm_mode = True

class LoginRequest(BaseModel):
    cellnumber: str
    password: str

class TokenResponse(BaseModel):
    token: str
    ttl: int
    userId: int
    created: datetime
