from fastapi import APIRouter, Depends, HTTPException, status, Path

from models import Todos, Users
from validations.TodoRequest import TodoRequest, TodoCreate, TodoUpdate
from validations.ChangePasswordRequest import ChangePasswordRequest
from database import SesssionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from .auth import get_current_user
from passlib.context import CryptContext


router = APIRouter(prefix="/users", tags=["users"])


# get the database
def get_db():
    db = SesssionLocal()

    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bycrpt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bycrpt_context.verify(plain_password, hashed_password)


def get_password_hashed(password: str) -> str:
    return bycrpt_context.hash(password)


# get user
@router.get("/", status_code=status.HTTP_200_OK)
async def getuser(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="please login first"
        )
    return db.query(Users).filter(Users.id == user.get("id")).first()


# change the password of user
@router.patch("/change_password", status_code=status.HTTP_200_OK)
async def changepassword(
    user: user_dependency, db: db_dependency, password_data: ChangePasswordRequest
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="please login first"
        )
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()

    if user_model is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="user not found"
        )
    # verify old password

    if not verify_password(password_data.old_password, user_model.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Old password is incorrect",
        )
    # update and hashed new password
    user_model.hashed_password = get_password_hashed(password_data.new_password)
    db.commit()

    return {"message": "Password changed successfully"}


@router.put("/update_phonenumber", status_code=status.HTTP_200_OK)
async def updatephonenumber(
    user: user_dependency, db: db_dependency, phone_number: str
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="please login first"
        )

    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    if user_model is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="user not found"
        )

    user_model.phone_number = phone_number
    db.commit()
    return {"message": "Phone Number Update successfully", "data": user_model}
