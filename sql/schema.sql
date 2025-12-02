-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Documents table
CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    source TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Chunks table with vector embeddings and FTS
CREATE TABLE IF NOT EXISTS chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    contextualized_content TEXT,
    embedding vector(1536),
    chunk_index INTEGER,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_chunks_document_id ON chunks(document_id);
CREATE INDEX IF NOT EXISTS idx_chunks_embedding ON chunks USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
CREATE INDEX IF NOT EXISTS idx_chunks_fts ON chunks USING gin(to_tsvector('english', content));

-- Hybrid search function (Vector + FTS with RRF)
CREATE OR REPLACE FUNCTION hybrid_search(
    query_embedding vector(1536),
    query_text TEXT,
    match_count INT DEFAULT 10,
    vector_weight FLOAT DEFAULT 0.5
)
RETURNS TABLE (
    id UUID,
    document_id UUID,
    content TEXT,
    contextualized_content TEXT,
    similarity FLOAT,
    fts_rank FLOAT,
    combined_score FLOAT
) AS $$
BEGIN
    RETURN QUERY
    WITH vector_search AS (
        SELECT 
            c.id,
            c.document_id,
            c.content,
            c.contextualized_content,
            1 - (c.embedding <=> query_embedding) AS similarity,
            ROW_NUMBER() OVER (ORDER BY c.embedding <=> query_embedding) AS rank
        FROM chunks c
        WHERE c.embedding IS NOT NULL
        ORDER BY c.embedding <=> query_embedding
        LIMIT match_count * 2
    ),
    fts_search AS (
        SELECT 
            c.id,
            ts_rank(to_tsvector('english', c.content), plainto_tsquery('english', query_text)) AS rank_score,
            ROW_NUMBER() OVER (ORDER BY ts_rank(to_tsvector('english', c.content), plainto_tsquery('english', query_text)) DESC) AS rank
        FROM chunks c
        WHERE to_tsvector('english', c.content) @@ plainto_tsquery('english', query_text)
        ORDER BY rank_score DESC
        LIMIT match_count * 2
    )
    SELECT 
        vs.id,
        vs.document_id,
        vs.content,
        vs.contextualized_content,
        vs.similarity,
        COALESCE(fs.rank_score, 0) AS fts_rank,
        (vector_weight * (1.0 / (60 + vs.rank)) + (1 - vector_weight) * (1.0 / (60 + COALESCE(fs.rank, 1000)))) AS combined_score
    FROM vector_search vs
    LEFT JOIN fts_search fs ON vs.id = fs.id
    ORDER BY combined_score DESC
    LIMIT match_count;
END;
$$ LANGUAGE plpgsql;
