from fastapi import APIRouter, Depends, HTTPException, status, Path

from models import Todos
from validations.TodoRequest import TodoRequest, TodoCreate, TodoUpdate
from database import SesssionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from .auth import get_current_user


router = APIRouter(prefix="/todo", tags=["todo"])


def get_db():
    db = SesssionLocal()

    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


# get all the todos
@router.get("/")
def get_allTodo(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authenticate first"
        )
    return db.query(Todos).filter(Todos.owner == user.get("id")).all()


# get todo by todo_id
@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def getTodobyId(
    user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authenticate First"
        )
    todo_model = (
        db.query(Todos)
        .filter(Todos.owner == user.get("id"))
        .filter(Todos.id == todo_id)
        .first()
    )
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not Found")


# create todos with valid user
@router.post("/createTodo", status_code=status.HTTP_201_CREATED)
async def createTodo(
    user: user_dependency, db: db_dependency, todo_request: TodoCreate
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed"
        )
    todo_model = Todos(**todo_request.dict(), owner=user.get("id"))

    db.add(todo_model)
    db.commit()


# update the todo
@router.put("/updatetodo/{todo_id}", status_code=status.HTTP_200_OK)
async def updateTodo(
    user: user_dependency,
    db: db_dependency,
    todo_request: TodoUpdate,
    todo_id: int = Path(gt=0),
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authenticate first"
        )

    todo_model = (
        db.query(Todos)
        .filter(Todos.owner == user.get("id"))
        .filter(Todos.id == todo_id)
        .first()
    )
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    update_data = todo_request.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(todo_model, key, value)

    db.commit()
    db.refresh(todo_model)
    return todo_model  


# delete the todo
@router.delete("/deletetodo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteTodo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo_model)
    db.commit()
