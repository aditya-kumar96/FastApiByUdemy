from .utils import *
from routers.auth import get_current_user,get_db

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


#now test the user is authenticate or not