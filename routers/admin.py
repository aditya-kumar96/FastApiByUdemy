from fastapi import APIRouter, Depends, HTTPException, status, Path

from models import Todos
from validations.TodoRequest import TodoRequest, TodoCreate, TodoUpdate
from database import SesssionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from .auth import get_current_user


router = APIRouter(prefix="/admin", tags=["admin"])


def get_db():
    db = SesssionLocal()

    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]




@router.get("/todo",status_code=status.HTTP_200_OK)
async def read_all(user:user_dependency , db:db_dependency ):
    if user is None or user.get('role') != 'admin' :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Not a Admin")
    return db.query(Todos).all()

