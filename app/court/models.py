from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.event.models import Event


class Court(Base):
    __tablename__ = "court"

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str]
    name: Mapped[str]

    event: Mapped[list["Event"]] = relationship(back_populates="court")

    def __str__(self):
        return f"{self.address} {self.name[:10]}"
