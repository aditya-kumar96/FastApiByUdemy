from fastapi import FastAPI
import models

from database import engine
from sqlalchemy.orm import Session

from routers import auth, todos,admin,users



app = FastAPI()


@app.get("/healthy")
async def health_check():
    return {
        'status':"Healthy"
    }
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

models.Base.metadata.create_all(bind=engine)
