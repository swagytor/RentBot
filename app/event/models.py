from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.player.models import Player
    from app.court.models import Court


class Event(Base):
    __tablename__ = "event"

    id: Mapped[int] = mapped_column(primary_key=True)
    court_id = mapped_column(ForeignKey("court.id"))
    player_id = mapped_column(ForeignKey("player.id"))
    start_time: Mapped[datetime] = mapped_column(DateTime)
    finish_time: Mapped[datetime] = mapped_column(DateTime)
    description: Mapped[str]

    player: Mapped["Player"] = relationship(back_populates="event")
    court: Mapped["Court"] = relationship(back_populates="event")

    def __str__(self):
        return f"{self.start_time} - {self.finish_time} - {self.court} - {self.description} - {self.player}"
