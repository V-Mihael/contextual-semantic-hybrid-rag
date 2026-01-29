# Agno vs LangChain

## 🔵 Agno

**Files**: `src/rag/agno/`

**Features**: Native PDF reading, built-in hybrid search, integrated agent framework

**Usage**:
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
agent.print_response("Your question")
```

**Ingest**: `poetry run python scripts/agno/ingest_contextual.py --directory data/pdfs`

---

## 🟢 LangChain

**Files**: `src/rag/langchain/`

**Features**: LangChain ecosystem, retriever interface, extensive integrations

**Usage**:
```python
from src.rag.langchain import ContextualLangChainKnowledgeBase
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA

kb = ContextualLangChainKnowledgeBase()
kb.ingest_directory("data/pdfs")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=kb.as_retriever())
result = qa_chain.invoke({"query": "Your question"})
```

**Ingest**: `poetry run python scripts/langchain/ingest.py --directory data/pdfs`

---

## Comparison

| Feature | Agno | LangChain |
|---------|------|-----------|
| Setup | Simple | Moderate |
| Hybrid Search | Built-in | Manual |
| Agent Framework | Native | Requires LangGraph |
| Ecosystem | Agno-specific | Large community |
| Flexibility | Good | Excellent |

## When to Use

**Agno**: Simplest setup, built-in features, quick prototyping

**LangChain**: Maximum flexibility, ecosystem compatibility, advanced patterns
