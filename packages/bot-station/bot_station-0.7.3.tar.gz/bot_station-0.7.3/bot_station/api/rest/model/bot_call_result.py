from pydantic import BaseModel, Field

from bot_station.domain.docs.model.document import Document


class BotCallResult(BaseModel):
    pass


class BotNotFoundCallResult(BotCallResult):
    pass


class BotAnswerCallResult(BotCallResult, BaseModel):
    text: str = Field()
    relevant_docs: list[Document] = Field(default=None)
