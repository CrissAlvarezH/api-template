from fastapi import APIRouter

from app.auth.routers import router as auth_router

router = APIRouter()


router.include_router(auth_router)
