from fastapi import APIRouter, Depends
from sqlalchemy import insert, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status

from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from app.database import get_async_session
from app.player.models import Player
from app.player.schemas import SPlayer

router = APIRouter(
    prefix="/player",
    tags=["player"],
)


@router.post("/")
async def create_player(new_player: SPlayer, se: AsyncSession = Depends(get_async_session)):
    try:
        new_player = insert(Player).values(**new_player.model_dump())
        await se.execute(new_player)
        await se.commit()

        return JSONResponse(content={"status": "success"},
                            status_code=status.HTTP_201_CREATED)
    except SQLAlchemyError as e:
        return JSONResponse(content={"error": f"An error occurred: {str(e)}"},
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/{player_id}")
async def delete_player(player_id: int, se: AsyncSession = Depends(get_async_session)):
    try:
        player = await se.get(Player, player_id)
        if player is None:
            return JSONResponse(content={"error": "Player not found"}, status_code=status.HTTP_404_NOT_FOUND)

        query = delete(Player).where(Player.id == player_id)
        await se.execute(query)
        await se.commit()

        return JSONResponse(content={"status": "success"}, status_code=status.HTTP_200_OK)
    except SQLAlchemyError as e:
        return JSONResponse(content={"error": f"An error occurred: {str(e)}"},
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/")
async def get_all_players(se: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Player)
        result = await se.execute(query)
        players = result.scalars().all()
        return players
    except SQLAlchemyError as e:
        return JSONResponse(content={"error": f"An error occurred: {str(e)}"},
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/{player_id}")
async def get_player(player_id: int, se: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Player).filter(Player.id == player_id)
        result = await se.execute(query)
        player = result.scalars().first()

        if player:
            return player
        else:
            return JSONResponse(content={"error": "Player not found"}, status_code=status.HTTP_404_NOT_FOUND)

    except SQLAlchemyError as e:
        return JSONResponse(content={"error": f"An error occurred: {str(e)}"},
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
