from fastapi import APIRouter, Depends
from sqlalchemy import insert, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.court.models import Court
from app.court.schemas import SCourt
from app.database import get_async_session

router = APIRouter(
    prefix="/court",
    tags=["court"],
)


@router.post("/")
async def create_court(new_court: SCourt, se: AsyncSession = Depends(get_async_session), ):
    new_court = insert(Court).values(**new_court.model_dump())
    await se.execute(new_court)
    await se.commit()
    return {"status": "success"}


@router.delete("/court_id")
async def delete_court(court_id: int, se: AsyncSession = Depends(get_async_session)):
    query = delete(Court).where(Court.id == court_id)
    await se.execute(query)
    await se.commit()
    return {"status": "success"}


@router.get("/court_id")
async def get_court(court_id: int, se: AsyncSession = Depends(get_async_session)):
    query = select(Court).where(Court.id == court_id)
    result = await se.execute(query)
    court = result.scalars().first()
    if court:
        return court
    else:
        return {"error": "Court not found"}


@router.get("/")
async def get_all_courts(se: AsyncSession = Depends(get_async_session)):
    query = select(Court)
    result = await se.execute(query)
    courts = result.scalars().all()
    return courts
