# API Contract: retrieve.py Module

**Feature**: 002-rag-retrieval
**Date**: 2026-01-13
**Type**: Python CLI Module

## Module Interface

### Public Functions

#### 1. `semantic_search(query: str, top_k: int = 5, chapter_filter: str | None = None) -> ResultSet`

Perform semantic search against the vector database.

**Parameters**:
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| query | str | Yes | - | Search query text |
| top_k | int | No | 5 | Number of results (1-20) |
| chapter_filter | str | No | None | Filter by chapter name |

**Returns**: `ResultSet` dataclass

**Errors**:
| Error Type | Condition | Exit Code |
|------------|-----------|-----------|
| ValueError | Empty query | - |
| ConnectionError | Qdrant unavailable | 3 |
| RuntimeError | Empty collection | - |

**Example**:
```python
from retrieve import semantic_search

results = semantic_search("What is ROS 2?", top_k=5)
for hit in results.results:
    print(f"{hit.score:.2f}: {hit.section_title}")
```

---

#### 2. `validate_retrieval() -> ValidationReport`

Run validation test suite with representative queries.

**Parameters**: None

**Returns**: `ValidationReport` dataclass

**Validation Checks**:
1. Relevance: Top result matches expected chapter
2. Metadata: All required fields present
3. Latency: Query completes under 2 seconds
4. Integrity: Content field non-empty

---

#### 3. `get_collection_stats() -> dict`

Get vector collection statistics (read-only).

**Returns**:
```python
{
    "collection_name": str,
    "vector_count": int,
    "status": str  # "ready" | "empty" | "not_found"
}
```

---

## CLI Interface

### Usage

```bash
python retrieve.py [QUERY] [OPTIONS]
python retrieve.py --validate
python retrieve.py --stats
```

### Arguments

| Argument | Description |
|----------|-------------|
| QUERY | Search query text (positional) |

### Options

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| --top-k | -k | int | 5 | Number of results |
| --chapter | -c | str | None | Filter by chapter |
| --json | -j | flag | False | Output as JSON |
| --validate | -v | flag | False | Run validation suite |
| --stats | -s | flag | False | Show collection stats |

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | No results found |
| 2 | Missing API credentials |
| 3 | Connection failure |
| 4 | Validation failed |

---

## Data Structures

### ResultSet

```python
@dataclass
class ResultSet:
    query: str
    results: list[SearchResult]
    total_count: int
    query_time_ms: float
    search_time_ms: float
    total_time_ms: float
```

### SearchResult

```python
@dataclass
class SearchResult:
    score: float
    content: str
    source_url: str
    section_title: str
    chunk_id: str
    chapter: str
    page_title: str
    position: int
    content_hash: str
```

### ValidationReport

```python
@dataclass
class ValidationReport:
    timestamp: str
    total_tests: int
    passed_tests: int
    failed_tests: int
    results: list[ValidationResult]
    avg_latency_ms: float
    overall_pass: bool
```

### ValidationResult

```python
@dataclass
class ValidationResult:
    query_text: str
    expected_chapter: str
    top_chapter: str
    relevance_pass: bool
    metadata_complete: bool
    latency_ms: float
    latency_pass: bool
    pass_all: bool
```

---

## Output Formats

### Console Output (Default)

```
RAG Retrieval Results
=====================
Query: "What is ROS 2?"
Results: 5 | Time: 0.823s

1. [0.66] module-1-ros2
   Section: Why ROS 2?
   URL: https://physical-ai-humanoid.../docs/module-1-ros2
   Preview: Just as the human nervous system...

2. [0.52] module-1-ros2
   ...
```

### JSON Output (--json)

```json
{
  "query": "What is ROS 2?",
  "total_count": 5,
  "total_time_ms": 823.45,
  "results": [
    {
      "score": 0.66,
      "content": "Just as the human nervous system...",
      "source_url": "https://...",
      "section_title": "Why ROS 2?",
      "chunk_id": "abc123_0",
      "chapter": "module-1-ros2"
    }
  ]
}
```

### Validation Output (--validate)

```
RAG Retrieval Validation
========================
Running 5 test queries...

1. [PASS] "What is ROS 2?" -> module-1-ros2 (0.52s)
2. [PASS] "Gazebo simulation" -> module-2-simulation (0.48s)
3. [PASS] "Isaac Sim" -> module-3-isaac (0.61s)
4. [PASS] "VLA models" -> module-4-vla (0.55s)
5. [PASS] "Capstone project" -> capstone (0.49s)

Summary
-------
Tests: 5/5 passed
Average latency: 0.53s
Metadata integrity: 100%

[PASS] VALIDATION PASSED
```

---

## Read-Only Guarantee

This module performs **read-only** operations only:

**Allowed Operations**:
- `query_points()` - Semantic search
- `get_collection()` - Collection info
- `scroll()` - Iterate points (validation only)

**Forbidden Operations** (not called):
- `upsert()` - Write vectors
- `delete()` - Remove vectors
- `create_collection()` - Create collection
- `update_collection()` - Modify collection
- `update_vectors()` - Modify vectors

If the collection does not exist, the module exits with an error message directing the user to run the ingestion pipeline first.
