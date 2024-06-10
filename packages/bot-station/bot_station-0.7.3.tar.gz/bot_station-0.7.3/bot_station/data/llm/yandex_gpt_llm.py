from langchain_community.chat_models import ChatYandexGPT
from langchain_core.language_models import BaseChatModel
from langchain_core.tracers import langchain

from bot_station.data.bot.model.yandex_cloud_config import YandexCloudConfig
from bot_station.domain.llm.llm import LLM


class YandexGPTLLM(LLM):
    gpt: BaseChatModel

    def __init__(
            self,
            yandex_cloud_config: YandexCloudConfig,
            temperature: float = 0.6,
    ):
        langchain.debug = False
        self.gpt = ChatYandexGPT(
            api_key=yandex_cloud_config.api_key,
            folder_id=yandex_cloud_config.folder_id,
            temperature=temperature,
            model_name=yandex_cloud_config.model_name,
            model_version=yandex_cloud_config.model_version,
            verbose=True,
        )

    async def call(self, query: str) -> str:
        return self.gpt.invoke(query).content
