from fastapi import FastAPI
from passlib.context import CryptContext

app = FastAPI(
    title="BuscaBook",
    description="A modern book finder",
    version="0.1.0",
)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


from buscabook.routers.book_routers import book_routers
from buscabook.routers.user_routers import user_routers

#Routers
app.include_router(book_routers)
app.include_router(user_routers)

