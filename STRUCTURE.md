# Project Structure

## 📁 Directory Structure

```
contextual-semantic-hybrid-rag/
├── src/
│   ├── rag/                          # RAG implementations
│   │   ├── agno/                     # Agno framework implementation
│   │   │   ├── knowledge_base.py    # Semantic chunking
│   │   │   ├── contextual_knowledge_base.py  # Contextual enhancement
│   │   │   └── chunking.py          # Agno-specific contextual chunking
│   │   └── langchain/                # LangChain framework implementation
│   │       ├── contextual_knowledge_base.py  # Contextual semantic chunking
│   │       └── chunking.py          # LangChain-specific contextual chunking
│   ├── api/                          # FastAPI application
│   │   └── main.py                  # API endpoints
│   ├── integrations/                 # External integrations
│   │   └── whatsapp.py              # WhatsApp integration
│   └── config.py                     # Configuration settings
│
├── scripts/                          # Ingestion scripts
│   ├── agno/                         # Agno-specific scripts
│   │   ├── ingest_semantic.py       # Fast semantic chunking
│   │   └── ingest_contextual.py     # Enhanced contextual chunking
│   ├── langchain/                    # LangChain-specific scripts
│   │   └── ingest.py                # Contextual semantic chunking
│   └── shared/                       # Shared utilities
│       └── download_pdfs.py         # PDF downloader
│
├── notebooks/                        # Jupyter notebooks
│   ├── agno/                         # Agno examples
│   │   ├── 01_semantic_chunking.ipynb
│   │   └── 02_contextual_chunking.ipynb
│   └── langchain/                    # LangChain examples
│       └── 01_contextual_chunking.ipynb
│
├── data/                             # Data directory
│   └── pdfs/                         # PDF files
│
├── sql/                              # Database schemas
│   └── schema.sql
│
└── docs/                             # Documentation
    ├── README.md
    ├── STRUCTURE.md
    ├── SETUP.md
    ├── AGNO_VS_LANGCHAIN.md
    └── DEPLOY.md
```

## 🎯 Key Principles

**Framework Independence**: Each framework has its own implementation. No shared code that depends on specific frameworks.

**Why?** Agno uses `agno.knowledge.document.Document`, LangChain uses `langchain_core.documents.Document`. Prefer duplication over wrong abstraction.

## 🚀 Usage

### Agno
```python
from src.rag.agno import AgnoKnowledgeBase, ContextualAgnoKnowledgeBase

# Fast
kb = AgnoKnowledgeBase(table_name="docs")
kb.ingest_directory("data/pdfs")

# Best quality
kb = ContextualAgnoKnowledgeBase(table_name="docs_enhanced")
kb.ingest_directory("data/pdfs")
```

### LangChain
```python
from src.rag.langchain import ContextualLangChainKnowledgeBase

kb = ContextualLangChainKnowledgeBase(collection_name="docs")
kb.ingest_directory("data/pdfs")
```

## 🔧 Scripts

```bash
# Agno
poetry run python scripts/agno/ingest_semantic.py --directory data/pdfs
poetry run python scripts/agno/ingest_contextual.py --directory data/pdfs

# LangChain
poetry run python scripts/langchain/ingest.py --directory data/pdfs

# Download PDFs
poetry run python scripts/shared/download_pdfs.py
```

## 🔄 Migration

**Old:**
```python
from src.storage.agno_knowledge import AgnoKnowledge
from src.storage.contextual_langchain_knowledge import ContextualLangChainKnowledge
```

**New:**
```python
from src.rag.agno import AgnoKnowledgeBase, ContextualAgnoKnowledgeBase
from src.rag.langchain import ContextualLangChainKnowledgeBase
```
