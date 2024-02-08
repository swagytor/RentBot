# from fastapi import APIRouter, Depends
# from sqlalchemy import insert
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from app.eventplayer.models import EventPlayer
# from app.eventplayer.schemas import SEventPlayer
# from app.database import get_async_session
#
# router = APIRouter(
#     prefix="/eventplayer",
#     tags=["eventplayer"],
# )
#
#
# @router.post("/")
# async def create_player(new_eventplayer: SEventPlayer, se: AsyncSession = Depends(get_async_session), ):
#     new_eventplayer = insert(EventPlayer).values(**new_eventplayer.model_dump())
#     await se.execute(new_eventplayer)
#     await se.commit()
#     return {"status": "success"}