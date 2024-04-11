from pydantic import BaseModel
from typing import Annotated
# class SessionData(BaseModel):
#     username: str
    
    


class TokenResponse(BaseModel):
    message:str
    access_token: str
    token_type: str
    