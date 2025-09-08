from fastapi import APIRouter, Depends, HTTPException
from buscabook.models import User
from buscabook.schemas import RegisterSchema
from buscabook.database import get_session
from sqlalchemy.orm import Session
from buscabook.main import bcrypt_context

user_routers = APIRouter(
    prefix="/user",
    tags=["user"],
)

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
