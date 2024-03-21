from fastapi import APIRouter, Depends
from sqlalchemy import insert, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.player.models import Player
from app.player.schemas import SPlayer

router = APIRouter(
    prefix="/player",
    tags=["player"],
)


@router.post("/")
async def create_player(new_palayer: SPlayer, se: AsyncSession = Depends(get_async_session), ):
    new_palayer = insert(Player).values(**new_palayer.model_dump())
    await se.execute(new_palayer)
    await se.commit()
    return {"status": "success"}


@router.delete("/{player_id}")
async def delete_player(player_id: int, se: AsyncSession = Depends(get_async_session)):
    query = delete(Player).where(Player.id == player_id)
    await se.execute(query)
    await se.commit()
    return {"status": "success"}


@router.get("/")
async def get_all_players(se: AsyncSession = Depends(get_async_session)):
    query = select(Player)
    result = await se.execute(query)
    players = result.scalars().all()
    return players


@router.get("/player_id")
async def get_player(player_id: int, se: AsyncSession = Depends(get_async_session)):
    query = select(Player).filter(Player.id == player_id)
    result = await se.execute(query)
    player = result.scalars().first()
    if player:
        return player
    else:
        return "error:" "Player not found"

# @router.get("/{player_id}", response_model=SPlayer)
# async def get_player(player_id: int, se: AsyncSession = Depends(get_async_session)):
#     query = select(Player).where(Player.id == player_id)
#     result = await se.execute(query)
#     player = await result.scalar()
#     if player is None:
#         return 'Not found'
#     return player

# @router.post("/")
# async def add_specific_product(new_product: ProductCreate, session: AsyncSession = Depends(get_async_session),
#                                user: User = Depends(current_user)):
#     stmt = insert(product).values(**new_product.model_dump())
#     await session.execute(stmt)
#     await session.commit()
#     return {"status": "success"}
