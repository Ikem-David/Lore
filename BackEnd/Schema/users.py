from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username : str
    email : str

class UserResponse(UserBase):
    id : int
    class Config:
        from_attributes = True

class CreateUser(UserBase):
    password : str

class LoginRequest(BaseModel):
    email : str
    password : str

class UpdateUser(BaseModel):
    username : Optional[str] = None
    email : Optional[str] = None
    password : Optional[str] = None