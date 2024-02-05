from pydantic import BaseModel, Field


class SCourt(BaseModel):

    address: str = Field(max_length=100, min_length=1)
    name: str = Field(max_length=100, min_length=1)
