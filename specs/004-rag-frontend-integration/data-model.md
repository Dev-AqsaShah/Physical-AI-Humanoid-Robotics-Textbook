# Data Model: RAG Pipeline – Backend and Frontend Integration

**Feature**: 004-rag-frontend-integration
**Date**: 2026-01-17

## Overview

This document defines the data structures for frontend-backend communication. These models extend the existing `AgentResponse` and `SourceCitation` classes from `agent.py`.

---

## Entities

### QueryRequest

Request payload sent from frontend to backend.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `question` | string | Yes | User's question (1-2000 chars) |
| `selected_text` | string | No | Text selected by user for context (max 5000 chars) |
| `top_k` | integer | No | Number of chunks to retrieve (1-20, default: 5) |
| `threshold` | float | No | Relevance threshold (0.0-1.0, default: 0.5) |

**Validation Rules**:
- `question` must be non-empty after trimming whitespace
- `question` maximum length: 2000 characters
- `selected_text` maximum length: 5000 characters
- `top_k` range: 1-20
- `threshold` range: 0.0-1.0

---

### QueryResponse

Response payload sent from backend to frontend.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `answer` | string | Yes | Generated response text |
| `sources` | SourceCitation[] | Yes | List of source citations (may be empty) |
| `has_relevant_context` | boolean | Yes | Whether relevant context was found |
| `timing` | TimingInfo | Yes | Performance metrics |

---

### SourceCitation

Reference to a textbook section used in the response.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `chapter` | string | Yes | Chapter identifier (e.g., "Module 1: ROS 2") |
| `section` | string | Yes | Section title |
| `url` | string | Yes | URL to the section in the book |
| `relevance_score` | float | Yes | Similarity score (0.0-1.0) |

---

### TimingInfo

Performance metrics for the query.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `retrieval_ms` | float | Yes | Time spent on vector search |
| `generation_ms` | float | Yes | Time spent on LLM generation |
| `total_ms` | float | Yes | Total request time |

---

### ErrorResponse

Error response for failed requests.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `error` | string | Yes | Error type identifier |
| `message` | string | Yes | Human-readable error message |
| `detail` | string | No | Additional error details |

**Error Types**:
- `validation_error`: Invalid request parameters
- `agent_error`: Agent processing failed
- `timeout_error`: Request timed out
- `internal_error`: Unexpected server error

---

### HealthResponse

Health check response.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `status` | string | Yes | "healthy" or "unhealthy" |
| `agent_ready` | boolean | Yes | Whether agent is initialized |

---

## Entity Relationships

```
QueryRequest
    └── triggers → QueryResponse
                       ├── answer (string)
                       ├── sources[] → SourceCitation
                       │                   ├── chapter
                       │                   ├── section
                       │                   ├── url
                       │                   └── relevance_score
                       ├── has_relevant_context
                       └── timing → TimingInfo
                                       ├── retrieval_ms
                                       ├── generation_ms
                                       └── total_ms
```

---

## State Transitions

### Frontend Chat State

```
IDLE → LOADING → SUCCESS | ERROR
  ↑__________________|________|
```

| State | Description | User Action |
|-------|-------------|-------------|
| `IDLE` | Ready for input | Can type and submit |
| `LOADING` | Waiting for response | Input disabled |
| `SUCCESS` | Answer displayed | Can ask new question |
| `ERROR` | Error displayed | Can retry |

---

## Mapping to Existing Types

The backend models map directly to existing `agent.py` types:

| API Model | agent.py Type |
|-----------|---------------|
| `QueryResponse` | `AgentResponse` |
| `SourceCitation` | `SourceCitation` |

Conversion is straightforward using `dataclasses.asdict()`.
