from abc import ABC
from dataclasses import dataclass


class LmChatMessage(ABC):
    """
    @:param chat_id external connector chat id
    """

    text: str
    chat_id: int | str = None


@dataclass
class LMUserMessage(LmChatMessage):
    text: str
    chat_id: int | str


@dataclass
class LMBotMessage(LmChatMessage):
    text: str
    chat_id: int | str
