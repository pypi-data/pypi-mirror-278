import logging
from typing import List

from bot_station.domain.bot.bot import Bot
from bot_station.domain.bot.chat_message_storage import ChatMessageStorage
from bot_station.domain.bot.model.bot_meta_info import BotMetaInfo
from bot_station.domain.bot.model.lm_call_result import CallResult
from bot_station.domain.bot.model.lm_chat_message import LMBotMessage, LmChatMessage
from bot_station.domain.bot.model.lm_chat_message import LMUserMessage
from bot_station.domain.docs.docs_library import DocsLibrary
from bot_station.domain.docs.model.document import Document
from bot_station.domain.docs.model.documents_search_result import DocumentsSearchResult
from bot_station.domain.llm.llm import LLM


class BotImpl(Bot):
    docs_library: DocsLibrary
    llm: LLM
    message_storage: ChatMessageStorage
    meta: BotMetaInfo

    """
    TODO: перенести prompt и настройки LLM в конфиг или наверх
    """
    __message_history_title = "Переписка с пользователем: "
    __relevant_docs_title = "Для ответа используй следующую информацию: "
    __user_question_title = "Сообщение пользователя: "

    def __init__(
            self,
            message_storage: ChatMessageStorage,
            docs_library: DocsLibrary,
            llm: LLM,
            meta: BotMetaInfo
    ):
        self.message_storage = message_storage
        self.docs_library = docs_library
        self.llm = llm
        self.meta = meta
        self.__is_loaded = False

    async def call(self, question: LMUserMessage) -> CallResult:
        logging.debug(f"call({question})")
        logging.debug(f"self.meta = {self.meta}")

        prompt_with_question = self.meta.prompt_intro + "\n"

        # 1. Add previous messages to prompt
        if self.meta.add_messages_history_to_prompt:
            message_history: List[LmChatMessage] = \
                await self.message_storage.get_history(chat_id=question.chat_id, limit=10)
            if len(message_history) >= 2:
                prompt_with_question = prompt_with_question + f"\n{self.__message_history_title}\n"
                for m in message_history:
                    prompt_with_question = prompt_with_question + "- " + m.text + "\n"

        # 2. Add context to prompt
        relevant_docs: List[Document] = []
        if self.meta.add_external_context_to_prompt:
            await self.docs_library.load()
            search_docs_result: DocumentsSearchResult = await self.docs_library.get_relevant_docs(
                query=question.text,
                min_score=self.meta.min_extract_relevant_docs_score,
                limit=self.meta.limit_extract_relevant_docs,
            )
            relevant_docs: List[Document] = [search_docs_result.docs[key] for key in search_docs_result.docs]
            await self.docs_library.close()
            if len(relevant_docs) > 0:
                prompt_with_question = (
                        prompt_with_question
                        + f"\n{self.__relevant_docs_title}\n"
                )
                for d in relevant_docs:
                    prompt_with_question = prompt_with_question + f"\n{d.data}"

        prompt_with_question = (prompt_with_question + f"\n{self.__user_question_title}" + question.text)

        logging.debug(f"Send message to LLM: {prompt_with_question}")
        response = await self.llm.call(prompt_with_question)
        logging.debug(f"Response: {response}")

        answer = LMBotMessage(text=response, chat_id=question.chat_id)
        await self.message_storage.add_user_message(chat_id=question.chat_id, message=question)
        await self.message_storage.add_bot_message(chat_id=question.chat_id, message=answer)

        return CallResult(answer=answer, relevant_docs=relevant_docs)
