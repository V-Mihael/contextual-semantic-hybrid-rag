"""Ingest PDFs using Agno with semantic chunking."""

import argparse
from pathlib import Path

from src.rag.agno import AgnoKnowledgeBase


def main():
    """Ingest PDFs with Agno and semantic chunking."""
    parser = argparse.ArgumentParser(
        description="Ingest PDFs using Agno with semantic chunking"
    )
    parser.add_argument(
        "--directory",
        type=str,
        default="data/pdfs",
        help="Directory containing PDF files",
    )
    parser.add_argument(
        "--table",
        type=str,
        default="economics_docs_agno",
        help="Table name for the vectorstore",
    )
    args = parser.parse_args()

    kb = AgnoKnowledgeBase(table_name=args.table)

    pdf_dir = Path(args.directory)
    if not pdf_dir.exists():
        print(f"❌ Directory not found: {args.directory}")
        return

    print(f"🚀 Starting Agno semantic ingestion from: {args.directory}")
    kb.ingest_directory(args.directory)
    print("✅ Ingestion complete!")


if __name__ == "__main__":
    main()
