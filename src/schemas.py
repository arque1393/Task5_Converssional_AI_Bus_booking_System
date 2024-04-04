from pydantic  import BaseModel , EmailStr


    
class User(BaseModel):
    user_id:int
    username: str
    email: str
    class Config:
        from_attribute = True

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password:str