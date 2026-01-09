from pydantic import BaseModel,Field
from typing import Optional



class TodoRequest(BaseModel):
    title:str=Field(min_length=3)
    description:str = Field(min_length=3)
    priority:int = Field(gt=0 , lt=6)
    complete:bool = Field(default=False)
    
    
class TodoCreate(BaseModel):
    title: str = Field(..., min_length=3)
    description: str = Field(..., min_length=3)
    priority: int = Field(..., gt=0, lt=6)
    complete: bool = Field(...)
    
    
class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3)
    description: Optional[str] = Field(None, min_length=3)
    priority: Optional[int] = Field(None, gt=0, lt=6)
    complete: Optional[bool] = None