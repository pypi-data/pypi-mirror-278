from abc import ABC, abstractmethod
from typing import List

from bot_station.domain.bot.model.bot_meta_info import BotMetaInfo


class BotRegistry(ABC):

    @abstractmethod
    async def create(self, config: BotMetaInfo):
        pass

    @abstractmethod
    async def update(self, meta: BotMetaInfo):
        pass

    @abstractmethod
    async def get(self, bot_id: str) -> BotMetaInfo | None:
        pass

    @abstractmethod
    async def get_all(self) -> List[BotMetaInfo]:
        pass

    @abstractmethod
    async def delete(self, bot_id: str):
        pass
