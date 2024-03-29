from fastapi import FastAPI, UploadFile , File 
from fastapi.responses import JSONResponse
import uvicorn 
from WebApp.constants  import TMP_FILE_PATH 
from WebApp.models import Query 
# from WebApp.elements.vector_store import 
import shutil

from WebApp.elements.vector_store import VectorStore
from WebApp.elements.agents import create_agent_executer
from langchain_core.messages import AIMessage, HumanMessage


from collections import defaultdict
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
    
    return {"message":'Success'}


@app.post('/ask')
async def ask_question(query:Query):
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