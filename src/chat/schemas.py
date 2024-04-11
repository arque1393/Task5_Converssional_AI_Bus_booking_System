from pydantic  import BaseModel , EmailStr , validator 
from typing import Sequence,Any
import json
class Query(BaseModel):
    '''Pydantic model to get Query'''
    question:str 
    

class ConversationInfo (BaseModel):
    conversation_id:int
    conversation_title:str
    class config:
        from_attribute = True
class Message(BaseModel):
    content:str                                     
    type:str    
    class config:
        from_attribute = True        
class ConversationDisplay(BaseModel):
    conversation_id:int
    conversation_title:str
    history:list[Message]
class InitConversation(BaseModel):
    answer: str
    conversation_title : str
    conversation_id : int
class ExistConversation(BaseModel):
    answer: str
    conversation_id : int

class Message(BaseModel):
    message:str