from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class SEvent(BaseModel):
    description: str = Field(max_length=100, min_length=1)
    start_time: datetime
    finish_time: datetime
    court_id: int
    player_id: int

    model_config = ConfigDict(from_attributes=True)
