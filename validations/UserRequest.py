from pydantic import BaseModel

class CreateUser(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    role: str



class Token(BaseModel):
    access_token : str
    token_type : str