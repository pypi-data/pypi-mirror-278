import logging

from bot_station.data.bot.bot_impl import BotImpl
from bot_station.data.bot.chat_message_storage_impl import ChatMessageStorageImpl
from bot_station.data.bot.model.qdrant_config import QdrantConfig
from bot_station.data.bot.model.yandex_cloud_config import YandexCloudConfig
from bot_station.data.docs.qdrant_docs_library import QdrantDocsLibrary
from bot_station.data.llm.yandex_gpt_llm import YandexGPTLLM
from bot_station.domain.base.const import message_history_path
from bot_station.domain.bot.bot import Bot
from bot_station.domain.bot.bot_factory import BotFactory
from bot_station.domain.bot.model.bot_meta_info import BotMetaInfo
from bot_station.domain.docs.docs_library import DocsLibrary
from bot_station.domain.llm.llm import LLM


class BotFactoryImpl(BotFactory):
    """
    Дб выставлено или config или реализация до вызова create()
    """
    yandex_cloud_config: YandexCloudConfig
    qdrant_config: QdrantConfig

    docs_library: DocsLibrary
    llm: LLM

    def __init__(self):
        self.yandex_cloud_config = None
        self.qdrant_config = None
        self.docs_library = None
        self.llm = None

    async def create(self, meta: BotMetaInfo) -> Bot:
        logging.debug(f"Create {meta}")
        if self.docs_library is None:
            self.docs_library = QdrantDocsLibrary(
                collection_name=meta.id,
                qdrant_config=self.qdrant_config
            )
        if self.llm is None:
            self.llm = YandexGPTLLM(
                yandex_cloud_config=self.yandex_cloud_config,
                temperature=meta.temperature
            )
        bot = BotImpl(
            message_storage=ChatMessageStorageImpl(root_message_history_path=message_history_path),
            llm=self.llm,
            docs_library=self.docs_library,
            meta=meta
        )
        return bot
