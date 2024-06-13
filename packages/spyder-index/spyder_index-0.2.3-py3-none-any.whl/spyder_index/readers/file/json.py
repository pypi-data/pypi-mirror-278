import os

from pathlib import Path
from typing import List, Optional

from spyder_index.core.readers import BaseReader
from spyder_index.core.document import Document

from langchain_community.document_loaders import JSONLoader

class JSONReader(BaseReader):

    def __init__(self, input_file: str = None, 
                 jq_schema: Optional[str] = None, 
                 text_content: Optional[bool] = False):
        try:
            import jq 
        except ImportError:
            raise ImportError("jq package not found, please install it with `pip install jq`")

        if not input_file:
            raise ValueError("You must provide a `input_dir` parameter")
        
        if not os.path.isfile(input_file):
                    raise ValueError(f"File `{input_file}` does not exist")
        
        self.input_file = Path(input_file)
        self.jq_schema = jq_schema
        self.text_content = text_content

    def load_data(self, extra_info: Optional[dict] = None) -> List[Document]: 

        lc_documents = JSONLoader(file_path=self.input_file,
                            jq_schema=self.jq_schema,
                            text_content=self.text_content).load()

        return [Document()._from_langchain_format(doc=doc) for doc in lc_documents]