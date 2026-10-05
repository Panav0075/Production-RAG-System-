from dataclasses import dataclass, asdict
from typing import Dict


@dataclass
class Document:
    document_id: str
    title: str
    source: str
    url: str
    text: str


@dataclass
class Chunk:
    chunk_id: str
    document_id: str
    title: str
    source: str
    url: str
    text: str
    chunk_index: int

    def to_dict(self) -> Dict:
        return asdict(self)
