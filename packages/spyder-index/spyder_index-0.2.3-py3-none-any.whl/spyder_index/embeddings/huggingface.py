from typing import List, Literal

from spyder_index.core.document import Document
from spyder_index.core.embeddings import Embeddings

from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings as LangchainHuggingFaceEmbeddings

class HuggingFaceEmbeddings(Embeddings):
    """Class for computing text embeddings using HuggingFace models."""

    def __init__(self, 
                 model_name: str= "sentence-transformers/all-MiniLM-L6-v2", 
                 device: Literal["cpu", "cuda"] = "cpu") -> None:
        
        model_kwargs = {
            "device": device
        }

        self._embed = LangchainHuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs)
    
    def get_query_embedding(self, query: str) -> List[float]:
        """Compute embedding for a text.

        Args:
            query (str): Input query to compute embedding.

        Returns:
            List[float]: Embedding vector for the input text.
        """ 
        embedding_text = self._embed.embed_query(query) 

        return embedding_text

    def get_embedding_from_texts(self, texts: List[str]) -> List[List[float]]:
        """Compute embeddings for list of texts.

        Args:
            texts (List[str]): List of input texts to compute embedding.

        Returns:
            List[List[float]]: List of embedding vectors for the input texts.
        """
        embedding_texts = self._embed.embed_documents(texts=texts)

        return embedding_texts
    
    def get_documents_embedding(self, documents: List[Document]) -> List[List[float]]:
        """Compute embeddings for a list of documents.

        Args:
            documents (List[Document]): List of Document.

        Returns:
            List[List[float]]: List of embedding vectors for the input documents.
        """
        embedding_documents = [self.get_query_embedding(document.get_text()) for document in documents]

        return embedding_documents
