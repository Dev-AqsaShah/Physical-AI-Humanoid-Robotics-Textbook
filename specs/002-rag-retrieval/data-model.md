# Data Model: RAG Pipeline Retrieval

**Date**: 2026-01-12
**Feature**: 002-rag-retrieval

## Entities

### 1. SearchQuery

Represents a user's semantic search request.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| query_text | string | User's search query | Required, non-empty |
| top_k | integer | Number of results to return | Default: 5, Max: 20 |
| chapter_filter | string | Optional module/chapter filter | Must match existing chapter |
| timestamp | datetime | When query was submitted | Auto-generated |

### 2. SearchResult

A single chunk returned from semantic search.

| Field | Type | Description |
|-------|------|-------------|
| score | float | Relevance score (0.0-1.0, higher is more relevant) |
| content | string | Original text content of the chunk |
| source_url | string | URL to the source book page |
| section_title | string | Heading/section title |
| chunk_id | string | Unique identifier for the chunk |
| chapter | string | Module/chapter name |
| position | integer | Chunk order within document |
| content_hash | string | MD5 hash for integrity verification |

### 3. ResultSet

Collection of search results with metadata.

| Field | Type | Description |
|-------|------|-------------|
| query | SearchQuery | The original query |
| results | list[SearchResult] | Ordered list of results by score |
| total_count | integer | Number of results returned |
| query_time_ms | float | Time to generate query embedding |
| search_time_ms | float | Time for Qdrant search |
| total_time_ms | float | End-to-end latency |

### 4. ValidationResult

Result of a single validation test.

| Field | Type | Description |
|-------|------|-------------|
| query_text | string | Test query used |
| expected_chapter | string | Expected primary chapter in results |
| actual_chapters | list[string] | Chapters found in top-k results |
| relevance_pass | boolean | Whether relevance criteria met |
| metadata_complete | boolean | Whether all results have complete metadata |
| latency_ms | float | Query latency |
| latency_pass | boolean | Whether under 2s threshold |

### 5. ValidationReport

Summary of all validation tests.

| Field | Type | Description |
|-------|------|-------------|
| timestamp | datetime | When validation was run |
| total_tests | integer | Number of test queries |
| passed_tests | integer | Tests meeting all criteria |
| failed_tests | integer | Tests failing one or more criteria |
| results | list[ValidationResult] | Individual test results |
| avg_latency_ms | float | Average query latency |
| overall_pass | boolean | All tests passed |

## Relationships

```
SearchQuery (1) ──────> (1) ResultSet
                              │
                              └──< (N) SearchResult

ValidationReport (1) ──< (N) ValidationResult
```

## Data Flow

```
User Query
    │
    ▼
SearchQuery
    │
    ├──> Cohere API (generate embedding)
    │
    ├──> Qdrant (similarity search)
    │
    ▼
ResultSet
    │
    └──> SearchResult[]
```

## Validation Rules

### SearchQuery Validation

1. `query_text` must be non-empty after trimming
2. `query_text` length must be under 2000 characters
3. `top_k` must be between 1 and 20
4. `chapter_filter` must be valid chapter name if provided

### SearchResult Validation

1. `score` must be between 0.0 and 1.0
2. `source_url` must be valid URL format
3. `chunk_id` must be non-empty
4. `content` must be non-empty

### Metadata Completeness Check

A result has complete metadata if ALL of:
- `source_url` is present and valid
- `section_title` is present
- `chunk_id` is present
- `chapter` is present
- `content` is present

## Test Query Mapping

| Query | Expected Chapter |
|-------|-----------------|
| "What is ROS 2 and how does it work?" | module-1-ros2 |
| "How do I simulate a robot in Gazebo?" | module-2-simulation |
| "What is NVIDIA Isaac Sim?" | module-3-isaac |
| "How does voice control work with robots?" | module-4-vla |
| "What is the capstone project about?" | capstone |
