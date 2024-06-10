from pydantic import BaseModel, Field


class BotCreationResult(BaseModel):
    id: str = Field(min_length=1, max_length=100)
