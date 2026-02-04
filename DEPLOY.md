# 🚀 Deploy Guide

## Prerequisites

1. **Render Account**: [render.com](https://render.com) (or Railway)
2. **Google API Key**: [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
3. **Telegram Bot Token**: Get from @BotFather on Telegram
4. **Supabase Database**: Create project and enable pgvector

## Supabase Setup

```sql
-- Run in Supabase SQL Editor
CREATE EXTENSION IF NOT EXISTS vector;
```

## Render Deployment

### 1. Create Web Service
- New → Web Service
- Connect GitHub repository
- Select: `contextual-semantic-hybrid-rag`

### 2. Configure Service
- **Name**: rag-telegram-bot
- **Environment**: Docker
- **Region**: Choose closest to you
- **Instance Type**: Free (or Starter for production)

### 3. Environment Variables
In Render dashboard, **Environment** tab:

```bash
GOOGLE_API_KEY=your_google_api_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TAVILY_API_KEY=your_tavily_api_key
DB_URL=postgresql+psycopg://postgres:[PASSWORD]@[HOST]:5432/postgres
```

**Get DB_URL from Supabase:**
- Dashboard → Settings → Database → Connection String (URI)
- Replace `postgresql://` with `postgresql+psycopg://`

### 4. Deploy
- Click **Create Web Service**
- Render detects `Dockerfile` and builds automatically
- Each GitHub push triggers new deployment

### 5. Test
- API: `https://your-app.onrender.com/health`
- Telegram: Send message to your bot

## Alternative: Railway Deployment

Same steps as Render:
1. New Project → Deploy from GitHub
2. Add environment variables
3. Railway auto-detects Dockerfile
4. Deploy!

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
curl https://your-app.onrender.com/health
```

### Query
```bash
curl -X POST https://your-app.onrender.com/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is semantic chunking?",
    "session_id": "user123"
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

**Error: "Agent loading..."**
- Wait for complete initialization (~30s)
- Check Render logs

**Telegram bot not responding:**
- Verify TELEGRAM_BOT_TOKEN is correct
- Check logs: `poetry run python scripts/telegram_bot.py`

**Error: Connection refused**
- Verify DB_URL is correct
- Confirm pgvector is enabled in Supabase

**Build fails:**
- Verify `poetry.lock` is committed
- Run `poetry lock` locally if needed
