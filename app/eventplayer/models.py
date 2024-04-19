from typing import TYPE_CHECKING
#
from sqlalchemy import ForeignKey, Table, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


if TYPE_CHECKING:
    # Убирает предупреждения отсутствия импорта и неприятные подчеркивания
    from app.player.models import Player
    from app.event.models import Event


class EventPlayer(Base):
    __tablename__ = "event_player"

    id: Mapped[int] = mapped_column(primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("player.id"), primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("event.id"), primary_key=True)
    player: Mapped["Player"] = relationship("Player", viewonly=True)
    event: Mapped["Event"] = relationship("Event")

# event_player = Table('event_player', Base.metadata,
#                      Column('event_id', Integer, ForeignKey('event.id')),
#                      Column('player_id', Integer, ForeignKey('player.id'))
#                      )
