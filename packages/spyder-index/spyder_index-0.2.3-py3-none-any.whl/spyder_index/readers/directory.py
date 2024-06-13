import os

from pathlib import Path
from typing import List, Optional, Type, Callable

from spyder_index.core.readers import BaseReader
from spyder_index.core.document import Document

from langchain_community.document_loaders import DirectoryLoader

def _loading_default_file_readers():
    from spyder_index.readers.file import DocxReader
    from spyder_index.readers.file import HTMLReader
    from spyder_index.readers.file import PDFReader

    default_file_reader_cls: dict[str, Type[BaseReader]] = {
        ".docx": DocxReader,
        ".html": HTMLReader,
        ".pdf": PDFReader,
    }
    
    return default_file_reader_cls


class DirectoryReader(BaseReader):
    default_file_reader_fn: Callable = _loading_default_file_readers

    def __init__(self, input_dir: str = None, 
                 file_reader: Optional[dict[str, Type[BaseReader]]] = None, 
                 recursive: Optional[bool] = False):
        
        if not input_dir:
            raise ValueError("You must provide a `input_dir` parameter")

        if not os.path.isdir(input_dir):
            raise ValueError(f"Directory `{input_dir}` does not exist")
        
        if file_reader is not None:
            self.file_reader = file_reader
        else:
            self.file_reader = {}
        
        self.input_dir = Path(input_dir)
        self.recursive = recursive


    def load_data(self, extra_info: Optional[dict] = None) -> List[Document]:
        documents = []
        default_file_reader_cls = DirectoryReader.default_file_reader_fn()

        file_reader = self.file_reader | default_file_reader_cls
        file_reader_suffix = list(file_reader.keys())

        for file_suffix in file_reader_suffix:
            print(file_suffix)
            #TO-DO add `file_reader_kwargs`
            docs = DirectoryLoader(self.input_dir, glob=f"**/*{file_suffix}", loader_cls=file_reader[file_suffix]).load()
            
            documents.extend(docs)
            #TO-DO extend `doc.metadata` with `extra_info`
        return documents
