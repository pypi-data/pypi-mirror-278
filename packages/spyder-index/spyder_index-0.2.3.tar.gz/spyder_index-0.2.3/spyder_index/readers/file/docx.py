import os

from pathlib import Path
from typing import List, Optional

from spyder_index.core.readers import BaseReader
from spyder_index.core.document import Document

from langchain_community.document_loaders import Docx2txtLoader

class DocxReader(BaseReader):

    def __init__(self, input_file: str = None):

        try:
            import docx2txt
        except ImportError:
            raise ImportError("docx2txt package not found, please install it with `pip install docx2txt`")
        
        if not input_file:
            raise ValueError("You must provide a `input_dir` parameter")
        
        if not os.path.isfile(input_file):
                    raise ValueError(f"File `{input_file}` does not exist")
        
        self.input_file = Path(input_file)

    def load_data(self, extra_info: Optional[dict] = None) -> List[Document]: 

        lc_documents = Docx2txtLoader(file_path=self.input_file).load()

        return [Document()._from_langchain_format(doc=doc) for doc in lc_documents]