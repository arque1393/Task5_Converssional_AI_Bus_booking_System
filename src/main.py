import uvicorn 
from fastapi import FastAPI, UploadFile , File , HTTPException, Depends
import uuid
import shutil
import dotenv
import os 
from typing import Annotated
from src.constants  import TMP_FILE_PATH 
from src.schemas import Query 
from src.ai_elements.vector_store import VectorStore, upload_on_vector_db
from src.ai_elements.agents import create_agent_executer
from src import models
from src.auth.utils import get_current_user
from langchain_core.messages import AIMessage, HumanMessage

from collections import defaultdict


from src.auth.utils import oauth2_scheme 
dotenv.load_dotenv()
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")


# global chat_hidtory 
chat_history:dict[str,list] = defaultdict(list)






if not TMP_FILE_PATH.exists():
    TMP_FILE_PATH.mkdir(parents=True)
app = FastAPI()
@app.get('/')
async def root():
    return 'Use Documentation to understand the API'
@app.post('/upload')
async def upload_file(file:UploadFile = File(...)):
    with open(TMP_FILE_PATH/file.filename, 'wb') as f : 
        shutil.copyfileobj(file.file, f)
    
    try:
        upload_on_vector_db(TMP_FILE_PATH/file.filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'{e}')
        
    return {"message":'Success'}
@app.post('/guest/login')
async def login():
    return uuid.uuid4()

@app.post('/ask', )
async def ask_question(query:Query,user:models.User = Annotated[models.user, Depends(get_current_user)]):
    
    # TODO 
    username='defaultUser'

    vs = VectorStore()
    agent_executor = create_agent_executer(vector_store=vs)
    
    response = agent_executor.invoke(
        {
            "input": query.question,
            "chat_history": chat_history[username]
        }
    )
    
    chat_history[username] += [
        HumanMessage(content=response['input']),
        AIMessage(content=response['output'])
    ]
    return {'answer': response['output']}
    
if __name__ =='__main__':
    uvicorn.run(app,host='localhost',port=8000)