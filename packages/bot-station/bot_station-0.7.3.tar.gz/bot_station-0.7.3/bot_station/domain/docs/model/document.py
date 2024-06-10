from dataclasses import dataclass, field
from typing import TypeAlias

DocId: TypeAlias = str


@dataclass
class Document:
    id: DocId = field()
    data: str = field()
    source_link: str | None = field(default=None)
    metadata: dict | None = field(default_factory=dict)
