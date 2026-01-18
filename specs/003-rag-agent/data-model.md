# Data Model: RAG Pipeline – Agent Construction with Retrieval

**Date**: 2026-01-16
**Feature Branch**: `003-rag-agent`

## Overview

This document defines the data structures used in the RAG agent feature. The agent reuses existing data models from `backend/retrieve.py` and introduces new structures for agent-specific concerns.

---

## Existing Entities (from retrieve.py)

These entities are imported and reused from the existing retrieval module.

### SearchResult

Represents a single retrieved chunk from the vector database.

| Field | Type | Description |
|-------|------|-------------|
| `score` | `float` | Relevance score (0.0-1.0, higher = more relevant) |
| `content` | `str` | The text content of the chunk |
| `source_url` | `str` | URL to the book page containing this chunk |
| `section_title` | `str` | Title of the section within the page |
| `chunk_id` | `str` | Unique identifier for the chunk |
| `chapter` | `str` | Chapter/module name (e.g., "module-1-ros2") |
| `page_title` | `str` | Title of the source page |
| `position` | `int` | Position of chunk within the source page |
| `content_hash` | `str` | MD5 hash for content integrity verification |

**Validation Rules**:
- `score` must be between 0.0 and 1.0
- `content` must not be empty
- `source_url` must be a valid URL format
- `chunk_id` must be non-empty string

### ResultSet

Collection of search results with query metadata.

| Field | Type | Description |
|-------|------|-------------|
| `query` | `str` | The original search query text |
| `results` | `list[SearchResult]` | Ordered list of retrieved chunks |
| `total_count` | `int` | Number of results returned |
| `query_time_ms` | `float` | Time to generate query embedding |
| `search_time_ms` | `float` | Time for vector search |
| `total_time_ms` | `float` | Total retrieval time |

---

## New Entities (agent-specific)

### AgentQuery

Represents an incoming user query to the agent.

| Field | Type | Description |
|-------|------|-------------|
| `text` | `str` | The user's question text |
| `top_k` | `int` | Number of chunks to retrieve (default: 5) |
| `relevance_threshold` | `float` | Minimum score for relevance (default: 0.5) |

**Validation Rules**:
- `text` must not be empty or whitespace-only
- `top_k` must be between 1 and 20
- `relevance_threshold` must be between 0.0 and 1.0

### SourceCitation

Represents a citation to source material in the response.

| Field | Type | Description |
|-------|------|-------------|
| `chapter` | `str` | Chapter/module identifier |
| `section` | `str` | Section title within the chapter |
| `url` | `str` | Direct link to the source page |
| `relevance_score` | `float` | How relevant this source was to the query |

### AgentResponse

Represents the complete response from the agent.

| Field | Type | Description |
|-------|------|-------------|
| `answer` | `str` | The generated answer text |
| `sources` | `list[SourceCitation]` | Citations used in the answer |
| `has_relevant_context` | `bool` | Whether relevant content was found |
| `retrieval_time_ms` | `float` | Time spent on retrieval |
| `generation_time_ms` | `float` | Time spent on LLM generation |
| `total_time_ms` | `float` | Total end-to-end time |

**Validation Rules**:
- `answer` must not be empty
- `sources` may be empty if `has_relevant_context` is False
- All time values must be non-negative

### AgentError

Represents an error condition in agent execution.

| Field | Type | Description |
|-------|------|-------------|
| `error_type` | `str` | Category of error (e.g., "retrieval", "generation", "validation") |
| `message` | `str` | User-friendly error message |
| `details` | `str | None` | Technical details for logging (not shown to user) |

**Error Types**:
- `validation`: Invalid input (empty query, bad parameters)
- `retrieval`: Qdrant or Cohere API failure
- `generation`: OpenAI API failure
- `no_context`: No relevant content found (threshold)

---

## Entity Relationships

```
AgentQuery
    │
    ▼
┌───────────────────────────────────────┐
│         semantic_search()             │
│  (existing retrieval function)        │
└───────────────────────────────────────┘
    │
    ▼
ResultSet ─────────► list[SearchResult]
    │
    ▼
┌───────────────────────────────────────┐
│         format_context()              │
│  (transform for LLM consumption)      │
└───────────────────────────────────────┘
    │
    ▼
┌───────────────────────────────────────┐
│         OpenAI Agent                  │
│  (generate grounded response)         │
└───────────────────────────────────────┘
    │
    ▼
AgentResponse ─────► list[SourceCitation]
    or
AgentError
```

---

## State Transitions

### Query Processing States

```
RECEIVED ──► VALIDATING ──► RETRIEVING ──► GENERATING ──► COMPLETE
    │            │              │              │
    └────────────┴──────────────┴──────────────┴──────► ERROR
```

| State | Description | Exits To |
|-------|-------------|----------|
| RECEIVED | Query received from user | VALIDATING |
| VALIDATING | Checking query parameters | RETRIEVING, ERROR |
| RETRIEVING | Fetching context from Qdrant | GENERATING, ERROR |
| GENERATING | LLM producing response | COMPLETE, ERROR |
| COMPLETE | Response returned to user | (terminal) |
| ERROR | Error condition occurred | (terminal) |

---

## Constants

| Constant | Value | Description |
|----------|-------|-------------|
| `DEFAULT_TOP_K` | 5 | Default number of chunks to retrieve |
| `DEFAULT_RELEVANCE_THRESHOLD` | 0.5 | Minimum score for "relevant" content |
| `MAX_TOP_K` | 20 | Maximum allowed top_k value |
| `MAX_QUERY_LENGTH` | 2000 | Maximum query text length (characters) |
| `COLLECTION_NAME` | "physical-ai-textbook" | Qdrant collection name |
