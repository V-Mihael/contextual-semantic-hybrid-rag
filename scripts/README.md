# Scripts Directory

Ingestion scripts organized by framework.

## 📁 Structure

```
scripts/
├── agno/           # Agno framework scripts
├── langchain/      # LangChain framework scripts
└── shared/         # Shared utilities
```

## 🚀 Usage

### Agno Scripts

**Semantic Chunking (Fast)**
```bash
poetry run python scripts/agno/ingest_semantic.py --directory data/pdfs --table my_docs
```

**Contextual Chunking (Best Quality)**
```bash
poetry run python scripts/agno/ingest_contextual.py --directory data/pdfs --table my_docs_enhanced
```

### LangChain Scripts

**Contextual Semantic Chunking**
```bash
poetry run python scripts/langchain/ingest.py --directory data/pdfs --collection my_docs
```

### Shared Scripts

**Download Sample PDFs**
```bash
poetry run python scripts/shared/download_pdfs.py
```

## 📝 Parameters

### Agno Scripts
- `--directory`: Path to PDF directory (default: `data/pdfs`)
- `--table`: PostgreSQL table name (default varies by script)

### LangChain Scripts
- `--directory`: Path to PDF directory (default: `data/pdfs`)
- `--collection`: PostgreSQL collection name (default: `economics_enhanced_langchain`)

## 📚 See Also

- [Main README](../README.md)
- [Structure Documentation](../STRUCTURE.md)
- [Migration Guide](../MIGRATION.md)
