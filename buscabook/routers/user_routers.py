from fastapi import APIRouter

user_routers = APIRouter(
    prefix="/user",
    tags="user",
)