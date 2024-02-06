from fastapi import APIRouter

user_router: APIRouter = APIRouter(prefix="/user", tags=['User'])
