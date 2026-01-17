from pydantic import BaseModel,Field, field_validator

class CreateUser(BaseModel):
    email: str = Field(...)
    username: str =  (Field...)
    first_name: str
    last_name: str
    password: str = Field(...)
    role: str = Field(default='user')
    phone_number : str = Field(... )
    
    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls,value:str):
        if not value.isdigit():
            raise ValueError("Phone number must contain only digits")
        if len(value) !=10 :
            raise ValueError("Phone number must be exactly 10 digits")
        return value



class Token(BaseModel):
    access_token : str
    token_type : str