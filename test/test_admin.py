from .utils import *
from routers.admin import get_db,get_current_user
from fastapi.testclient import TestClient
import main
from models import Todos
    
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_admin_read_all_authenticated(test_todo):
        response = client.get("/admin/todo")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == [
            {   "id":1,
                "title": "this is the first todo",
                "description": "this todo creating in postgresql",
                "priority": 5,
                "complete": True,
                "owner_id": 1,
            }
        ]

