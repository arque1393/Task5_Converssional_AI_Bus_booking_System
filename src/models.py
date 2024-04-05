from sqlalchemy import (Column, ForeignKey, 
                        JSON, Integer, String, DateTime)
from sqlalchemy.orm import relationship
from src.database import Base

from sqlalchemy.sql import func

'''This module contains All the SQLAlchemy Database Schemas or Model
'''

class User(Base): 
    __tablename__ = "user"
    user_id = Column(Integer, primary_key= True,autoincrement=True)
    username =  Column(String(100),unique=True,nullable=False)
    email = Column(String(100),unique=True, index= True, nullable= False )
    _password_hash = Column(String(200), nullable=False)
    conversation = relationship('Conversation', back_populates='user')
    

class Conversation(Base):
    __tablename__ = "conversation"    
    conversation_id = Column(Integer, primary_key= True,autoincrement=True)
    conversation_title = Column(String(100), nullable= False)
    user_id =  Column(Integer, ForeignKey('user.user_id'), nullable=False)
    history = Column(JSON, nullable=False)
    user = relationship('User', back_populates='conversation')