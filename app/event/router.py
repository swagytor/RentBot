from fastapi import APIRouter, Depends
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.event.models import Event
from app.event.schemas import SEvent
from app.database import get_async_session

router = APIRouter(
    prefix="/event",
    tags=["event"],
)


@router.post("/")
async def create_player(new_event: SEvent, se: AsyncSession = Depends(get_async_session), ):
    new_event = insert(Event).values(**new_event.model_dump())
    await se.execute(new_event)
    await se.commit()
    return {"status": "success"}