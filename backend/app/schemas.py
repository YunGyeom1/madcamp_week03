# schemas.py
from pydantic import BaseModel, EmailStr

class UserRegister(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class LikeRequest(BaseModel):
    user_id: int
    product_id: int

class StopListeningRequest(BaseModel):
    user_id: int
    artwork_id: int
    progress: float