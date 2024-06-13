from langchain_community.document_loaders import UnstructuredFileLoader

import os

from pathlib import Path
from typing import List, Optional

from spyder_index.core.readers import BaseReader
from spyder_index.core.document import Document

class UnstructuredTxtReader(BaseReader):

    def __init__(self, input_file: str = None):

        if not input_file:
            raise ValueError("You must provide a `input_dir` parameter")
        
        if not os.path.isfile(input_file):
                    raise ValueError(f"File `{input_file}` does not exist")
        
        self.input_file = Path(input_file)

    # def load_data(self, extra_info: Optional[dict] = None) -> List[Document]: 

        # work in progress
        # return
