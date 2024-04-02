from pydantic  import BaseModel 

class Query(BaseModel):
    '''Pydantic model to get Query'''
    question:str 
    