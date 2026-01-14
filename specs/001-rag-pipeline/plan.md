# Implementation Plan: RAG Pipeline – Content Ingestion, Embeddings, and Vector Storage

**Branch**: `001-rag-pipeline` | **Date**: 2026-01-12 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-rag-pipeline/spec.md`

## Summary

Build a Python-based content ingestion pipeline that reads the Physical AI textbook markdown files, chunks content semantically, generates embeddings via Cohere, and stores vectors in Qdrant Cloud with full metadata for RAG retrieval.

**Key Technical Decisions**:
- Read local markdown files directly (not HTTP crawling)
- Single `main.py` file per user specification
- Semantic chunking based on markdown headers
- Deterministic point IDs for idempotent upserts

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: cohere, qdrant-client, python-dotenv, rich
**Storage**: Qdrant Cloud (Free Tier) - vector database
**Testing**: Manual verification via sample queries
**Target Platform**: CLI tool (Windows/Linux/macOS)
**Project Type**: Single script (all logic in main.py per user spec)
**Performance Goals**: Process 40 pages in <10 minutes
**Constraints**: Cohere rate limit (100 calls/min), Qdrant free tier (1GB)
**Scale/Scope**: 40 pages, ~150-200 chunks, ~1MB vector storage

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Spec-First Writing | ✅ PASS | Implementation follows approved spec.md |
| II. Clarity for Readers | ✅ PASS | N/A - backend code, not documentation |
| III. Accuracy and Correctness | ✅ PASS | All API contracts verified against official docs |
| IV. Modular Documentation | ✅ PASS | Plan artifacts organized per template |
| V. Professional Technical Writing | ✅ PASS | N/A - backend code |
| VI. Docusaurus Compatibility | ✅ PASS | N/A - not generating book content |

**Gate Result**: PASS - No violations. This feature is infrastructure code supporting the book, not book content itself.

## Project Structure

### Documentation (this feature)

```text
specs/001-rag-pipeline/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0: Technical decisions
├── data-model.md        # Phase 1: Entity definitions
├── quickstart.md        # Phase 1: Setup guide
├── contracts/           # Phase 1: Interface definitions
│   ├── cli-interface.md
│   └── external-apis.md
├── tasks.md             # Phase 2 output (/sp.tasks)
└── checklists/
    └── requirements.md  # Spec validation checklist
```

### Source Code (repository root)

```text
backend/
├── main.py              # All ingestion logic (single file per user spec)
├── pyproject.toml       # uv project configuration
├── .env.example         # Environment variable template
└── .env                 # Local credentials (gitignored)
```

**Structure Decision**: Single project layout with all logic in `main.py` per user specification. No separate modules, services, or test directories - simplest viable implementation.

## Implementation Approach

### Pipeline Flow

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  1. Discovery   │────>│  2. Extraction  │────>│  3. Chunking    │
│  Find .md files │     │  Read & parse   │     │  Split on H2/H3 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  6. Verify      │<────│  5. Store       │<────│  4. Embed       │
│  Sample query   │     │  Qdrant upsert  │     │  Cohere API     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Key Implementation Details

**1. File Discovery**
- Glob pattern: `**/docs/**/*.md`
- Skip: `_category_.json`, non-markdown files
- Result: ~40 markdown files

**2. Content Extraction**
- Parse YAML frontmatter for title/metadata
- Extract body content after frontmatter
- Derive chapter name from parent directory

**3. Semantic Chunking**
- Primary split: H2 (`##`) headers
- Keep H3 content with parent H2
- Target: 500-1500 characters per chunk
- Overlap: 100 characters for context

**4. Embedding Generation**
- Model: `embed-english-v3.0` (1024 dimensions)
- Input type: `search_document`
- Batch size: 96 texts per API call
- Retry: Exponential backoff on rate limits

**5. Vector Storage**
- Collection: `physical-ai-textbook`
- Point ID: UUID from `sha256(path + index)`
- Payload: source_url, section_title, chunk_id, chapter, position, content_hash, content
- Operation: Upsert (idempotent)

**6. Verification**
- Query: "What is ROS 2 and how does it work?"
- Success: Top-5 results include relevant ROS 2 content
- Report: Total vectors stored, query results

### Idempotency Implementation

```python
# Deterministic ID generation
point_id = uuid.UUID(hashlib.sha256(f"{file_path}:{chunk_index}".encode()).hexdigest()[:32])

# Upsert always overwrites existing points with same ID
# Re-running pipeline on unchanged content = no duplicates
```

### Error Handling

| Error Type | Response |
|------------|----------|
| Missing .env vars | Exit code 2, clear instructions |
| Cohere rate limit | Exponential backoff, 3 retries |
| Cohere API error | Log, skip chunk, continue |
| Qdrant connection | Exit code 3, connection help |
| Empty page content | Log warning, skip page |
| Chunk too large | Split further or truncate |

## Dependencies

### Python Packages

| Package | Version | Purpose |
|---------|---------|---------|
| cohere | ^5.0 | Embedding generation |
| qdrant-client | ^1.7 | Vector database client |
| python-dotenv | ^1.0 | Environment variables |
| rich | ^13.0 | Progress bars, formatted output |

### External Services

| Service | Configuration | Credentials |
|---------|---------------|-------------|
| Cohere | embed-english-v3.0, 1024 dims | `COHERE_API_KEY` |
| Qdrant Cloud | Free tier, Cosine distance | `QDRANT_URL`, `QDRANT_API_KEY` |

## Complexity Tracking

> No Constitution Check violations to justify.

| Item | Decision | Rationale |
|------|----------|-----------|
| Single file | `main.py` only | User specification; simplest viable approach |
| No tests | Manual verification | Scope constraint; verification query validates correctness |
| Local files | Direct read vs crawl | Faster, more reliable, cleaner content |

## Acceptance Criteria Mapping

| Spec Requirement | Implementation |
|------------------|----------------|
| FR-001: Crawl/accept URLs | Read local markdown files directly |
| FR-002: Extract clean text | Parse markdown, skip frontmatter |
| FR-003: Semantic chunking | Split on H2/H3 headers |
| FR-004: Cohere embeddings | embed-english-v3.0 model |
| FR-005: Qdrant storage | physical-ai-textbook collection |
| FR-006: Metadata | source_url, section_title, chunk_id |
| FR-007: Idempotent | Deterministic UUIDs + upsert |
| FR-008: Graceful failures | Try/catch + continue pattern |
| FR-009: Logging | rich console output |
| FR-010: Verification | Sample query after ingestion |

## Next Steps

Run `/sp.tasks` to generate the implementation task breakdown.
