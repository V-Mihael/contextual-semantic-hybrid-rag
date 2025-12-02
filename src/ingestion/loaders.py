from pathlib import Path
from pypdf import PdfReader

class DocumentLoader:
    @staticmethod
    def load_pdf(file_path: str) -> str:
        reader = PdfReader(file_path)
        return "\n".join(page.extract_text() for page in reader.pages)
    
    @staticmethod
    def load_txt(file_path: str) -> str:
        return Path(file_path).read_text(encoding="utf-8")
    
    @staticmethod
    def load(file_path: str) -> str:
        ext = Path(file_path).suffix.lower()
        if ext == ".pdf":
            return DocumentLoader.load_pdf(file_path)
        elif ext == ".txt":
            return DocumentLoader.load_txt(file_path)
        raise ValueError(f"Unsupported file type: {ext}")
