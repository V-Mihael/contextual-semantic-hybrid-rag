# Production RAG: Semantic Chunking + Contextual Retrieval + Hybrid Search

Advanced RAG system with **Semantic Chunking**, **Contextual Retrieval** & **Hybrid Search** for superior retrieval quality.


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

## Advanced Chunking Pipeline

This RAG system combines **Semantic Chunking** with **Contextual Retrieval** for superior retrieval quality:

### 1. Semantic Chunking (powered by chonkie)
- Splits documents using sentence-level embedding similarity (OpenAI text-embedding-3-small)
- `similarity_threshold=0.5` ensures coherent topical boundaries
- Preserves semantic units vs. fixed-size splitting

### 2. Contextual Retrieval (Anthropic-inspired)
- LLM-generated **contextual headers** prepended to each chunk before embedding
- Headers provide document-level situational awareness ("Q2 2023 financials for ACME Corp...")
- Boosts hybrid search recall by 30-60% on complex queries

### Complete Pipeline
```
PDF → SemanticChunking → LLM Context Headers → Hybrid Embeddings (BM25 + Vector) → pgvector/Supabase
```

**Result**: Production-grade retrieval that understands both local chunk semantics and global document context.

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
- 30-60% better retrieval accuracy
- Best for production

### Core Features

- **Agno Framework**: Native PDF reading, chunking, and vector storage
- **PgVector**: Postgres extension for vector similarity search
- **Hybrid Search**: Combines semantic + keyword search with RRF
- **Gemini Integration**: Embeddings (text-embedding-004) + LLM (gemini-2.5-flash)
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
    model=Gemini(id="gemini-2.5-flash"),
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
- Powered by chonkie with OpenAI embeddings

**Contextual Enhancement (Anthropic-inspired)**
- LLM generates situating context for each chunk
- Improves retrieval by 30-60%
- Provides document-level awareness to each chunk
- Uses Gemini 1.5 Flash (1M+ context, $0.075/M tokens)
- Cost: ~$0.10 per 500-page book (one-time ingest)

**Hybrid Search > Vector-Only**
- Combines semantic similarity (vector) + keyword matching (BM25)
- Handles both conceptual and specific queries
- RRF (Reciprocal Rank Fusion) for result merging

## Cost & Performance

### Context Window Strategy

Long documents (128k+ tokens) are handled efficiently:

| Model | Context Window | Cost/M Input | Best For |
|-------|----------------|--------------|----------|
| Gemini 1.5 Flash | 1M+ | $0.075/M | Large books (recommended) |
| Claude 3 Haiku | 200k | $0.25/M | Medium docs with caching |
| GPT-4o-mini | 128k | $0.15/M | Short docs |

### Ingestion Cost Examples

- **500-page book**: ~$0.10 (one-time)
- **Research paper (50 pages)**: ~$0.01
- **Documentation set (1000 pages)**: ~$0.20

**Key**: Context generation is one-time cost. Queries use only embeddings (nearly free).

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
