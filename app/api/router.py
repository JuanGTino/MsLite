from fastapi import APIRouter
from app.api.routes import general

router = APIRouter()

router.include_router(general.router, prefix="/general", tags=["general"])
