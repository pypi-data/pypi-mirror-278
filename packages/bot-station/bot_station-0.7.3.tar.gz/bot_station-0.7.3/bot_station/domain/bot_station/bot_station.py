import logging
from abc import abstractmethod, ABC
from typing import List

from bot_station.domain.bot.bot import Bot
from bot_station.domain.bot.bot_factory import BotFactory
from bot_station.domain.bot.model.bot_meta_info import BotMetaInfo
from bot_station.domain.bot_station.bot_registry import BotRegistry


class BotStation(ABC):

    @abstractmethod
    async def create(self, config: BotMetaInfo):
        pass

    @abstractmethod
    async def get_bot(self, bot_id: str) -> Bot | None:
        pass

    @abstractmethod
    async def get_bots_list(self) -> List[BotMetaInfo]:
        pass

    @abstractmethod
    async def delete(self, bot_id: str) -> bool:
        pass

    @abstractmethod
    async def update(self, info: BotMetaInfo):
        pass


class BotStationImpl(BotStation):
    bot_registry: BotRegistry
    bot_factory: BotFactory

    __in_memory_bots: dict[str, Bot] = {}

    def __init__(
            self,
            bot_registry: BotRegistry,
            bot_factory: BotFactory,
    ):
        self.bot_registry = bot_registry
        self.bot_factory = bot_factory

    async def create(self, bot_info: BotMetaInfo):
        logging.debug(f"create {bot_info}")
        bot_with_same_id = await self.bot_registry.get(bot_id=bot_info.id)
        if bot_with_same_id is None:
            meta_info = await self.bot_registry.create(bot_info)
            return meta_info
        else:
            raise Exception(f"Bot with id '{bot_info.id}' already exists!")

    async def get_bot(self, bot_id: str) -> Bot | None:
        logging.debug(f"Get {bot_id})")
        if bot_id is None:
            raise Exception("Bot id is None!")
        bot = self.__in_memory_bots.get(bot_id, None)
        if bot is not None:
            return bot

        meta = await self.bot_registry.get(bot_id)
        if meta is None:
            logging.warning(f"No {bot_id} in registry!")
            return None
        else:
            bot = await self.bot_factory.create(meta=meta)
            await bot.docs_library.load()
            self.__in_memory_bots[bot_id] = bot
            return bot

    async def get_bots_list(self) -> List[BotMetaInfo]:
        logging.debug("get_bots_list")
        return await self.bot_registry.get_all()

    async def delete(self, bot_id: str) -> bool:
        logging.debug(f"delete {bot_id}")
        bot = await self.get_bot(bot_id=bot_id)
        if bot is not None:
            await bot.docs_library.load()
            await bot.docs_library.clear()
            await self.bot_registry.delete(bot_id=bot_id)
            self.__in_memory_bots.pop(bot_id, None)
            return True
        else:
            logging.warning(f"No {bot_id} in registry")
            return False

    async def update(self, info: BotMetaInfo):
        logging.debug(f"Update {info}")
        await self.bot_registry.update(info)
        # reload bot
        bot = self.__in_memory_bots.pop(info.id, None)
        if bot is not None:
            logging.debug(f"Close {bot.meta}")
            await bot.docs_library.close()
