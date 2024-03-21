from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Player(Base):
    __tablename__ = "player"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    NTRP: Mapped[str]  # changes
    tg_id: Mapped[int] = mapped_column(unique=True)
    tg_username: Mapped[str] = mapped_column(unique=True)
    games_played_on_week: Mapped[int] = mapped_column(default=0)
    is_notification: Mapped[bool] = mapped_column(default=False)
    is_notification_changes: Mapped[bool] = mapped_column(default=False)

    # event: Mapped["Event"] = relationship(viewonly=True)

    def __str__(self):
        return f"{self.name} - {self.NTRP} - {self.tg_id} - {self.tg_username} - {self.games_played_on_week} - " \
               f"{self.is_notification} - {self.is_notification_changes}"
