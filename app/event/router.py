from fastapi import APIRouter, Depends
from sqlalchemy import insert, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from fastapi import status
from app.event.models import Event
from app.event.schemas import SEvent
from app.database import get_async_session

router = APIRouter(
    prefix="/event",
    tags=["event"],
)


@router.post("/")
async def create_event(new_event: SEvent, se: AsyncSession = Depends(get_async_session)):
    try:
        new_event_query = insert(Event).values(**new_event.model_dump())
        await se.execute(new_event_query)
        await se.commit()
        return {"status": "success"}

    except SQLAlchemyError as e:
        await se.rollback()
        return JSONResponse(content={"error": f"An error occurred: {str(e)}"},
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/")
async def get_all_events(se: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Event)
        result = await se.execute(query)
        events = result.scalars().all()
        return events

    except SQLAlchemyError as e:
        return JSONResponse(content={"error": f"An error occurred: {str(e)}"},
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/{event_id}")
async def get_event(event_id: int, se: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Event).where(Event.id == event_id)
        result = await se.execute(query)
        event = result.scalars().first()

        if event:
            return event
        else:
            return {"error": "Event not found"}

    except SQLAlchemyError as e:
        return JSONResponse(content={"error": f"An error occurred: {str(e)}"},
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/{event_id}")
async def delete_event(event_id: int, se: AsyncSession = Depends(get_async_session)):
    try:
        event = await se.get(Event, event_id)

        if event is None:
            return JSONResponse(content={"error": "Event not found"},
                                status_code=status.HTTP_404_NOT_FOUND)

        query = delete(Event).where(Event.id == event_id)
        await se.execute(query)
        await se.commit()
        return {"status": "success"}

    except SQLAlchemyError as e:
        await se.rollback()
        return JSONResponse(content={"error": f"An error occurred: {str(e)}"},
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

