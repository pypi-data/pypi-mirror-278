from enum import Enum


class KnowledgeSourceContentType(str, Enum):
    CSV = "csv"
    PDF = "pdf"
    TEXT = "text"

    def __str__(self) -> str:
        return str(self.value)
