from fastapi import FastAPI,Depends,HTTPException,status,Path
import models 
from models import Todos
from validations.TodoRequest import TodoRequest,TodoCreate,TodoUpdate
from database import engine,SesssionLocal
from sqlalchemy.orm import Session
from typing import Annotated

app= FastAPI()

models.Base.metadata.create_all(bind=engine)
def get_db():
    db = SesssionLocal()
    
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]


        
     
#get all the todos         
@app.get('/')
def get_allTodo(db:db_dependency):
    return db.query(Todos).all()

#get todo by todo_id
@app.get('/todo/{todo_id}',status_code=status.HTTP_200_OK)
async def getTodobyId(db:db_dependency,todo_id:int= Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id==todo_id ).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404,detail="Todo not Found")
    

#create todos
@app.post('/createTodo',status_code=status.HTTP_201_CREATED)
async def createTodo(db:db_dependency , todo_request:TodoCreate):
    todo_model = Todos(**todo_request.dict())
    
    db.add(todo_model)
    db.commit()
    
    
#update the todo
@app.put('/updatetodo/{todo_id}',status_code=status.HTTP_200_OK)
async def updateTodo(db:db_dependency , todo_request:TodoUpdate , todo_id:int=Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404,detail="Todo not found")
    
    update_data = todo_request.model_dump(exclude_unset=True)
    
    for key,value in update_data.items():
        setattr(todo_model,key,value)
    
    db.commit()
    db.refresh(todo_model)
    return todo_model


#delete the todo
@app.delete('/deletetodo/{todo_id}',status_code=status.HTTP_204_NO_CONTENT)
async def deleteTodo(db:db_dependency, todo_id : int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404,detail="Todo not found")
    
    db.delete(todo_model)    
    db.commit()

    
    
