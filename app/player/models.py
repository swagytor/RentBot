from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Player(Base):
    __tablename__ = "player"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    ntrp: Mapped[str]  # changes
    tg_id: Mapped[int] = mapped_column(unique=True)
    tg_username: Mapped[str] = mapped_column(unique=True)
    games_played_on_week: Mapped[int] = mapped_column(default=0)
    is_notification: Mapped[bool] = mapped_column(default=False)
    is_notification_changes: Mapped[bool] = mapped_column(default=False)
    player: Mapped[list["EventPlayer"]] = relationship("EventPlayer", back_populates="player")

    def __str__(self):
        return f"{self.name} - {self.ntrp} - {self.tg_id} - {self.tg_username} - {self.games_played_on_week} - " \
               f"{self.is_notification} - {self.is_notification_changes}"
