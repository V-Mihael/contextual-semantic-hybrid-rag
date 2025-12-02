from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.config import settings

class Chunker:
    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size or settings.chunk_size,
            chunk_overlap=chunk_overlap or settings.chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def chunk(self, text: str) -> list[str]:
        return self.splitter.split_text(text)
