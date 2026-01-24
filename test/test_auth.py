from .utils import *
from routers.auth import get_current_user,get_db,authenticate_user

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


#now test the user is authenticate or not

def test_authenticate_user(test_users):
    db = TestingSessionLocal()
    
    user = authenticate_user(test_users.username,'testpass',db)
    assert user is not None
    assert user.username == test_users.username
    
    #if user is not authenticate
    non_exists_user = authenticate_user('wronguser' , 'testpass',db)
    assert non_exists_user is False
    
    #if wrong password
    
    wrong_password_user = authenticate_user(test_users.username,'password',db)
    assert wrong_password_user is False
    
    