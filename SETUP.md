# Quick Setup Guide

## Prerequisites

- Python 3.13+
- Supabase account (free tier works)
- Google AI Studio API key (free)

## 1. Install Dependencies

```bash
poetry install
```

## 2. Setup Supabase

1. Create a Supabase project at https://supabase.com
2. Go to **SQL Editor** and run:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

3. Get your **PostgreSQL connection string (URI)**:
   - Copy the connection string (looks like: `postgresql://postgres.xxxxx:...`)
   - **Important**: Replace `[YOUR-PASSWORD]` with your actual database password
   - Add `+psycopg` after `postgresql` (becomes `postgresql+psycopg://...`)

**Example:**
```
postgresql+psycopg://postgres.abcdefgh:mypassword123@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```

## 3. Get Google AI API Key

1. Go to https://aistudio.google.com/apikey
2. Create a new API key
3. Copy the key

## 4. Configure Environment

```bash
cp .env.example .env
```

Edit `.env`:
```
GOOGLE_API_KEY=your-google-api-key-here
DB_URL=postgresql+psycopg://postgres:your-password@db.xxx.supabase.co:5432/postgres
```

## 5. Download Sample PDFs (Optional)

```bash
poetry run python scripts/download_pdfs.py
```

This downloads sample public domain books:
- The Richest Man in Babylon (personal finance)
- The Wealth of Nations (economics)
- The Science of Getting Rich (wealth building)
- The Theory of Money and Credit (monetary theory)
- Common Sense (political economy)

**Or use your own PDFs:**
```bash
mkdir -p data/pdfs
cp /path/to/your/*.pdf data/pdfs/
```

## 6. Ingest PDFs

**Option A: Fast (Semantic Chunking)**
```bash
poetry run python scripts/ingest_pdfs_agno.py --directory data/pdfs
```

**Option B: Best Accuracy (Enhanced Contextual)**
```bash
poetry run python scripts/ingest_pdfs_enhanced.py --directory data/pdfs
```

## 7. Query with Agent

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

agent.print_response("Your question about the documents", stream=True)
```

## 8. Or Use Notebooks

```bash
poetry run jupyter lab
```

Open:
- `notebooks/01_agno_semantic.ipynb` - Fast semantic chunking
- `notebooks/02_enhanced_contextual.ipynb` - Enhanced with LLM context

## Troubleshooting

**"No module named 'agno'"**
```bash
poetry install
```

**"Connection refused"**
- Check DB_URL in `.env`
- Verify Supabase project is active
- Test connection: `psql "your-db-url"`

**"Rate limit exceeded"**
- Gemini free tier: 15 requests/minute
- Wait or upgrade to paid tier

## What's Next?

- See `IMPLEMENTATION_COMPARISON.md` for approach details
- Check `PDF_SOURCES.md` for sample PDF sources
- Read `README.md` for architecture overview
