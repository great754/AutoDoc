from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    full_name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    full_name: str
    email: EmailStr

    class Config:
        from_attributes = True