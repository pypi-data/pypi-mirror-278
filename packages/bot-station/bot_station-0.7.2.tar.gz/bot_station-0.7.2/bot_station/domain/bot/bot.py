from abc import abstractmethod, ABC

from bot_station.domain.bot.model.bot_meta_info import BotMetaInfo
from bot_station.domain.bot.model.lm_call_result import CallResult
from bot_station.domain.bot.model.lm_chat_message import LMUserMessage
from bot_station.domain.docs.docs_library import DocsLibrary


class Bot(ABC):
    meta: BotMetaInfo
    docs_library: DocsLibrary

    @abstractmethod
    async def call(self, question: LMUserMessage) -> CallResult:
        pass
