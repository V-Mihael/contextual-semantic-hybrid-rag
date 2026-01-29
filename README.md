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
poetry run python scripts/shared/download_pdfs.py

# 5. Ingest your PDFs (choose one)
poetry run python scripts/agno/ingest_semantic.py --directory data/pdfs          # Fast
poetry run python scripts/agno/ingest_contextual.py --directory data/pdfs       # Best
poetry run python scripts/langchain/ingest.py --directory data/pdfs             # LangChain

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

### Two Framework Options

**🔵 Agno (Recommended for Quick Start)**
- Native PDF reading and agent framework
- Built-in hybrid search
- ~10 lines of code
- Best for prototyping

**🟢 LangChain (Maximum Flexibility)**
- Standard LangChain ecosystem
- Compatible with LangChain chains
- Extensive community integrations
- Best for complex workflows

**See [AGNO_VS_LANGCHAIN.md](AGNO_VS_LANGCHAIN.md) for detailed comparison**

### Two Chunking Approaches

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

- **Agno & LangChain**: Choose your preferred framework
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
poetry run python scripts/shared/download_pdfs.py
```

### Ingest PDFs

**Agno (Fast):**
```bash
poetry run python scripts/agno/ingest_semantic.py --directory data/pdfs
```

**Agno (Best Accuracy):**
```bash
poetry run python scripts/agno/ingest_contextual.py --directory data/pdfs
```

**LangChain:**
```bash
poetry run python scripts/langchain/ingest.py --directory data/pdfs
```

### Query with Agent

```python
from agno.agent import Agent
from agno.models.google import Gemini
from src.rag.agno import AgnoKnowledgeBase

kb = AgnoKnowledgeBase()

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

- `notebooks/agno/01_semantic_chunking.ipynb` - Fast semantic chunking (Agno)
- `notebooks/agno/02_contextual_chunking.ipynb` - Enhanced contextual (Agno)
- `notebooks/langchain/01_contextual_chunking.ipynb` - LangChain implementation

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
├── rag/
│   ├── agno/
│   │   ├── knowledge_base.py                # Fast semantic (Agno)
│   │   ├── contextual_knowledge_base.py     # Enhanced contextual (Agno)
│   │   └── chunking.py                      # Agno-specific chunking
│   └── langchain/
│       ├── contextual_knowledge_base.py     # Contextual semantic (LangChain)
│       └── chunking.py                      # LangChain-specific chunking
├── api/
│   └── main.py                              # FastAPI application
├── integrations/
│   └── whatsapp.py                          # WhatsApp integration
└── config.py                                # Settings

scripts/
├── agno/
│   ├── ingest_semantic.py                   # Fast ingestion (Agno)
│   └── ingest_contextual.py                 # Enhanced ingestion (Agno)
├── langchain/
│   └── ingest.py                            # LangChain ingestion
└── shared/
    └── download_pdfs.py                     # Sample PDF downloader

notebooks/
├── agno/
│   ├── 01_semantic_chunking.ipynb           # Quick demo (Agno)
│   └── 02_contextual_chunking.ipynb         # Advanced demo (Agno)
└── langchain/
    └── 01_contextual_chunking.ipynb         # LangChain demo
```

## Documentation

- **[SETUP.md](SETUP.md)** - Complete setup guide
- **[STRUCTURE.md](STRUCTURE.md)** - Project structure and architecture
- **[AGNO_VS_LANGCHAIN.md](AGNO_VS_LANGCHAIN.md)** - Framework comparison
- **[DEPLOY.md](DEPLOY.md)** - Deployment guide

## Requirements

- Python 3.13+
- Supabase account (free tier)
- Google AI Studio API key (free)
- PDF documents to ingest

## License

MIT
