import collections
import logging
from typing import Tuple, List, Optional

from qdrant_client import QdrantClient
from qdrant_client.conversions.common_types import PointId, Record

from bot_station.data.docs.mapper.document_mapper import SOURCE_LINK_KEY
from bot_station.domain.docs.model.document import Document


class QdrantDocsIterator(collections.abc.Iterator):
    qdrant_cli: QdrantClient
    collection_name: str
    last_point_id: PointId | None
    iteration_started: bool

    def __init__(self,
                 qdrant_cli: QdrantClient,
                 collection_name: str
                 ):
        self.qdrant_cli = qdrant_cli
        self.collection_name = collection_name
        self.last_point_id = None
        self.iteration_started = False

    def __next__(self):
        if self.iteration_started and self.last_point_id is None:
            raise StopIteration()
        self.iteration_started = True

        try:
            result: Tuple[List[Record], Optional[PointId]] = \
                self.qdrant_cli.scroll(collection_name=self.collection_name,
                                       limit=1,
                                       offset=self.last_point_id,
                                       with_vectors=False)
            record: Record = result[0][0]
            self.last_point_id = result[1]

            data = record.payload["document"]
            record.payload.pop("document")
            metadata = record.payload
            source_link = metadata[SOURCE_LINK_KEY]
            return Document(id=record.id, data=data, source_link=source_link, metadata=metadata)
        except Exception as e:
            logging.error(f"Iteration error: {e}")
            raise StopIteration()


class QdrantDocsIterable(collections.abc.Iterable):
    qdrant_cli: QdrantClient
    collection_name: str

    def __init__(self,
                 qdrant_cli: QdrantClient,
                 collection_name: str
                 ):
        self.qdrant_cli = qdrant_cli
        self.collection_name = collection_name

    def __iter__(self):
        return QdrantDocsIterator(qdrant_cli=self.qdrant_cli, collection_name=self.collection_name)
