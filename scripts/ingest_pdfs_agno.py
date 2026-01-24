"""Ingest PDFs using Agno's native Knowledge and PDFReader."""
import argparse
from pathlib import Path
from src.storage.agno_knowledge import AgnoKnowledge


def main():
    parser = argparse.ArgumentParser(description="Ingest PDFs using Agno")
    parser.add_argument("--file", type=str, help="Path to single PDF file")
    parser.add_argument("--directory", type=str, help="Path to directory with PDFs")
    
    args = parser.parse_args()
    
    print("🚀 Initializing Agno Knowledge Base...")
    kb = AgnoKnowledge()
    
    if args.file:
        print(f"\n📄 Ingesting: {args.file}")
        kb.ingest_pdf(args.file)
        print("✅ Done!")
        
    elif args.directory:
        print(f"\n📚 Ingesting directory: {args.directory}")
        kb.ingest_directory(args.directory)
        print("✅ Done!")
        
    else:
        print("❌ Please provide --file or --directory")
        parser.print_help()


if __name__ == "__main__":
    main()
