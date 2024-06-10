from dataclasses import dataclass

from pydantic import BaseModel, Field


@dataclass
class BotInfoDto(BaseModel):
    id: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=64)
    description: str = Field(min_length=0, max_length=512)
    prompt_intro: str = Field(min_length=0, max_length=2048)
    add_external_context_to_prompt: bool = Field(True)
    add_messages_history_to_prompt: bool = Field(False)
    temperature: float = Field(0.6)
