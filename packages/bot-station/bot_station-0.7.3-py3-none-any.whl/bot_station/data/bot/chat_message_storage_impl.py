from typing import List

from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

from bot_station.domain.bot.chat_message_storage import ChatMessageStorage
from bot_station.domain.bot.model.lm_chat_message import (
    LmChatMessage,
    LMUserMessage,
    LMBotMessage,
)


class ChatMessageStorageImpl(ChatMessageStorage):
    root_message_history_path = ""

    def __init__(self, root_message_history_path: str):
        self.root_message_history_path = root_message_history_path

    async def get_history(
        self, chat_id: int | str, limit: int = 100
    ) -> List[LmChatMessage]:
        base_messages: List[BaseMessage] = self.__get_message_history(chat_id).messages
        messages: List[LmChatMessage] = []
        counter = 0
        for m in base_messages:
            if counter > limit:
                break
            if isinstance(m, HumanMessage):
                messages.append(LMUserMessage(chat_id=chat_id, text=m.content))
            if isinstance(m, AIMessage):
                messages.append(LMBotMessage(chat_id=chat_id, text=m.content))
            counter = counter + 1
        return messages

    async def add_bot_message(self, chat_id: int | str, message: LmChatMessage):
        chat_message_history = self.__get_message_history(chat_id)
        chat_message_history.add_ai_message(message.text)

    async def add_user_message(self, chat_id: int | str, message: LmChatMessage):
        chat_message_history = self.__get_message_history(chat_id)
        chat_message_history.add_user_message(message.text)

    def get_message_history(self, chat_id: int | str) -> BaseChatMessageHistory:
        return self.__get_message_history(chat_id)

    async def clear(self, chat_id: int | str):
        pass

    def __get_message_history(self, chat_id: int | str) -> SQLChatMessageHistory:
        return SQLChatMessageHistory(
            session_id=str(chat_id),
            connection_string=f"sqlite:///{self.root_message_history_path}/chat-{str(chat_id)}.db",
        )
