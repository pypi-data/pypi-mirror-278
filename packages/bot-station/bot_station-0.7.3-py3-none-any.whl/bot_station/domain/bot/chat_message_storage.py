from abc import ABC, abstractmethod
from typing import List

from langchain_core.chat_history import BaseChatMessageHistory

from bot_station.domain.bot.model.lm_chat_message import LmChatMessage


class ChatMessageStorage(ABC):

    @abstractmethod
    async def add_user_message(self, chat_id: int | str, message: LmChatMessage):
        pass

    @abstractmethod
    async def add_bot_message(self, chat_id: int | str, message: LmChatMessage):
        pass

    @abstractmethod
    async def get_history(
        self, chat_id: int | str, limit: int = 100
    ) -> List[LmChatMessage]:
        pass

    @abstractmethod
    def get_message_history(self, chat_id: int | str) -> BaseChatMessageHistory:
        pass

    @abstractmethod
    async def clear(self, chat_id: int | str):
        pass
