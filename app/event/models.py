from datetime import date

from sqlalchemy import ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Event(Base):
    __tablename__ = "event"

    id: Mapped[int] = mapped_column(primary_key=True)
    start_time: Mapped[date] = mapped_column(Date)
    finish_time: Mapped[date] = mapped_column(Date)
    court: Mapped[int] = mapped_column(ForeignKey("court.id"))
    player: Mapped[int] = mapped_column(ForeignKey("player.id"))
    description: Mapped[str]
