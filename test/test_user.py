from .utils import *
from routers.users import get_db, get_current_user
from fastapi import status


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


# get the users
def test_return_user(test_users):
    response = client.get("/users")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "user"
    assert response.json()["email"] == "user@gmail.com"

#change password
def test_change_password_success(test_users):
    response = client.patch("/users/change_password",json={"old_password":"testpass","new_password":"newtestpass"})
    assert response.status_code == status.HTTP_200_OK
    
    
#now to if change password not work

def test_change_password_invalid_current_password(test_users):
    response = client.patch("/users/change_password",json={"old_password":"passsss","new_password":"newtestpass"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() ==  {'detail':"Old password is incorrect"}
    
    
#change phone number test
def test_change_phone_number_success(test_users):
    response = client.put('/users/update_phonenumber',params={'phone_number':'8727191918'})
    assert response.status_code ==  status.HTTP_200_OK
    
