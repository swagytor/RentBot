from fastapi import APIRouter, Depends
from sqlalchemy import insert, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from fastapi import status
from app.court.models import Court
from app.court.schemas import SCourt
from app.database import get_async_session

router = APIRouter(
    prefix="/court",
    tags=["court"],
)


@router.post("/")
async def create_court(new_court: SCourt, se: AsyncSession = Depends(get_async_session)):
    try:
        existing_court = await se.execute(select(Court).where(Court.name == new_court.name))
        if existing_court.scalar():
            return {"status": "Court already exists"}

        new_court_query = insert(Court).values(**new_court.model_dump())
        await se.execute(new_court_query)
        await se.commit()
        return {"status": "success"}

    except SQLAlchemyError as e:
        await se.rollback()
        return JSONResponse(content={"error": f"An error occurred: {str(e)}"},
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/court_id")
async def delete_court(court_id: int, se: AsyncSession = Depends(get_async_session)):
    try:
        court = await se.get(Court, court_id)
        if court is None:
            return JSONResponse(content={"error": "Court not found"}, status_code=status.HTTP_404_NOT_FOUND)

        query = delete(Court).where(Court.id == court_id)
        await se.execute(query)
        await se.commit()

    except SQLAlchemyError as e:
        await se.rollback()
        return JSONResponse(content={"error": f"An error occurred: {str(e)}"},
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/court_id")
async def get_court(court_id: int, se: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Court).where(Court.id == court_id)
        result = await se.execute(query)
        court = result.scalars().first()

        if court:
            return court
        else:
            return {"error": "Court not found"}

    except SQLAlchemyError as e:
        return JSONResponse(content={"error": f"An error occurred: {str(e)}"},
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/")
async def get_all_courts(se: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Court)
        result = await se.execute(query)
        courts = result.scalars().all()
        return courts

    except SQLAlchemyError as e:
        return JSONResponse(content={"error": f"An error occurred: {str(e)}"},
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

