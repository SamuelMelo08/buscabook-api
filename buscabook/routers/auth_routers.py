from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from buscabook.models import User
from buscabook.schemas import RegisterSchema, LoginSchema, ResponseInfoUser, UpdateUserSchema
from buscabook.database import get_session
from buscabook.dependencies import verify_token
from sqlalchemy.orm import Session
from buscabook.config import bcrypt_context, ALGORITHM, SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from jose import jwt
from datetime import datetime, timedelta, timezone 

auth_routers = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


def authenticate_user(email: str, password: str, session : Session = Depends(get_session)):

    user = session.query(User).filter(User.email == email).first()

    if not user:
        return False

    elif not bcrypt_context.verify(password, user.password):
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


@auth_routers.post("/register")
async def register(register_schema: RegisterSchema, session: Session = Depends(get_session) ):
    """Rota para registrar um usuário."""
    
    user = session.query(User).filter(User.email == register_schema.email).first()
    
    if user:
        raise HTTPException(status_code=400, detail="Este email já está cadastrado.")
    
    else:

        password_cry = bcrypt_context.hash(register_schema.password)

        new_user = User(name=register_schema.name, email=register_schema.email, password=password_cry)

        session.add(new_user)
        session.commit()

        return {"message": f"Usuário cadastrado com sucesso! {register_schema.email}"}


@auth_routers.post("/login")
async def login(login_schema: LoginSchema , session: Session = Depends(get_session)):
    """Rota para logar com uma conta cadastrada."""

    user = authenticate_user(login_schema.email , login_schema.password, session)

    if not user:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credencias inválidas")

    else:
        access_token = create_token(user_id=user.id)

        return {

             "access_token" : access_token,
             "token_type": "Bearer",

            } 


@auth_routers.post("/login-form", include_in_schema=False)
async def login(form_data: OAuth2PasswordRequestForm = Depends() , session: Session = Depends(get_session)):
    """Rota para logar no swagger."""

    user = authenticate_user(form_data.username, form_data.password, session)

    if not user:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credencias inválidas")

    else:
        access_token = create_token(user_id=user.id)

        return {

             "access_token" : access_token,
             "token_type": "Bearer",

            } 

@auth_routers.get("/info-user", response_model=ResponseInfoUser)
async def info_user(user: User = Depends(verify_token)):

    return user


@auth_routers.put("/update-user")
async def update_user(update_schema: UpdateUserSchema, user: User = Depends(verify_token), session: Session = Depends(get_session)):

    if update_schema.name and update_schema.name != "string":
        user.name = update_schema.name

    if update_schema.email and update_schema.email != "string":
        user.email = update_schema.email
    
    session.commit()

    return { 
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }


@auth_routers.delete("/delete-user")
async def delete_user(user: User = Depends(verify_token), session: Session = Depends(get_session)):
    """Rota para deletar um usuário"""

    session.delete(user)
    session.commit()
