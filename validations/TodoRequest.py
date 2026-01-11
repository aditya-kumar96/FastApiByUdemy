from pydantic import BaseModel,Field,field_validator
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
    
    @field_validator("title","description")
    @classmethod
    def reject_placeholder_strings(cls,value):
        if value is None:
            return value
        if value.strip().lower() == "string":
            raise ValueError("field can not be empty")
        return value
    