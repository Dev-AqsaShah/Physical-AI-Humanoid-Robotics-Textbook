# CLI Interface Contract: RAG Pipeline Ingestion

**Date**: 2026-01-12
**Feature**: 001-rag-pipeline

## Overview

The ingestion pipeline is a CLI tool executed via `python main.py`. It reads markdown files, generates embeddings, and stores vectors in Qdrant.

## Command Interface

### Main Command

```bash
python main.py [OPTIONS]
```

### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--book-path` | PATH | `../Physical-AI-Humanoid-Robotics-Textbook/book/docs` | Path to book docs directory |
| `--collection` | STRING | `physical-ai-textbook` | Qdrant collection name |
| `--dry-run` | FLAG | False | Parse and chunk without storing |
| `--verbose` | FLAG | False | Enable detailed logging |

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `COHERE_API_KEY` | Yes | Cohere API authentication |
| `QDRANT_URL` | Yes | Qdrant Cloud cluster URL |
| `QDRANT_API_KEY` | Yes | Qdrant API authentication |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success - all pages ingested |
| 1 | Partial failure - some pages failed |
| 2 | Configuration error - missing env vars |
| 3 | Connection error - cannot reach external services |

## Output Format

### Standard Output (Success)

```
RAG Pipeline Ingestion
======================
Book path: ../Physical-AI-Humanoid-Robotics-Textbook/book/docs
Collection: physical-ai-textbook

[1/40] Processing module-1-ros2/index.md... ✓ (4 chunks)
[2/40] Processing module-1-ros2/1-1-introduction.md... ✓ (6 chunks)
...

Summary
-------
Pages processed: 40/40
Chunks created: 187
Vectors stored: 187
Time elapsed: 5m 23s
```

### Standard Error (Failures)

```
ERROR: [15/40] module-2-simulation/2-3-physics.md
  Cohere API rate limit exceeded. Retrying in 60s...
  Retry 1/3 failed. Retry 2/3...
  ✓ Recovered after 2 retries

WARNING: [22/40] module-3-isaac/3-5-vslam.md
  Page has no text content (images only). Skipping.
```

### Dry Run Output

```
DRY RUN - No vectors will be stored

[1/40] module-1-ros2/index.md
  Title: "ROS 2 Foundations"
  Chunks: 4
  Chunk sizes: [892, 1204, 756, 1102]

[2/40] module-1-ros2/1-1-introduction.md
  Title: "Introduction to ROS 2"
  Chunks: 6
  Chunk sizes: [1045, 889, 1320, 967, 1156, 723]
...

Summary
-------
Total pages: 40
Total chunks: 187
Estimated vectors: 187
Estimated storage: ~0.8 MB
```

## Verification Query

After successful ingestion, the pipeline runs a verification query:

```python
# Verification query
query = "What is ROS 2 and how does it work?"
results = collection.search(query_vector, limit=5)

# Expected output
Verification Query Results
--------------------------
Query: "What is ROS 2 and how does it work?"

1. [0.89] module-1-ros2/1-1-introduction.md
   Section: "What is ROS 2?"
   Preview: "ROS 2 (Robot Operating System 2) is a set of..."

2. [0.84] module-1-ros2/1-2-architecture.md
   Section: "ROS 2 Architecture Overview"
   Preview: "The ROS 2 architecture consists of nodes..."

3. [0.81] module-1-ros2/index.md
   Section: "Module Overview"
   Preview: "This module introduces the fundamentals..."

✓ Verification passed: Top results are semantically relevant
```

## Error Handling

### Missing Environment Variables

```
ERROR: Missing required environment variables:
  - COHERE_API_KEY: not set
  - QDRANT_URL: not set

Please create a .env file with these variables.
See .env.example for the template.

Exit code: 2
```

### Connection Failures

```
ERROR: Cannot connect to Qdrant Cloud
  URL: https://xxx.qdrant.io:6333
  Error: Connection timeout after 30s

Please verify:
  1. QDRANT_URL is correct
  2. QDRANT_API_KEY is valid
  3. Network connectivity to Qdrant Cloud

Exit code: 3
```

### Partial Failures

```
WARNING: Ingestion completed with errors

Failed pages (3):
  - module-2-simulation/2-4-sensor-simulation.md: Cohere API error
  - module-3-isaac/3-3-synthetic-data.md: Empty content
  - capstone/cap-5-vision.md: Chunk too large

Successfully processed: 37/40 pages
Vectors stored: 162/187

Re-run the pipeline to retry failed pages.

Exit code: 1
```
