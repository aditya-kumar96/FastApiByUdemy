from fastapi import APIRouter, Depends, status,HTTPException
from validations.UserRequest import CreateUser, Token
from models import Users
from database import SesssionLocal
from passlib.context import CryptContext
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import jwt,JWTError
from datetime import timedelta, datetime, timezone


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = "32105308db36b2871246369dda1df3edef897a418ea3e4e35ad14a8917c7cfb5"
ALGORITHM = "HS256"

bycrpt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


def get_db():
    db = SesssionLocal()

    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
form_data = Annotated[OAuth2PasswordRequestForm, Depends()]


def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bycrpt_context.verify(password, user.hashed_password):
        return False
    return user




#now we need to validate the user as well as the jwt token which shared by client 
#so for that , we create getcurrentuser function to validate the jwt token 
# create access token
def create_access_token(username: str, user_id: int, role:str, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id , "role":role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

#get current user info
async def get_current_user(token:Annotated[str,Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username : str = payload.get('sub')
        user_id : int = payload.get('id')
        user_role:str = payload.get('role')
        if username is None or user_id is None :
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Could not validate user')
        return {'username':username , 'id':user_id , 'role':user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Could not validate user')
        



# create user
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, user_request: CreateUser):
    user_model = Users(
        email=user_request.email,
        username=user_request.username,
        first_name=user_request.first_name,
        last_name=user_request.last_name,
        role=user_request.role,
        hashed_password=bycrpt_context.hash(user_request.password),
        is_active=True,
        phone_number = user_request.phone_number
    )
    db.add(user_model)
    db.commit()
    return user_model


# get all users


@router.get("/getuser")
async def getalluser(db: db_dependency):
    return db.query(Users).all()


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: form_data, db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Could not validate user')
    token = create_access_token(user.username, user.id, user.role   , timedelta(minutes=20))
    return {"access_token": token, "token_type": "Bearer"}
