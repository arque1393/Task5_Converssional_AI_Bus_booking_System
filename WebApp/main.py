from fastapi import FastAPI, UploadFile , File 
from fastapi.responses import JSONResponse
import uvicorn 
from WebApp.constants  import TMP_FILE_PATH 
from WebApp.models import Query 
# from WebApp.elements.vector_store import 
import shutil

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
    
    return {'answer':query.question}
    
if __name__ =='__main__':
    uvicorn.run(app,host='localhost',port=8000)