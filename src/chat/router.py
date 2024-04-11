# FastAPI
from fastapi import (APIRouter,Depends,
        HTTPException,UploadFile , File , HTTPException, Depends)
# Langchain 
from langchain_core.messages import AIMessage, HumanMessage
# ORM
from sqlalchemy.orm import Session
# System
from typing import Annotated,List,Dict
import shutil
import json
# Custom 
from src import schemas, models
from src.database import get_session
from src.constants import TMP_FILE_PATH
from src.auth.utils import get_current_user
from src.chat.schemas import Query
from src.ai_elements.vector_store import upload_on_vector_db, VectorStore 
from src.ai_elements.agents import create_agent_executer
from src.chat.schemas import (ConversationInfo,
        ConversationDisplay,InitConversation,Message)
from src.chat.utils import json_to_chat_history,chat_history_to_json
from src.ai_elements.prompts import  title_prompt_template
from src.ai_elements.llm import gorq_llm

chat_routers = APIRouter()

@chat_routers.post('/upload')
async def upload_file(file:UploadFile = File(...)):
    with open(TMP_FILE_PATH/file.filename, 'wb') as f : 
        shutil.copyfileobj(file.file, f)
    try:
        upload_on_vector_db(TMP_FILE_PATH/file.filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'{e}')
    finally:
        (TMP_FILE_PATH/file.filename).unlink()
    return {"message":'Success'}




@chat_routers.get('/conversation/',response_model=List[ConversationInfo],tags=['chat'] )
async def get_chat(current_user: Annotated[schemas.User, Depends(get_current_user)],
                session:Session=Depends(get_session)):
    try:
        conversation_list = session.query(models.Conversation).filter(
                    models.Conversation.user_id==current_user.user_id).all()    
        return conversation_list
    except Exception as e:
        raise HTTPException(status_code=500, detail= f'{e}')



@chat_routers.get('/conversation/all',tags=['chat'],response_model=list[ConversationDisplay])
async def get_all_conversation(current_user: Annotated[schemas.User, Depends(get_current_user)],
                session:Session=Depends(get_session)):
    try:
        if conversation_list := session.query(models.Conversation)                                          \
                    .filter(models.Conversation.user_id == current_user.user_id).all():
            return [dict(
                # ConversationDisplay(
                    conversation_id =  conversation.conversation_id,
                    conversation_title = conversation.conversation_title,
                    history = [json.loads(conv) for conv in conversation.history],                    
                    ) for conversation in conversation_list ]
        else:
            raise HTTPException(status_code=404, detail = "No Conversation is found")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f'{e}')



@chat_routers.get('/conversation/{conversation_id}',tags=['chat'], response_model=ConversationDisplay)
async def get_chat(conversation_id:int,
                current_user: Annotated[schemas.User, Depends(get_current_user)],
                session:Session=Depends(get_session)):
    try:
        if conversation := session.query(models.Conversation).filter(
                models.Conversation.user_id == current_user.user_id).filter(
                models.Conversation.conversation_id==conversation_id).first():
            return dict(
        # ConversationDisplay(
                conversation_id=conversation_id,
                conversation_title=conversation.conversation_title,
                history=[json.loads(conv) for conv in conversation.history])
        else:
            raise HTTPException(status_code=404, detail = "No Conversation is found")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f'{e}')

@chat_routers.patch('/conversation/{conversation_id}',tags=['chat'], response_model=Message)
async def update_title(conversation_id: int, title: str, 
            current_user:Annotated[schemas.User, Depends(get_current_user)] ,
            session: Session = Depends(get_session)):
    try:
        conversation=filter(models.Conversation.conversation_id == conversation_id).first()
    except Exception as e: 
        return HTTPException(status_code=404, detail=f'{e}')
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    if conversation.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="You don't have permission to delete this conversation")  
    conversation.conversation_title = title
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return {"message":"success"}

@chat_routers.post('/conversation',response_model=InitConversation,tags=['chat'] )
async def ask_question( query:Query, 
            current_user: Annotated[schemas.User,Depends(get_current_user)],
            conversation_id : int | None= None ,session:Session=Depends(get_session)):
    vs = VectorStore()
    agent_executor = create_agent_executer(vector_store=vs)   
    if not conversation_id :
        llm_chain = title_prompt_template|gorq_llm
        response = llm_chain.invoke( query.question )
        title = response.content
        response = agent_executor.invoke({"input": query.question})
        chat_history = [
            HumanMessage(content=response['input']),
            AIMessage(content=response['output'])
        ]
        chat_history_json = chat_history_to_json(chat_history)
        conversation = models.Conversation(conversation_title=title, 
                    user_id=current_user.user_id , history=chat_history_json, )     
    else : 
        conversation = session.query(models.Conversation).filter(
                models.Conversation.conversation_id==conversation_id and
                models.Conversation.user_id == current_user.user_id).first()    
        # print(type(conversation.history[0]))
        chat_history = json_to_chat_history(conversation.history)
        response = agent_executor.invoke(
            {
                "input": query.question,
                "chat_history": chat_history
            }
        )        
        chat_history+= [
            HumanMessage(content=response['input']),
            AIMessage(content=response['output'])
        ]        
        chat_history_json = chat_history_to_json(chat_history)
        conversation.history = chat_history_json
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return InitConversation(answer= response['output'],
            conversation_id=conversation.conversation_id,
            conversation_title=conversation.conversation_title)


@chat_routers.delete('/conversation/{conversation_id}',tags=['chat'], response_model=Message)
async def get_chat(conversation_id:int,
                current_user: Annotated[schemas.User, Depends(get_current_user)],
                session:Session=Depends(get_session)):
    conversation = session.query(models.Conversation).filter(models.Conversation.conversation_id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    if conversation.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="You don't have permission to delete this conversation")
    session.delete(conversation)
    session.commit()
    return {"message":"success"}