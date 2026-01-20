#to test the app , we need to create a duplicate database which is similiar like production db.
#to do that , we need to mock everything from app to functionality.
#app should be inside TestClient , so pytest will understand that it is the mockup of our production level apis
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..database import Base
#create a new database
SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine= create_engine(SQLALCHEMY_DATABASE_URL , 
                      connect_args={"check_same_thread":False},
                      poolclass=StaticPool)

#create a SessionLocal

TestingSessionLocal = sessionmaker(autocommit= False , autoflush = False , bind = engine)


Base.metadata.create_all(bind=engine)

#now override the getdb

