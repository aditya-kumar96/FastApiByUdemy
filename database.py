from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Aditya%40123@localhost:5432/TodoApplicationDatabase"
#need to update the password

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SesssionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)

Base = declarative_base()