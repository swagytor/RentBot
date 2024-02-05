from datetime import datetime

from sqlalchemy import ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Event(Base):
    __tablename__ = "event"

    id: Mapped[int] = mapped_column(primary_key=True)
    start_time: Mapped[datetime] = mapped_column(Date)
    finish_time: Mapped[datetime] = mapped_column(Date)
    court: Mapped[int] = mapped_column(ForeignKey("court.id"))
    description: Mapped[str]
