from fastapi import APIRouter

book_routers = APIRouter(
    prefix="/books",
    tags=["books"]
)