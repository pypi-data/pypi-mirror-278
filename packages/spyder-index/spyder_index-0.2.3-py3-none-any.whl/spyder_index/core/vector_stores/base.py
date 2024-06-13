from pydantic import BaseModel

from spyder_index.core.document import Document

class VectorStoreQueryResult(BaseModel):
    document: Document
    confidence: float

    @classmethod
    def class_name(cls) -> str:
        return "VectorStoreQueryResult"