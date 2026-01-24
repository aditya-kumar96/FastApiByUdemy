from .utils import *
from routers.auth import get_current_user,get_db,authenticate_user,create_access_token,SECRET_KEY,ALGORITHM
from jose import jwt
from datetime import timedelta
import pytest
from fastapi import HTTPException

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
    
    
#test create access token

def test_create_access_token():
    username = 'testuser'
    user_id = 1
    role = 'user'
    expires_delta = timedelta(days=1)
    
    token = create_access_token(username,user_id,role,expires_delta)
    
    decoded_token = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM,options={'verify_signature':False})
    
    assert decoded_token['sub'] == username
    assert decoded_token['id'] == user_id
    assert decoded_token['role'] == role
    
    
#time to check valid token or not

@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode = {'sub':'testuser','id':1,'role':'admin'}
    
    token = jwt.encode(encode,SECRET_KEY , algorithm=ALGORITHM)
    
    user = await get_current_user(token=token)
    
    assert user == {'username':'testuser','id':1,'role':'admin'}
    
@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {'role':'user'}
    token = jwt.encode(encode , SECRET_KEY , algorithm=ALGORITHM)
    
    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=token)
        
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == 'Could not validate user'
    
    
    #Testing Done