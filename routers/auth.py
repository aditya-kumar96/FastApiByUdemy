from fastapi import APIRouter,Depends
from validations.UserRequest import CreateUser
from models import Users
from database import SesssionLocal
from passlib.context import CryptContext
from typing import Annotated
from sqlalchemy.orm import Session



router = APIRouter()
def get_db():
    db = SesssionLocal()

    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


bycrpt_context = CryptContext( schemes=["bcrypt"] , deprecated='auto')


@router.post('/auth')
async def create_user(user_request : CreateUser):
    user_model = Users(
        email = user_request.email,
        username = user_request.username,
        first_name = user_request.first_name,
        last_name = user_request.last_name,
        role = user_request.role,
        hashed_password = bycrpt_context.hash(user_request.password),
        is_active = True
    )
    return user_model



