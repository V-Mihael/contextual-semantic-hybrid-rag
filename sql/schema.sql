-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Agno will automatically create tables with this structure:
-- - Table name: specified in your code (e.g., 'philosophy_docs')
-- - Columns: id, name, meta_data, content, embedder, embedding, usage
-- - Indexes: vector similarity (HNSW or IVFFlat)

-- Optional: Create full-text search index for hybrid search
-- This enhances Agno's hybrid search capabilities

-- Note: Run this AFTER Agno creates the table
-- Replace 'philosophy_docs' with your actual table name

-- CREATE INDEX IF NOT EXISTS idx_philosophy_docs_fts 
-- ON philosophy_docs USING gin(to_tsvector('english', content));

-- CREATE INDEX IF NOT EXISTS idx_philosophy_enhanced_fts 
-- ON philosophy_docs_enhanced USING gin(to_tsvector('english', content));
