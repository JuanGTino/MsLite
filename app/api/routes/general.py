from fastapi import APIRouter, Depends, Request
from typing import Any

from app.deps import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.GET.tanques_precios import get_tanques_precios

router = APIRouter()

@router.get("/tanquesprecios")
async def tanques_precios(request: Request, db: AsyncSession = Depends(get_db)):
    host = request.headers.get("host")
    db_name = request.headers.get("x-database")
    return await get_tanques_precios(db, host, db_name)