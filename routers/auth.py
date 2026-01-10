from fastapi import APIRouter
from validations.UserRequest import CreateUser
from models import Users


router = APIRouter()


@router.post('/auth')
async def create_user(user_request : CreateUser):
    user_model = Users(
        email = user_request.email,
        username = user_request.username,
        first_name = user_request.first_name,
        last_name = user_request.last_name,
        role = user_request.role,
        hashed_password = user_request.password,
        is_active = True
    )
    return user_model



