"""Ingest PDFs using LangChain with contextual semantic chunking."""

import argparse
from pathlib import Path

from src.rag.langchain import ContextualLangChainKnowledgeBase


def main():
    """Ingest PDFs with LangChain and contextual semantic chunking."""
    parser = argparse.ArgumentParser(
        description="Ingest PDFs using LangChain with contextual semantic chunking"
    )
    parser.add_argument(
        "--directory",
        type=str,
        default="data/pdfs",
        help="Directory containing PDF files",
    )
    parser.add_argument(
        "--collection",
        type=str,
        default="economics_enhanced_langchain",
        help="Collection name for the vectorstore",
    )
    args = parser.parse_args()

    kb = ContextualLangChainKnowledgeBase(collection_name=args.collection)

    pdf_dir = Path(args.directory)
    if not pdf_dir.exists():
        print(f"❌ Directory not found: {args.directory}")
        return

    print(f"🚀 Starting LangChain ingestion from: {args.directory}")
    kb.ingest_directory(args.directory)
    print("✅ Ingestion complete!")


if __name__ == "__main__":
    main()
