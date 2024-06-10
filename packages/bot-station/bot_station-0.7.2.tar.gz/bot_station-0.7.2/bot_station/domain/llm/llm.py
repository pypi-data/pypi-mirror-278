from abc import ABC, abstractmethod


class LLM(ABC):

    @abstractmethod
    async def call(self, query: str) -> str:
        pass
