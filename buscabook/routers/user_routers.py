from fastapi import APIRouter, Depends, HTTPException
from buscabook.models import User
from buscabook.schemas import RegisterSchema, LoginSchema
from buscabook.database import get_session
from sqlalchemy.orm import Session
from buscabook.config import bcrypt_context, ALGORITHM, SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from jose import jwt
from datetime import datetime, timedelta, timezone 

user_routers = APIRouter(
    prefix="/user",
    tags=["user"],
)

def authenticate_user(login_schema: LoginSchema, session : Session = Depends(get_session)):

    user = session.query(User).filter(User.email == login_schema.email).first()

    if not user:
        return False

    elif not bcrypt_context.verify(login_schema.password, user.password):
        return False
    
    else:
        return user

def create_token(user_id, duration_token = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):

    exp_date = datetime.now(timezone.utc) + duration_token

    dic_token = {
        'sub': str(user_id),
        'exp': exp_date,
    }

    token = jwt.encode(dic_token, SECRET_KEY, algorithm=ALGORITHM, )

    return token



#Rota para registrar um usuário
@user_routers.post("/register")
async def register(register_schema: RegisterSchema, session: Session = Depends(get_session) ):
    
    user = session.query(User).filter(User.email == register_schema.email).first()
    
    if user:
        raise HTTPException(status_code=400, detail="Este email já está cadastrado.")
    
    else:

        password_cry = bcrypt_context.hash(register_schema.password)

        new_user = User(name=register_schema.name, email=register_schema.email, password=password_cry)

        session.add(new_user)
        session.commit()

        return {"message": f"Usuário cadastrado com sucesso! {register_schema.email}"}


@user_routers.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(get_session)):

    user = authenticate_user(login_schema, session)

    if not user:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credencias inválidas")

    else:
        access_token = create_token(user_id=user.id)

        return {

             "access_token" : access_token,
             "token_type": "Bearer",

            } 
    

