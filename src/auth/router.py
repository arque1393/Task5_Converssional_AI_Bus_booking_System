# FastAPI
from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
# ORM
from sqlalchemy.orm import Session
# System
from datetime import timedelta
from typing import Annotated
# Custom 
from src import schemas, models
from src.database import get_session
from src.constants import ACCESS_TOKEN_EXPIRE_MINUTES
from src.auth.utils import( is_email_or_username_taken,get_current_user,
        create_access_token, get_password_hash,authenticate_user)
from src.auth.schemas import Token

auth_routers = APIRouter()

@auth_routers.post("/user", tags=['User Auth'])
async def create(user:schemas.UserCreate,  session:Session = Depends(get_session)):    
    if validate_entity := is_email_or_username_taken(user.email,user.username, models.User,session):
        raise HTTPException(status_code=400, detail=f'{validate_entity} is already taken')    
    new_user = models.User(email = user.email,username= user.username,
                        _password_hash = get_password_hash(user.password) )  

    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")

@auth_routers.post("/login", tags=['User Auth'] )
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
        session: Session = Depends(get_session) 
    ) -> Token:
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )    
    return Token(access_token=access_token, token_type="bearer")
    
@auth_routers.get("/user", response_model=schemas.User,tags=['view'])
async def read_users_me(current_user: Annotated[schemas.User,Depends(get_current_user)]):
    return current_user