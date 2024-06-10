from dataclasses import dataclass
from typing import TypeAlias

from bot_station.domain.docs.model.document import Document

RelevanceScore: TypeAlias = float


@dataclass
class DocumentsSearchResult:
    docs: dict[RelevanceScore, Document]
