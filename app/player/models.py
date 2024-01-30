from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Players(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    NTRP: Mapped[float]
    tg_id: Mapped[int] = mapped_column(unique=True)
    user_name_tg: Mapped[str] = mapped_column(unique=True)
    games_played_on_week: Mapped[int] = mapped_column(default=0)
    is_notification: Mapped[bool] = mapped_column(default=False)
    is_notification_changes: Mapped[bool] = mapped_column(default=False)
