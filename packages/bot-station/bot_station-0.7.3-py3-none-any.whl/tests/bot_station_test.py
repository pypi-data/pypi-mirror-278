import unittest

from bot_station.data.bot.bot_factory_impl import BotFactoryImpl
from bot_station.data.bot.model.qdrant_config import QdrantConfig
from bot_station.data.bot.model.yandex_cloud_config import YandexCloudConfig
from bot_station.data.docs.qdrant_docs_library import QdrantDocsLibrary
from bot_station.di.bot_station_module import BotStationModule
from bot_station.domain.bot.model.bot_meta_info import BotMetaInfo
from bot_station.domain.bot.model.lm_chat_message import LMUserMessage
from bot_station.domain.bot_station.bot_station import BotStation
from bot_station.domain.docs.model.documents_search_result import DocumentsSearchResult
from tests.mock_llm import MockLLM


class BotStationTest(unittest.IsolatedAsyncioTestCase):
    yandex_cloud_config = YandexCloudConfig(
        api_key="",
        folder_id="",
        model_name="",
        model_version="rc"
    )
    qdrant_config = QdrantConfig(
        qdrant_url=None,
        qdrant_db_path=".data/qdrant",
    )
    docs_library = QdrantDocsLibrary(
        collection_name="",
        qdrant_config=qdrant_config,
    )
    llm = MockLLM()
    bot_factory = BotFactoryImpl()
    bot_factory.docs_library = docs_library
    bot_factory.llm = llm

    BotStationModule.provide_bot_factory(bot_factory)
    bot_station: BotStation = BotStationModule.create_bot_station(yandex_cloud_config=yandex_cloud_config,
                                                                  qdrant_config=qdrant_config)

    bot_id = "test"
    meta_info = BotMetaInfo(
        name="Nutritio",
        description="Бот, отвечающий на вопросы о правильном питании",
        prompt_intro="Ты - нутрициолог, помогающий выстроить правильное питание.",
        add_external_context_to_prompt=True,
        add_messages_history_to_prompt=False,
        temperature=0.1,
        id=bot_id,
        min_extract_relevant_docs_score=0.8
    )

    async def asyncSetUp(self):
        await self.__delete_bot(self.bot_id)

    async def asyncTearDown(self):
        await self.__delete_bot(self.bot_id)

    async def test_create_bot(self):
        await self.bot_station.create(self.meta_info)
        bot = await self.bot_station.get_bot(self.bot_id)

        self.assertIsNotNone(bot)
        self.assertEqual(self.meta_info.min_extract_relevant_docs_score, bot.meta.min_extract_relevant_docs_score)
        await self.__delete_bot(self.bot_id)

    async def test_train_bot(self):
        await self.bot_station.create(self.meta_info)
        bot = await self.bot_station.get_bot(self.bot_id)
        await bot.docs_library.load()

        doc = await bot.docs_library.create_document(
            data="FastAPI is a modern, fast, web framework for building APIs with Python.")
        answer = await bot.call(question=LMUserMessage("What is FastAPI?", chat_id=0))
        relevant_doc = answer.relevant_docs[0]

        self.assertIsNotNone(answer)
        self.assertEqual(doc.id, relevant_doc.id)
        await self.__delete_bot(self.bot_id)

    async def test_fetch_all_docs(self):
        await self.bot_station.create(self.meta_info)
        bot = await self.bot_station.get_bot(self.bot_id)
        await bot.docs_library.load()

        await bot.docs_library.create_document(
            data="FastAPI is a modern, fast, web framework for building APIs with Python.",
            source_link="http://link.co")
        await bot.docs_library.create_document(
            data="FastAPI is a web framework for hackathon developers.")

        docs_iterable = await bot.docs_library.get_all_docs()
        all_docs = list(docs_iterable)

        self.assertEqual(2, len(all_docs))
        await self.__delete_bot(self.bot_id)

    async def test_fetch_relevant_docs(self):
        await self.bot_station.create(self.meta_info)
        bot = await self.bot_station.get_bot(self.bot_id)
        await bot.docs_library.load()

        await bot.docs_library.create_document(
            data="FastAPI is a modern, fast, web framework for building APIs with Python language.",
            source_link="http://link.co")
        await bot.docs_library.create_document(
            data="FastAPI is a web framework for hackathon developers.")

        search_result: DocumentsSearchResult = await bot.docs_library.get_relevant_docs(
            "What programming language can used for FastAPI?"
        )
        self.assertEqual(2, len(search_result.docs))
        await self.__delete_bot(self.bot_id)

    async def __delete_bot(self, bot_id: str):
        await self.bot_station.delete(bot_id=bot_id)


if __name__ == '__main__':
    unittest.main()
