from pydantic import BaseModel

class SessionData(BaseModel):
    username: str
    
    
class Token(BaseModel):
    access_token: str
    token_type: str