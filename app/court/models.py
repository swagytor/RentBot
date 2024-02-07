from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Court(Base):
    __tablename__ = "court"

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str]
    name: Mapped[str]

    def __str__(self):
        return f"{self.address} {self.name[:10]}"
