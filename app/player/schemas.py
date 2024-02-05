from pydantic import BaseModel, Field


class SPlayer(BaseModel):

    name: str = Field(max_length=100, min_length=1)
    NTRP: str = Field(max_length=5, min_length=1)
    tg_id: int = Field(gt=-1)
    tg_username: str = Field(max_length=100, min_length=1)
    games_played_on_week: int = Field(default=0)
    is_notification: bool = Field(default=False)
    is_notification_changes: bool = Field(default=False)
