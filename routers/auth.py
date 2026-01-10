from fastapi import APIRouter,Depends,status
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


#create user
@router.post('/auth',status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency , user_request : CreateUser):
    user_model = Users(
        email = user_request.email,
        username = user_request.username,
        first_name = user_request.first_name,
        last_name = user_request.last_name,
        role = user_request.role,
        hashed_password = bycrpt_context.hash(user_request.password),
        is_active = True
    )
    db.add(user_model)
    db.commit()
    return user_model


#get all users

@router.get("/getuser")
async def getalluser(db:db_dependency):
   return db.query(Users).all()




