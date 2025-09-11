from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

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

