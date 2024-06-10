from bot_station.data.bot.bot_factory_impl import BotFactoryImpl
from bot_station.data.bot.model.qdrant_config import QdrantConfig
from bot_station.data.bot.model.yandex_cloud_config import YandexCloudConfig
from bot_station.data.bot_station.bot_registry_impl import BotRegistryImpl
from bot_station.domain.bot.bot_factory import BotFactory
from bot_station.domain.bot_station.bot_registry import BotRegistry
from bot_station.domain.bot_station.bot_station import BotStation, BotStationImpl


class BotStationModule(object):
    overrides_bot_factory: BotFactory | None = None

    @staticmethod
    def provide_bot_factory(bot_factory: BotFactory):
        BotStationModule.overrides_bot_factory = bot_factory

    @staticmethod
    def create_bot_station(
            yandex_cloud_config: YandexCloudConfig,
            qdrant_config: QdrantConfig,
    ) -> BotStation:
        bot_registry: BotRegistry = BotRegistryImpl()
        bot_station: BotStation = BotStationImpl(
            bot_registry=bot_registry,
            bot_factory=BotStationModule.__get_bot_factory(yandex_cloud_config, qdrant_config),
        )
        return bot_station

    @staticmethod
    def __get_bot_factory(
            env_config: YandexCloudConfig,
            qdrant_config: QdrantConfig,
    ) -> BotFactory:
        if BotStationModule.overrides_bot_factory is not None:
            return BotStationModule.overrides_bot_factory
        else:
            factory = BotFactoryImpl()
            factory.yandex_cloud_config = env_config
            factory.qdrant_config = qdrant_config
            return factory
