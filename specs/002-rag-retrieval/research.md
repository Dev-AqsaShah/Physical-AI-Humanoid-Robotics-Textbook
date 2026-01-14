# Research: RAG Pipeline – Retrieval & Validation

**Feature**: 002-rag-retrieval
**Date**: 2026-01-13
**Status**: Complete

## Research Questions Addressed

### 1. Qdrant Query API (qdrant-client >= 1.16)

**Decision**: Use `query_points()` method for semantic search

**Rationale**:
- The `search()` method was deprecated in qdrant-client 1.16+
- `query_points()` is the current standard API
- Already validated in `main.py:523` during ingestion verification

**Implementation Pattern**:
```python
results = qdrant_client.query_points(
    collection_name=COLLECTION_NAME,
    query=query_vector,  # embedding vector
    limit=top_k,
    query_filter=models.Filter(...)  # optional metadata filter
)
# Access results via results.points
```

**Alternatives Considered**:
- `search()` - Deprecated, causes AttributeError
- `scroll()` - For pagination, not semantic search
- `recommend()` - For item-to-item recommendations, not text queries

---

### 2. Cohere Query Embedding Generation

**Decision**: Use `input_type="search_query"` for query embeddings

**Rationale**:
- Cohere's embed-english-v3.0 model distinguishes between document and query embeddings
- Documents use `input_type="search_document"` (used during ingestion)
- Queries use `input_type="search_query"` for asymmetric retrieval
- Already validated in `main.py:517`

**Implementation Pattern**:
```python
response = cohere_client.embed(
    texts=[query_text],
    model="embed-english-v3.0",
    input_type="search_query",
    truncate="END"
)
query_vector = response.embeddings[0]
```

**Alternatives Considered**:
- Using `input_type="search_document"` - Would work but suboptimal for queries
- Using a different model - embed-english-v3.0 is already indexed, must match

---

### 3. Metadata Filtering in Qdrant

**Decision**: Use `models.Filter` with field conditions for chapter/module filtering

**Rationale**:
- Qdrant supports filtering during vector search
- Metadata fields available: `chapter`, `page_title`, `section_title`, `source_url`
- Filter applied server-side for efficiency

**Implementation Pattern**:
```python
from qdrant_client.http import models

filter_condition = models.Filter(
    must=[
        models.FieldCondition(
            key="chapter",
            match=models.MatchValue(value="module-1-ros2")
        )
    ]
)

results = qdrant_client.query_points(
    collection_name=COLLECTION_NAME,
    query=query_vector,
    query_filter=filter_condition,
    limit=top_k
)
```

**Alternatives Considered**:
- Post-filtering in Python - Less efficient, pagination issues
- Separate collection per chapter - Over-engineered for 53 vectors

---

### 4. Performance Measurement

**Decision**: Use Python `time.perf_counter()` for query timing

**Rationale**:
- High precision timing (nanosecond resolution on most systems)
- Measures wall-clock time including I/O
- Standard library, no additional dependencies

**Implementation Pattern**:
```python
import time

start = time.perf_counter()
results = qdrant_client.query_points(...)
elapsed_ms = (time.perf_counter() - start) * 1000
```

**Alternatives Considered**:
- `time.time()` - Lower precision
- `timeit` - For benchmarking, not production timing
- External profilers - Overkill for single query timing

---

### 5. Validation Test Suite Structure

**Decision**: Built-in validation mode with representative test queries

**Rationale**:
- Self-contained validation without external test framework
- Can run as `python retrieve.py --validate`
- Outputs structured validation report

**Test Query Set** (covering all modules):
1. "What is ROS 2 and how does it work?" → expect module-1-ros2
2. "How do I simulate a robot in Gazebo?" → expect module-2-simulation
3. "What is NVIDIA Isaac Sim used for?" → expect module-3-isaac
4. "How do vision-language-action models work?" → expect module-4-vla
5. "What are the capstone project requirements?" → expect capstone

**Validation Criteria**:
- Each query returns results within 2 seconds
- Top result score > 0.4 (semantic relevance threshold)
- Metadata fields present: source_url, section_title, chunk_id, chapter
- Content field matches stored content (no corruption)

**Alternatives Considered**:
- pytest integration tests - Good for CI, but adds complexity
- External validation script - Less maintainable

---

### 6. Error Handling Strategy

**Decision**: Graceful degradation with informative error messages

**Rationale**:
- Read-only operations should not crash the system
- Users need clear feedback on connection/API issues
- Consistent with existing `main.py` patterns

**Error Categories**:
| Error Type | Handling |
|------------|----------|
| Missing API credentials | Exit with code 2, clear message |
| Qdrant connection failure | Exit with code 3, suggest checking URL/key |
| Empty collection | Return empty results with warning |
| Cohere API rate limit | Retry with exponential backoff |
| Query timeout | Return partial results with warning |

---

### 7. Read-Only Operation Guarantee

**Decision**: No write methods in retrieve.py, explicit collection existence check only

**Rationale**:
- Feature requirement: "Confirm read-only operation with no data mutation"
- retrieve.py will only use: `query_points()`, `get_collection()`, `scroll()` (for validation)
- No upsert, delete, create_collection, or update methods

**Verification**:
- Code review confirms no write methods called
- Collection must exist (created by ingestion pipeline)
- If collection missing, exit with clear error, do not create

---

## Resolved Unknowns Summary

| Item | Resolution |
|------|------------|
| Qdrant query API version | `query_points()` for qdrant-client >= 1.16 |
| Query embedding type | `input_type="search_query"` |
| Metadata filtering | `models.Filter` with field conditions |
| Timing measurement | `time.perf_counter()` |
| Validation approach | Built-in validation mode with test queries |
| Error handling | Graceful degradation, exit codes |
| Read-only guarantee | No write methods, explicit check |

## Dependencies Confirmed

- **cohere>=5.0**: Already installed, embed API confirmed working
- **qdrant-client>=1.16**: Already installed (1.16.2), query_points API confirmed
- **python-dotenv>=1.0**: Already installed, .env loading works
- **rich>=13.0**: Already installed, console output confirmed
