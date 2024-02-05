from fastapi import APIRouter, Depends
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.court.models import Court
from app.court.schemas import SCourt
from app.database import get_async_session

router = APIRouter(
    prefix="/court",
    tags=["court"],
)


@router.post("/")
async def create_player(new_court: SCourt, se: AsyncSession = Depends(get_async_session), ):
    new_court = insert(Court).values(**new_court.model_dump())
    await se.execute(new_court)
    await se.commit()
    return {"status": "success"}