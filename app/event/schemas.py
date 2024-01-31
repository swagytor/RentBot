from datetime import date

from pydantic import BaseModel, Field, ConfigDict


class SEvent(BaseModel):

    description: str = Field(max_length=100, min_length=1)
    start_time: date
    finish_time: date
    court: int
    player: int
