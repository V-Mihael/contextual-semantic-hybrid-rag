"""Ingest PDFs with context-enhanced semantic chunking."""

import argparse

from src.storage.contextual_agno_knowledge import ContextualAgnoKnowledge


def main() -> None:
    """Ingest PDFs with contextual semantic chunking for improved retrieval.

    This script uses enhanced chunking that combines:
    - Semantic chunking for natural boundaries
    - LLM-based context generation for each chunk
    - Hybrid search (vector + full-text)
    """
    parser = argparse.ArgumentParser(
        description="Ingest PDFs with contextual semantic chunking"
    )
    parser.add_argument("--file", type=str, help="Path to single PDF file")
    parser.add_argument("--directory", type=str, help="Path to directory with PDFs")

    args = parser.parse_args()

    print("🚀 Initializing Enhanced Knowledge Base...")
    print("   ✓ Semantic chunking (natural boundaries)")
    print("   ✓ LLM contextual enhancement")
    print("   ✓ Hybrid search (vector + FTS)\n")

    kb = ContextualAgnoKnowledge()

    if args.file:
        kb.ingest_pdf(args.file)
        print("\n✅ Done!")

    elif args.directory:
        kb.ingest_directory(args.directory)
        print("\n✅ Done!")

    else:
        print("❌ Please provide --file or --directory")
        parser.print_help()


if __name__ == "__main__":
    main()
