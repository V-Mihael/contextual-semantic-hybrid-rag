# 🚀 Deploy Guide - Railway

## Prerequisites

1. **Railway Account**: [railway.app](https://railway.app)
2. **Google API Key**: [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
3. **Supabase Database**: Create project and enable pgvector

## Supabase Setup

```sql
-- Run in Supabase SQL Editor
CREATE EXTENSION IF NOT EXISTS vector;
```

## Railway Deployment

### 1. Connect Repository
- New Project → Deploy from GitHub repo
- Select: `contextual-rag-agno-supabase`

### 2. Configure Environment Variables
In Railway dashboard, **Variables** tab:

```bash
GOOGLE_API_KEY=your_google_api_key_here
DB_URL=postgresql+psycopg://postgres:[PASSWORD]@[HOST]:5432/postgres
```

**Get DB_URL from Supabase:**
- Dashboard → Settings → Database → Connection String (URI)
- Replace `postgresql://` with `postgresql+psycopg://`

### 3. Automatic Deploy
- Railway detects `Dockerfile` and builds automatically
- Each GitHub push triggers new deployment

## Local Testing

```bash
# Build
docker build -t rag .

# Run
docker run -p 8000:8000 \
  -e GOOGLE_API_KEY=your_key \
  -e DB_URL=your_db_url \
  rag

# Test
curl http://localhost:8000/health
```

## API Endpoints

### Health Check
```bash
curl https://your-app.railway.app/health
```

### Query
```bash
curl -X POST https://your-app.railway.app/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is semantic chunking?",
    "max_results": 5
  }'
```

## Ingest PDFs (Before Deploy)

```bash
# Install dependencies
poetry install

# Ingest PDFs locally
poetry run python scripts/ingest_pdfs_enhanced.py --directory data/pdfs

# Commit and push
git add .
git commit -m "Add ingested data"
git push
```

## Troubleshooting

**Error: "Knowledge base loading..."**
- Wait for complete initialization (~30s)
- Check Railway logs

**Error: Connection refused**
- Verify DB_URL is correct
- Confirm pgvector is enabled in Supabase

**Build fails:**
- Verify `poetry.lock` is committed
- Run `poetry lock` locally if needed
