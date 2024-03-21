from fastapi import APIRouter, Depends
from sqlalchemy import insert, select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.event.models import Event
from app.event.schemas import SEvent
from app.database import get_async_session

router = APIRouter(
    prefix="/event",
    tags=["event"],
)


@router.post("/")
async def create_event(new_event: SEvent, se: AsyncSession = Depends(get_async_session), ):
    new_event = insert(Event).values(**new_event.model_dump())
    await se.execute(new_event)
    await se.commit()
    return {"status": "success"}


@router.get("/")
async def get_all_events(se: AsyncSession = Depends(get_async_session)):
    query = select(Event)
    result = await se.execute(query)
    events = result.scalars().all()
    return events


@router.get("/event_id")
async def get_event(event_id: int, se: AsyncSession = Depends(get_async_session)):
    query = select(Event).where(Event.id == event_id)
    result = await se.execute(query)
    event = result.scalars().first()
    if event:
        return event
    else:
        return {"error": "Event not found"}


@router.delete("/event_id")
async def delete_event(event_id: int, se: AsyncSession = Depends(get_async_session)):
    query = delete(Event).where(Event.id == event_id)
    await se.execute(query)
    await se.commit()
    return {"status": "success"}
