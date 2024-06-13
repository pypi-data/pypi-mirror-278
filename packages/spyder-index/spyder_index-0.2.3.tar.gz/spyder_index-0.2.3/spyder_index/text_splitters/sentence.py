from typing import List

from spyder_index.core.document import Document

from langchain_text_splitters.character import RecursiveCharacterTextSplitter

class SentenceSplitter():

    def __init__(self, 
                 chunk_size: int = 512 , 
                 chunk_overlap: int = 256,
                 separators = ["\n\n", "\n", " ", ""]
                 ) -> None:

        
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators


    def from_text(self, text: str) -> List[str]: 
        """
        Split text into chunks.
        
        Args:
        - text (str): Input text to split.
        
        Returns:
        - List[str]: List of chunks.
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=self.separators,
        )
        
        return text_splitter.split_text(text)

    
    def from_documents(self, documents: List[Document]) -> List[Document]: 
        chunks = []
        
        for document in documents:
            texts = self.from_text(document.get_text())

            for text in texts:
                chunks.append(Document(text=text, metadata=document.get_metadata()))

        return chunks