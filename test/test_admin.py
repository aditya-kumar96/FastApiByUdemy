from .utils import *
from routers.admin import get_db, get_current_user
from fastapi.testclient import TestClient
import main
from models import Todos

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


# read the todo if user is admin
def test_admin_read_all_authenticated(test_todo):
    response = client.get("/admin/todo")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "id": 1,
            "title": "this is the first todo",
            "description": "this todo creating in postgresql",
            "priority": 5,
            "complete": True,
            "owner_id": 1,
        }
    ]


# test the  delete todo if user is admin


def test_admin_delete_todo(test_todo):
    response = client.delete("/admin/todo/1")
    assert response.status_code == 200
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


# delete todo not found
def test_admin_delete_todo_not_found():
    response = client.delete("/admin/todo/122")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}
