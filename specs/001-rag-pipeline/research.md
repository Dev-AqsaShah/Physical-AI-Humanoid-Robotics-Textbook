# Research: RAG Pipeline – Content Ingestion, Embeddings, and Vector Storage

**Date**: 2026-01-12
**Feature**: 001-rag-pipeline
**Status**: Complete

## Technical Decisions

### 1. Book Content Source

**Decision**: Ingest from local markdown files rather than crawling deployed URLs

**Rationale**:
- Book content exists as markdown files at `Physical-AI-Humanoid-Robotics-Textbook/book/docs/`
- Direct file access is faster, more reliable, and avoids network dependencies
- Markdown is cleaner for chunking than HTML (no boilerplate extraction needed)
- 40 total pages across 5 modules + intro

**Alternatives Considered**:
- HTTP crawling deployed Vercel URL: Adds complexity, network dependency, and HTML parsing overhead
- Sitemap parsing: Book doesn't have a dedicated sitemap file

### 2. Python Project Setup

**Decision**: Use `uv` for Python project initialization per user specification

**Rationale**:
- User explicitly requested uv for project setup
- uv provides fast dependency resolution and virtual environment management
- Modern Python packaging with pyproject.toml support

**Configuration**:
- Python version: 3.11+ (required for modern type hints and async features)
- Single `main.py` file per user specification
- Dependencies managed via uv

### 3. Text Chunking Strategy

**Decision**: Semantic chunking based on markdown structure (headers + paragraphs)

**Rationale**:
- Markdown headers provide natural semantic boundaries
- Each H2/H3 section forms a coherent topic unit
- Preserves context better than fixed-size character splits
- Optimized for retrieval (not summarization) per spec

**Implementation**:
- Split on H2 (`##`) headers as primary chunk boundaries
- Keep H3 (`###`) content with parent H2 section
- Target chunk size: 500-1500 characters (optimal for embedding models)
- Overlap: 100 characters between chunks for context continuity

### 4. Cohere Embedding Model

**Decision**: Use `embed-english-v3.0` model

**Rationale**:
- Latest Cohere embedding model with 1024 dimensions
- Strong performance on retrieval tasks
- Book content is primarily English technical documentation
- Free tier available for development/testing

**API Details**:
- Endpoint: `https://api.cohere.ai/v1/embed`
- Input type: `search_document` for ingestion, `search_query` for retrieval
- Batch size: Up to 96 texts per request
- Rate limits: 100 calls/minute on free tier

### 5. Qdrant Configuration

**Decision**: Use Qdrant Cloud Free Tier with deterministic point IDs

**Rationale**:
- Free tier provides 1GB storage (sufficient for ~100k vectors)
- Cloud deployment avoids local infrastructure
- Deterministic IDs enable idempotent upserts

**Configuration**:
- Collection name: `physical-ai-textbook`
- Vector size: 1024 (matches Cohere embed-english-v3.0)
- Distance metric: Cosine similarity
- Point ID strategy: Hash of `{source_url}:{chunk_index}` for idempotency

### 6. Metadata Schema

**Decision**: Store comprehensive metadata for retrieval context

**Schema**:
```json
{
  "source_url": "string",      // Relative path to markdown file
  "section_title": "string",   // H2 header text
  "chunk_id": "string",        // Unique identifier: {file_hash}_{chunk_index}
  "chapter": "string",         // Module/chapter name
  "position": "integer",       // Chunk order within document
  "content_hash": "string"     // MD5 of chunk content for change detection
}
```

**Rationale**:
- `content_hash` enables detecting changed content on re-ingestion
- `position` preserves document order for context reconstruction
- `chapter` enables filtered queries by module

### 7. Idempotency Strategy

**Decision**: Upsert with deterministic IDs + content hash comparison

**Rationale**:
- Qdrant's upsert operation naturally handles duplicates
- Deterministic point IDs (hash of source + position) ensure same content maps to same ID
- Content hash in metadata allows detecting actual content changes vs. re-runs

**Implementation**:
- Generate point ID as UUID from `sha256(source_path + chunk_index)`
- On re-run, same content produces same IDs → upsert overwrites (no duplicates)
- Changed content produces different hash → logged as update

### 8. Error Handling Strategy

**Decision**: Fail-forward with comprehensive logging

**Rationale**:
- Single failed page shouldn't block entire ingestion
- Progress tracking enables retry of failed items
- Structured logging enables debugging and monitoring

**Implementation**:
- Try/except around each page processing
- Log failures with full context (URL, error type, stack trace)
- Continue processing remaining pages
- Summary report at end with success/failure counts

## Dependencies

### Python Packages

| Package | Version | Purpose |
|---------|---------|---------|
| cohere | ^5.0 | Embedding generation via Cohere API |
| qdrant-client | ^1.7 | Vector database client |
| python-dotenv | ^1.0 | Environment variable management |
| rich | ^13.0 | Progress bars and formatted logging |

### External Services

| Service | Tier | Credentials Required |
|---------|------|---------------------|
| Cohere API | Free/Trial | `COHERE_API_KEY` |
| Qdrant Cloud | Free (1GB) | `QDRANT_URL`, `QDRANT_API_KEY` |

## File Structure

```text
backend/
├── main.py              # All ingestion logic (single file per user spec)
├── pyproject.toml       # Project config (uv)
├── .env.example         # Environment variable template
└── .env                 # Local credentials (gitignored)
```

## Estimated Scale

| Metric | Estimate |
|--------|----------|
| Total pages | 40 |
| Average page size | ~3,000 characters |
| Chunks per page | ~3-5 |
| Total chunks | ~150-200 |
| Vector dimensions | 1024 |
| Storage required | ~1MB (well within free tier) |
| Ingestion time | ~5-10 minutes |

## Open Questions Resolved

1. **Q: Crawl URLs or read local files?**
   A: Read local markdown files directly for simplicity and reliability.

2. **Q: Which Cohere model?**
   A: `embed-english-v3.0` (1024 dimensions, best for retrieval).

3. **Q: How to ensure idempotency?**
   A: Deterministic point IDs via content hashing + Qdrant upsert.

4. **Q: Chunk size?**
   A: 500-1500 characters with 100-char overlap, split on markdown headers.
