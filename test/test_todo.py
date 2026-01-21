# to test the app , we need to create a duplicate database which is similiar like production db.
# to do that , we need to mock everything from app to functionality.
# app should be inside TestClient , so pytest will understand that it is the mockup of our production level apis
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from database import Base
from main import app 
from routers.todos import get_db,get_current_user
from fastapi.testclient import TestClient
from fastapi import status
# create a new database
SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# create a SessionLocal

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)

# now override the getdb


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

#get the current user
def override_get_current_user():
    return {"username": "adityak3", "id": 1}


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


client = TestClient(app)


def test_read_all_authenticated():
    response = client.get("/todo/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []