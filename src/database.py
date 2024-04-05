import dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
'''This module contains Database Configuration Variable, Database connection String database engine and database access utility  '''
dotenv.load_dotenv()
# # # SQLite setup
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# # PostgreSQL Database Configuration
USER = os.getenv('DATABASE_USER')
DATABASE = os.getenv('DATABASE_NAME')
PASSWORD = os.getenv('DATABASE_PASSWORD')
HOST = os.getenv('DATABASE_HOST')
PORT = os.getenv('DATABASE_PORT')

# PostgreSQL Connection
SQLALCHEMY_DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# BASE ORM Model 
Base = declarative_base()


# DB Utilities 
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        




