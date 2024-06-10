from abc import ABC, abstractmethod

from bot_station.domain.bot.bot import Bot
from bot_station.domain.bot.model.bot_meta_info import BotMetaInfo


class BotFactory(ABC):

    @abstractmethod
    async def create(self, meta: BotMetaInfo) -> Bot:
        pass
