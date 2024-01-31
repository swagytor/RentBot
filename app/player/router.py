from fastapi import APIRouter, Depends
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.player.models import Players
from app.player.schemas import SPlayer

router = APIRouter(
    prefix="/player",
    tags=["player"],
)


@router.post("/")
async def create_player(new_palayer: SPlayer, se: AsyncSession = Depends(get_async_session), ):
    new_palayer = insert(Players).values(**new_palayer.model_dump())
    await se.execute(new_palayer)
    await se.commit()
    return {"status": "success"}

# @router.post("/")
# async def add_specific_product(new_product: ProductCreate, session: AsyncSession = Depends(get_async_session),
#                                user: User = Depends(current_user)):
#     stmt = insert(product).values(**new_product.model_dump())
#     await session.execute(stmt)
#     await session.commit()
#     return {"status": "success"}
