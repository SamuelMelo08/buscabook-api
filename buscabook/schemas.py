from pydantic import BaseModel
from typing import Optional

#Esquema de parâmetros para o registro de um usuário
class RegisterSchema(BaseModel):

    name: str
    email: str
    password: str

    class Config():
        from_attributes = True

class LoginSchema(BaseModel):

    email: str
    password: str

    class Config():
        from_attributes = True

class ResponseInfoUser(BaseModel):

    id: int
    name: str
    email: str

    class Config():
        from_attributes = True

class UpdateUserSchema(BaseModel):

    name: Optional[str] = None
    email: Optional[str] = None

    class Config():
        from_attributes = True
