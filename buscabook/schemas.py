from pydantic import BaseModel

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
