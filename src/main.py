import uvicorn 
from fastapi import FastAPI

import dotenv
import os 


from src.constants  import TMP_FILE_PATH 
from src import models
from src.database import engine

from src.auth.router import auth_routers
from src.chat.router import chat_routers
from collections import defaultdict


from src.auth.utils import oauth2_scheme 
dotenv.load_dotenv()
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")


# global chat_hidtory 
chat_history:dict[str,list] = defaultdict(list)

models.Base.metadata.create_all(engine)

if not TMP_FILE_PATH.exists():
    TMP_FILE_PATH.mkdir(parents=True)

app = FastAPI()
@app.get('/')
async def root():
    return 'Use Documentation to understand the API'


app.include_router(auth_routers)
app.include_router(chat_routers)

if __name__ == '__main__':
    uvicorn.run(app,host='0.0.0.0',port=8000)
    
    

