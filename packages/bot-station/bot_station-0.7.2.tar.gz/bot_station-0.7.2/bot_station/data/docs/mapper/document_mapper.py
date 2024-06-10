from qdrant_client.fastembed_common import QueryResponse

from bot_station.domain.docs.model.document import Document

SOURCE_LINK_KEY = "source_link"
CUSTOM_ID = "custom_id"
ID_KEY = "id"


class DocumentMapper:
    @staticmethod
    def from_qdrant_response(doc: QueryResponse) -> Document:
        return Document(
            data=doc.document,
            metadata=doc.metadata,
            source_link=doc.metadata.get(SOURCE_LINK_KEY, None),
            id=doc.id,
        )
