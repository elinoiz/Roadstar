from pydantic import BaseModel

class UserCreate(BaseModel):
    user_name: str
    user_pass: str

class UserResponse(BaseModel):
    user_id: int
    user_name: str

    class Config:
        orm_mode = True
