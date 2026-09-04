from pydantic import BaseModel
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    description: str = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str = None
    completed: bool
    created_at: datetime

    class Config:
        from_attributes = True

class TaskUpdate(BaseModel):
    title: str = None
    description: str = None
    completed: bool = None

class UserCreate(BaseModel):
    username: str
    email: str
    password: str 

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    user_id : int
    created_at: datetime

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str