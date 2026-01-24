#!/usr/bin/env python3
"""Download sample PDFs from public domain sources."""
import urllib.request
from pathlib import Path


SOURCES = {
    "wealth_of_nations.pdf": "https://ia801309.us.archive.org/21/items/inquiryintonatur01smit/inquiryintonatur01smit.pdf",
    "common_sense_paine.pdf": "https://ia800308.us.archive.org/33/items/commonsense00pain/commonsense00pain.pdf",
    "science_of_getting_rich.pdf": "https://ia802706.us.archive.org/14/items/scienceofgetting00watt/scienceofgetting00watt.pdf",
}


def download_file(url: str, output_path: Path):
    """Download file with progress."""
    print(f"  📥 Downloading: {output_path.name}")
    try:
        urllib.request.urlretrieve(url, output_path)
        print(f"  ✅ Saved: {output_path}")
    except Exception as e:
        print(f"  ❌ Failed: {e}")


def main():
    # Create directory
    pdf_dir = Path("data/pdfs")
    pdf_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📚 Downloading {len(SOURCES)} sample PDFs to {pdf_dir}/\n")
    
    for filename, url in SOURCES.items():
        output_path = pdf_dir / filename
        
        if output_path.exists():
            print(f"  ⏭️  Skipping (already exists): {filename}")
            continue
        
        download_file(url, output_path)
    
    print(f"\n✨ Download complete! Files in {pdf_dir}/")
    print(f"\n💡 Next step: python scripts/ingest_pdfs_agno.py --directory {pdf_dir}")


if __name__ == "__main__":
    main()
