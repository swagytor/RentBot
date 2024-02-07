from datetime import datetime

from pydantic import BaseModel, Field


class SEvent(BaseModel):
    description: str = Field(max_length=100, min_length=1)
    start_time: datetime
    finish_time: datetime
    court: int
