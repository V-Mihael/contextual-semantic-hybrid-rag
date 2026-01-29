# Agno vs LangChain Implementation

This project now supports **two implementations** of the same RAG system:

## 🔵 Agno Implementation
**Files**: 
- `src/rag/agno/knowledge_base.py` (semantic chunking)
- `src/rag/agno/contextual_knowledge_base.py` (contextual enhancement)

### Features
- Native PDF reading with `PDFReader`
- Built-in hybrid search (vector + BM25)
- Integrated agent framework
- Simpler API with fewer dependencies
- Direct integration with Gemini embeddings

### Usage
```python
from src.rag.agno import ContextualAgnoKnowledgeBase
from agno.agent import Agent
from agno.models.google import Gemini

kb = ContextualAgnoKnowledgeBase()
kb.ingest_directory("data/pdfs")

agent = Agent(
    model=Gemini(id="gemini-2.5-flash"),
    knowledge=kb.knowledge,
    search_knowledge=True
)
agent.print_response("Your question here")
```

### Ingestion
```bash
poetry run python scripts/agno/ingest_contextual.py --directory data/pdfs
```

### Notebook
- `notebooks/agno/02_contextual_chunking.ipynb`

---

## 🟢 LangChain Implementation
**File**: `src/rag/langchain/contextual_knowledge_base.py`

### Features
- Standard LangChain ecosystem
- Compatible with LangChain chains and agents
- More flexibility for custom workflows
- Extensive community integrations
- Retriever interface for advanced patterns

### Usage
```python
from src.rag.langchain import ContextualLangChainKnowledgeBase
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA

kb = ContextualLangChainKnowledgeBase()
kb.ingest_directory("data/pdfs")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=kb.as_retriever()
)
result = qa_chain.invoke({"query": "Your question here"})
```

### Ingestion
```bash
poetry run python scripts/langchain/ingest.py --directory data/pdfs
```

### Notebook
- `notebooks/langchain/01_contextual_chunking.ipynb`

---

## Comparison

| Feature | Agno | LangChain |
|---------|------|-----------|
| **Setup Complexity** | ⭐⭐ Simple | ⭐⭐⭐ Moderate |
| **Code Lines** | ~10 lines | ~15 lines |
| **Hybrid Search** | ✅ Built-in | ⚠️ Manual setup |
| **Agent Framework** | ✅ Native | ⚠️ Requires LangGraph |
| **Ecosystem** | 🔵 Agno-specific | 🟢 Large community |
| **Flexibility** | ⭐⭐⭐ Good | ⭐⭐⭐⭐ Excellent |
| **Learning Curve** | ⭐⭐ Easy | ⭐⭐⭐ Moderate |

---

## Common Features (Both)

Both implementations share:
- ✅ **Semantic Chunking** via Chonkie
- ✅ **Contextual Enhancement** with LLM-generated headers
- ✅ **PGVector** for vector storage
- ✅ **Google Gemini** embeddings
- ✅ Same chunking strategy and quality

---

## When to Use Which?

### Use Agno if:
- You want the simplest setup
- You need built-in hybrid search
- You prefer an integrated agent framework
- You're building a prototype quickly

### Use LangChain if:
- You need LangChain ecosystem compatibility
- You want maximum flexibility
- You're integrating with existing LangChain code
- You need advanced chain patterns (LCEL, etc.)

---

## Installation

Both implementations are included. Install dependencies:

```bash
poetry install
```

This installs both Agno and LangChain packages.

---

## Architecture

Both implementations use the same underlying architecture:

```
PDF → PyPDFLoader/PDFReader → Semantic Chunking → LLM Context → Embed → PgVector
                                                                              ↓
                                                    Query → Hybrid Search → Answer
```

The only difference is the **framework layer** on top of PGVector.
