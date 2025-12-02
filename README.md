# Contextual RAG with Agno + Supabase

Advanced RAG system featuring Contextual Retrieval, Hybrid Search (Vector + FTS), and LLM-based Reranking.

## Features

- **Contextual Retrieval**: Adds situating context to chunks using LLM
- **Hybrid Search**: Combines vector similarity + full-text search with RRF
- **Reranking**: LLM-based reranking for improved relevance
- **Agno Framework**: Agent orchestration and LLM interactions
- **Supabase**: Postgres + pgvector + FTS backend

## Setup

1. Install dependencies:
```bash
poetry install
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env with your credentials
```

3. Setup Supabase schema:
```bash
psql -h your-db.supabase.co -U postgres -d postgres -f sql/schema.sql
```

## Usage

### API Server

```bash
uvicorn src.api.main:app --reload
```

### Ingest Documents

```bash
curl -X POST "http://localhost:8000/ingest" \
  -F "file=@document.pdf"
```

### Query

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the main topic?", "top_k": 5}'
```

## Architecture

```
Query → Hybrid Search (Vector + FTS) → Rerank → LLM → Answer
```

## License

MIT
