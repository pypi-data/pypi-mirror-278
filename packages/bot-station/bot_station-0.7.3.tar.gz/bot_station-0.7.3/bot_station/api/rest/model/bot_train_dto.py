from dataclasses import dataclass

from pydantic import BaseModel, Field


@dataclass
class BotTrainDto(BaseModel):
    bot_id: str = Field(min_length=1, max_length=100)
    data: str = Field(min_length=0, max_length=10_000)
    source_link: str | None = Field(min_length=0, max_length=1000)
    metadata: dict[str, str] = Field(default_factory=dict)
