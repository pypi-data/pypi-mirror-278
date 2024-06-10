from dataclasses import dataclass

from pydantic import BaseModel, Field


@dataclass
class BotCallDto(BaseModel):
    bot_id: str = Field(min_length=1, max_length=100)
    chat_id: int | str = Field()
    data: str = Field(min_length=0, max_length=10_000)
