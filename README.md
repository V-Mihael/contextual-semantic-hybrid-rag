# Contextual RAG with Agno + Supabase

Advanced RAG system with **Semantic Chunking**, **Contextual Enhancement**, and **Hybrid Search** for PDF documents.

**Use Case**: Build intelligent Q&A systems over any PDF collection - books, research papers, documentation, etc.

## Quick Start

```bash
# 1. Install
poetry install

# 2. Configure environment
cp .env.example .env
# Edit .env with your GOOGLE_API_KEY and DB_URL

# 3. Enable pgvector in Supabase
# Run: CREATE EXTENSION IF NOT EXISTS vector;

# 4. Download sample PDFs (optional)
poetry run python scripts/download_pdfs.py

# 5. Ingest your PDFs (choose one)
poetry run python scripts/ingest_pdfs_agno.py --directory data/pdfs          # Fast
poetry run python scripts/ingest_pdfs_enhanced.py --directory data/pdfs     # Best

# 6. Query with notebooks
poetry run jupyter lab
```

**Full setup guide:** [SETUP.md](SETUP.md)

## Features

### Two Approaches Available

**1. Semantic Chunking (Fast)**
- Natural boundary detection using embeddings
- Hybrid search (vector + full-text)
- ~10 lines of code
- Best for prototyping

**2. Enhanced Contextual (Best Accuracy)**
- Semantic chunking + LLM context generation
- Each chunk gets situating context
- 20-30% better retrieval accuracy
- Best for production

### Core Features

- **Agno Framework**: Native PDF reading, chunking, and vector storage
- **PgVector**: Postgres extension for vector similarity search
- **Hybrid Search**: Combines semantic + keyword search with RRF
- **Gemini Integration**: Embeddings (text-embedding-004) + LLM (gemini-2.0-flash)
- **Supabase**: Managed Postgres with pgvector support

## Architecture

```
PDF → Agno PDFReader → Semantic Chunking → [Optional: LLM Context] → Embed → PgVector
                                                                              ↓
                                                    Query → Hybrid Search → Agent → Answer
```

## Usage

### Add Your PDFs

```bash
# Place PDFs in data/pdfs/ directory
mkdir -p data/pdfs
cp /path/to/your/*.pdf data/pdfs/
```

Or download sample PDFs:
```bash
poetry run python scripts/download_pdfs.py
```

See [PDF_SOURCES.md](PDF_SOURCES.md) for free public domain books.

### Ingest PDFs

**Fast (Semantic Chunking):**
```bash
poetry run python scripts/ingest_pdfs_agno.py --directory data/pdfs
```

**Best Accuracy (Enhanced Contextual):**
```bash
poetry run python scripts/ingest_pdfs_enhanced.py --directory data/pdfs
```

### Query with Agent

```python
from agno.agent import Agent
from agno.models.google import Gemini
from src.storage.agno_knowledge import AgnoKnowledge

kb = AgnoKnowledge()

agent = Agent(
    model=Gemini(id="gemini-2.0-flash-exp"),
    knowledge=kb.knowledge,
    search_knowledge=True
)

agent.print_response(
    "Your question here",
    stream=True
)
```

### Interactive Notebooks

```bash
poetry run jupyter lab
```

- `notebooks/01_agno_semantic.ipynb` - Fast semantic chunking demo
- `notebooks/02_enhanced_contextual.ipynb` - Enhanced contextual demo

## Why This Approach?

**Semantic Chunking > Fixed-Size Chunking**
- Preserves natural boundaries (paragraphs, concepts)
- Related content stays together
- Better retrieval accuracy
- No arbitrary splits mid-sentence

**Contextual Enhancement (Optional)**
- LLM generates situating context for each chunk
- Improves retrieval by 20-30%
- Inspired by Anthropic's contextual retrieval
- Trade-off: slower ingestion, higher cost

**Hybrid Search > Vector-Only**
- Combines semantic similarity + keyword matching
- Handles both conceptual and specific queries
- RRF (Reciprocal Rank Fusion) for result merging

## Project Structure

```
src/
├── ingestion/
│   └── contextual_semantic_chunking.py  # Custom chunking strategy
├── storage/
│   ├── agno_knowledge.py                # Fast semantic approach
│   └── enhanced_agno_knowledge.py       # Enhanced contextual approach
└── config.py                            # Settings

scripts/
├── download_pdfs.py                     # Sample PDF downloader
├── ingest_pdfs_agno.py                  # Fast ingestion
└── ingest_pdfs_enhanced.py              # Enhanced ingestion

notebooks/
├── 01_agno_semantic.ipynb               # Quick demo
└── 02_enhanced_contextual.ipynb         # Advanced demo
```

## Documentation

- **[SETUP.md](SETUP.md)** - Complete setup guide
- **[IMPLEMENTATION_COMPARISON.md](IMPLEMENTATION_COMPARISON.md)** - Approach comparison
- **[PDF_SOURCES.md](PDF_SOURCES.md)** - Sample PDF sources

## Requirements

- Python 3.13+
- Supabase account (free tier)
- Google AI Studio API key (free)
- PDF documents to ingest

## License

MIT
