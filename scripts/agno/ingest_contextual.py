"""Ingest PDFs using Agno with contextual semantic chunking."""

import argparse
from pathlib import Path

from src.rag.agno import ContextualAgnoKnowledgeBase


def main():
    """Ingest PDFs with Agno and contextual semantic chunking."""
    parser = argparse.ArgumentParser(
        description="Ingest PDFs using Agno with contextual semantic chunking"
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
        default="economics_enhanced_agno",
        help="Table name for the vectorstore",
    )
    args = parser.parse_args()

    kb = ContextualAgnoKnowledgeBase(table_name=args.table)

    pdf_dir = Path(args.directory)
    if not pdf_dir.exists():
        print(f"❌ Directory not found: {args.directory}")
        return

    print(f"🚀 Starting Agno contextual ingestion from: {args.directory}")
    kb.ingest_directory(args.directory)
    print("✅ Ingestion complete!")


if __name__ == "__main__":
    main()
