from pydantic  import BaseModel , EmailStr, ValidationError, constr, validator, Field

from fastapi import HTTPException 
    
class User(BaseModel):
    user_id:int
    username: str
    email: str
    class Config:
        from_attribute = True

class UserCreate(BaseModel):
    username: str     =  Field(..., example="john_doe")
    email: EmailStr   =  Field(..., example="john@example.com")
    password:constr(min_length=8)     =  Field(..., example="your_password")
    
    @validator('password')
    def validate_password(cls, v):
        # Additional custom validation can be added here
        if not any(char.isdigit() for char in v):
            raise HTTPException(status_code=400, detail = 'Password must contain at least one digit')
        if not any(char.isalpha() for char in v):
            raise HTTPException(status_code=400, detail = 'Password must contain at least one letter')
        return v
    
    


