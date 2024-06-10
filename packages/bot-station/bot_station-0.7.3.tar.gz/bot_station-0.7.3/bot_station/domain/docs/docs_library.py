from abc import abstractmethod
from typing import Iterable

from bot_station.domain.docs.docs_source import DocsSource
from bot_station.domain.docs.model.document import Document, DocId


class DocsLibrary(DocsSource):

    @abstractmethod
    async def load(self):
        pass

    @abstractmethod
    async def create_document(
            self,
            data: str,
            source_link: str | None = None,
            metadata: dict = {},
    ) -> Document:
        pass

    @abstractmethod
    async def delete_document(self, doc_id: DocId):
        pass

    @abstractmethod
    async def get_all_docs(self) -> Iterable[Document]:
        pass

    @abstractmethod
    async def close(self):
        pass

    @abstractmethod
    async def clear(self):
        pass
