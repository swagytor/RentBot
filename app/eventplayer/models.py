from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    # Убирает предупреждения отсутствия импорта и неприятные подчеркивания
    from app.player.models import Player
    from app.event.models import Event


class EventPlayer(Base):
    __tablename__ = "event_player"

    id: Mapped[int] = mapped_column(primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("player.id"))
    event_id: Mapped[int] = mapped_column(ForeignKey("event.id"))
    player: Mapped["Player"] = relationship(back_populates="player")
    event: Mapped["Event"] = relationship(back_populates="event")


    def __str__(self):
        return f"{self.player} - {self.event}"