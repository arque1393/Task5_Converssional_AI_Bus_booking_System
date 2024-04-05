from pydantic  import BaseModel , EmailStr

class Query(BaseModel):
    '''Pydantic model to get Query'''
    question:str 
    
    
class ConversationDisplay (BaseModel):
    conversation_id:int
    conversation_title:str
    
    class config:
        from_attribute = True