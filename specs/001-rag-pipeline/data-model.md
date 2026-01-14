# Data Model: RAG Pipeline

**Date**: 2026-01-12
**Feature**: 001-rag-pipeline

## Entities

### 1. BookPage

Represents a single markdown file from the textbook.

| Field | Type | Description | Source |
|-------|------|-------------|--------|
| file_path | string | Relative path to markdown file | File system |
| title | string | Page title from frontmatter | YAML frontmatter |
| module | string | Module name (e.g., "module-1-ros2") | Directory name |
| content | string | Raw markdown content | File content |
| sidebar_position | integer | Order within module | YAML frontmatter |

**Derived URL**: `https://physical-ai-humanoid-robotics-textb-two-ecru.vercel.app/docs/{module}/{filename}`

### 2. TextChunk

A semantically meaningful segment of text extracted from a BookPage.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| chunk_id | string | Unique identifier | Format: `{file_hash}_{index}` |
| content | string | Chunk text content | 500-1500 characters |
| source_path | string | Origin file path | FK to BookPage.file_path |
| section_title | string | H2/H3 header text | Extracted from markdown |
| position | integer | Order within document | 0-indexed |
| content_hash | string | MD5 of content | For change detection |

**Uniqueness**: `(source_path, position)` pair is unique

### 3. VectorEmbedding

Stored representation in Qdrant.

| Field | Type | Description |
|-------|------|-------------|
| id | uuid | Deterministic from chunk_id |
| vector | float[1024] | Cohere embedding |
| payload.source_url | string | Web URL for the page |
| payload.section_title | string | Header text |
| payload.chunk_id | string | Reference to TextChunk |
| payload.chapter | string | Module/chapter name |
| payload.position | integer | Chunk order |
| payload.content_hash | string | For idempotency |
| payload.content | string | Original text (for retrieval display) |

### 4. IngestionRecord

Tracks processing status (in-memory during execution).

| Field | Type | Description |
|-------|------|-------------|
| file_path | string | Source file |
| status | enum | pending / processing / success / failed |
| chunks_created | integer | Number of chunks generated |
| error_message | string | Error details if failed |
| processed_at | datetime | Completion timestamp |

## Relationships

```
BookPage (1) ──────< (N) TextChunk
    │                      │
    │                      │
    └─ file_path ──────────┘ source_path

TextChunk (1) ──────< (1) VectorEmbedding
    │                          │
    │                          │
    └─ chunk_id ───────────────┘ payload.chunk_id
```

## State Transitions

### IngestionRecord Lifecycle

```
┌─────────┐     start      ┌────────────┐     success    ┌─────────┐
│ pending │ ──────────────>│ processing │ ──────────────>│ success │
└─────────┘                └────────────┘                └─────────┘
                                 │
                                 │ error
                                 ▼
                           ┌────────┐
                           │ failed │
                           └────────┘
```

## Qdrant Collection Schema

**Collection**: `physical-ai-textbook`

```json
{
  "vectors": {
    "size": 1024,
    "distance": "Cosine"
  },
  "payload_schema": {
    "source_url": { "type": "keyword", "indexed": true },
    "section_title": { "type": "text", "indexed": true },
    "chunk_id": { "type": "keyword", "indexed": true },
    "chapter": { "type": "keyword", "indexed": true },
    "position": { "type": "integer", "indexed": false },
    "content_hash": { "type": "keyword", "indexed": true },
    "content": { "type": "text", "indexed": false }
  }
}
```

## Validation Rules

### TextChunk Validation

1. `content` must be non-empty after whitespace trimming
2. `content` length must be between 100 and 2000 characters
3. `section_title` must not contain markdown syntax
4. `position` must be >= 0

### VectorEmbedding Validation

1. `vector` must have exactly 1024 dimensions
2. `payload.source_url` must be a valid URL format
3. `payload.chunk_id` must match pattern `[a-f0-9]{8}_\d+`

## Indexing Strategy

### Qdrant Indexes

| Field | Index Type | Purpose |
|-------|------------|---------|
| source_url | Keyword | Filter by page |
| chapter | Keyword | Filter by module |
| content_hash | Keyword | Idempotency check |

### Query Patterns

1. **Semantic Search**: Vector similarity on `vector` field
2. **Filter by Module**: `chapter == "module-1-ros2"`
3. **Deduplication Check**: `content_hash == {hash}`
