from fastapi import APIRouter, Depends, HTTPException, status, Path

from models import Todos
from validations.TodoRequest import TodoRequest, TodoCreate, TodoUpdate
from database import SesssionLocal
from sqlalchemy.orm import Session
from typing import Annotated


router = APIRouter()


def get_db():
    db = SesssionLocal()

    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


# get all the todos
@router.get("/")
def get_allTodo(db: db_dependency):
    return db.query(Todos).all()


# get todo by todo_id
@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def getTodobyId(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not Found")


# create todos
@router.post("/createTodo", status_code=status.HTTP_201_CREATED)
async def createTodo(db: db_dependency, todo_request: TodoCreate):
    todo_model = Todos(**todo_request.dict())

    db.add(todo_model)
    db.commit()


# update the todo
@router.put("/updatetodo/{todo_id}", status_code=status.HTTP_200_OK)
async def updateTodo(
    db: db_dependency, todo_request: TodoUpdate, todo_id: int = Path(gt=0)
):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
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
