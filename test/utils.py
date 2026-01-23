from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from database import Base
from main import app
from routers.todos import get_db, get_current_user
from fastapi.testclient import TestClient
from fastapi import status
import pytest
from models import Todos, Users
from routers.auth import bycrpt_context


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


# get the current user
def override_get_current_user():
    return {"username": "adityak3", "id": 1, "role": "admin"}


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


client = TestClient(app)

# read the todo


@pytest.fixture
def test_todo():
    todo = Todos(
        title="this is the first todo",
        description="this todo creating in postgresql",
        priority=5,
        complete=True,
        owner_id=1,
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


# just like todo , we create for Users to create and test the user


@pytest.fixture
def test_users():
    user = Users(
        email="user@gmail.com",
        username="user",
        first_name="abc",
        last_name="bca",
        hashed_password=bycrpt_context.hash("testpass"),
        role="admin",
        phone_number="8273182382",
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE from users;"))
        connection.commit()
