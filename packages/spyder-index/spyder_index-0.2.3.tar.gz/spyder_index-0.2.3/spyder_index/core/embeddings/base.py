import numpy as np

from typing import List, Literal
from abc import ABC, abstractmethod

class Embeddings(ABC):
    """Interface for embedding models."""

    @classmethod
    def class_name(cls) -> str:
        return "Embeddings"
    
    @abstractmethod
    def get_query_embedding(self, query: str) -> List[float]:
        """Embed the input query."""

    @abstractmethod
    def get_embedding_from_texts(self, texts: List[str]) -> List[List[float]]:
        """Embed list of texts."""

    @abstractmethod
    def get_documents_embedding(self, documents: List[str]) -> List[List[float]]:
        """Embed list of docs."""

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.get_embedding_from_texts(texts=texts)
    
    
def embedding_similarity(embedding1: List[float], embedding2: List[float], 
                             mode: Literal["cosine", "dot_product", "euclidean"] = "cosine") -> float:
    if mode == "euclidean":
        return -float(np.linalg.norm(np.array(embedding1) - np.array(embedding2)))
        
    elif mode == "dot_product":
        return np.dot(embedding1, embedding2)
        
    else:
        product = np.dot(embedding1, embedding2)
        norm = np.linalg.norm(embedding1) * np.linalg.norm(embedding2)
        return product / norm