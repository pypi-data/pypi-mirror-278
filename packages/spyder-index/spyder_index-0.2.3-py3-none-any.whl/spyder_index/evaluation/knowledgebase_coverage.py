from typing import Optional, Literal, List

from spyder_index.core.embeddings import Embeddings

class KnowledgeBaseCoverage():

    def __init__(self,
                 embed_model: Optional[Embeddings] = None,
                 similarity_mode: Literal["cosine", "dot_product", "euclidean"] = "cosine",
                 similarity_threshold: float = 0.8,) -> None:
        
        self._embed_model = embed_model
        # self._similarity_fn = 
        self._similarity_threshold = similarity_threshold

        def compute(self, retrieval_context: List[str], model_output: str):
                            
            if model_output is None or retrieval_context is None:
                raise ValueError("Must specify both retrieval_context and model_output")
            
            
        
