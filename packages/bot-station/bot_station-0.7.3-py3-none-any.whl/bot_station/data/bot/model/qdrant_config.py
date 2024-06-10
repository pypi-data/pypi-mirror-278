from dataclasses import dataclass


@dataclass
class QdrantConfig:
    qdrant_url: str | None
    qdrant_db_path: str | None