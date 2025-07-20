from fastapi import APIRouter
from app.api.v1.students import router as students_router
from app.api.v1.auth import router as auth_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(students_router, tags=["students"])
