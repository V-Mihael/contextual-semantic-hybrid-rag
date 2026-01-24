# Sample PDF Sources

Free public domain books for testing the RAG system.

## Automated Download

```bash
poetry run python scripts/download_pdfs.py
```

## Investment & Economics Books

### The Richest Man in Babylon - George S. Clason (1926)
- **URL**: https://www.gutenberg.org/ebooks/58523
- **Topics**: Personal finance, wealth building, saving principles
- **Format**: PDF available
- **Public Domain**: Yes

### The Wealth of Nations - Adam Smith (1776)
- **URL**: https://www.gutenberg.org/ebooks/3300
- **Topics**: Economics, capitalism, free markets, division of labor
- **Format**: PDF available
- **Public Domain**: Yes

### The Science of Getting Rich - Wallace D. Wattles (1910)
- **URL**: https://www.gutenberg.org/ebooks/43948
- **Topics**: Wealth creation, positive thinking, success principles
- **Format**: PDF available
- **Public Domain**: Yes

### The Theory of Money and Credit - Ludwig von Mises (1912)
- **URL**: https://www.gutenberg.org/ebooks/61580
- **Topics**: Monetary theory, banking, credit systems, Austrian economics
- **Format**: PDF available
- **Public Domain**: Yes

### Common Sense - Thomas Paine (1776)
- **URL**: https://www.gutenberg.org/ebooks/147
- **Topics**: Political economy, independence, governance
- **Format**: PDF available
- **Public Domain**: Yes

### Capital - Karl Marx (1867)
- **URL**: https://www.gutenberg.org/ebooks/61218
- **Topics**: Political economy, capitalism critique, labor theory
- **Format**: PDF available
- **Public Domain**: Yes

## Business & Self-Help

### Think and Grow Rich - Napoleon Hill (1937)
- **Source**: https://archive.org/details/think-and-grow-rich
- **Topics**: Success principles, mindset, wealth accumulation
- **Note**: Check copyright status in your region

### The Art of Money Getting - P.T. Barnum (1880)
- **URL**: https://www.gutenberg.org/ebooks/8581
- **Topics**: Business advice, money management, success
- **Public Domain**: Yes

### How to Live on 24 Hours a Day - Arnold Bennett (1910)
- **URL**: https://www.gutenberg.org/ebooks/2274
- **Topics**: Time management, productivity, self-improvement
- **Public Domain**: Yes

### The Game of Life and How to Play It - Florence Scovel Shinn (1925)
- **URL**: https://www.gutenberg.org/ebooks/44214
- **Topics**: Prosperity, positive thinking, metaphysics
- **Public Domain**: Yes

## Additional Resources

### More Economics
- **Principles of Economics** - Carl Menger: https://www.gutenberg.org/ebooks/64329
- **The Economic Consequences of the Peace** - John Maynard Keynes: https://www.gutenberg.org/ebooks/15776
- **Essays on Political Economy** - Frédéric Bastiat: https://www.gutenberg.org/ebooks/44800

### More Business
- **The Autobiography of Benjamin Franklin**: https://www.gutenberg.org/ebooks/20203
- **Up from Slavery** - Booker T. Washington: https://www.gutenberg.org/ebooks/2376
- **The Man Who Knew Too Much** - G.K. Chesterton: https://www.gutenberg.org/ebooks/1720

## Download Instructions

### From Project Gutenberg

1. Visit the URL
2. Click "PDF" or "EPUB" format
3. Save to `data/pdfs/` directory

### From Archive.org

1. Visit the URL
2. Click "Download Options" on the right
3. Select "PDF" format
4. Save to `data/pdfs/` directory

### Convert EPUB to PDF

```bash
# Install calibre
sudo apt install calibre  # Linux
brew install calibre      # macOS

# Convert
ebook-convert book.epub book.pdf
```

## Using Your Own PDFs

Simply place any PDF files in the `data/pdfs/` directory:

```bash
mkdir -p data/pdfs
cp /path/to/your/*.pdf data/pdfs/
```

Then ingest:

```bash
# Fast semantic chunking
poetry run python scripts/ingest_pdfs_agno.py --directory data/pdfs

# Enhanced contextual (best accuracy)
poetry run python scripts/ingest_pdfs_enhanced.py --directory data/pdfs
```

## Copyright Notice

- **Public Domain**: Works published before 1928 are public domain in the US
- **Project Gutenberg**: Only hosts public domain works
- **Archive.org**: Check individual item's copyright status
- **Your PDFs**: Ensure you have rights to process them

Always verify copyright status in your jurisdiction before use.

## Notes on Warren Buffett & Modern Books

**Warren Buffett's Letters to Shareholders** and modern investment books like **"Rich Dad Poor Dad"** are still under copyright and cannot be freely distributed.

**Alternatives:**
- Purchase legitimate copies
- Use for personal/educational purposes only
- Check if your institution has access
- Look for author-authorized free versions

**For this demo**, we use public domain books that cover similar topics:
- Wealth building principles
- Economic theory
- Business philosophy
- Financial wisdom
