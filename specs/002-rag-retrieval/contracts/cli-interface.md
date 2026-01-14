# CLI Interface Contract: RAG Retrieval Module

**Date**: 2026-01-12
**Feature**: 002-rag-retrieval

## Overview

The retrieval module is a CLI tool executed via `python retrieve.py`. It performs semantic search against Qdrant and optionally runs validation tests.

## Command Interface

### Search Mode (Default)

```bash
python retrieve.py "<query>" [OPTIONS]
```

### Validation Mode

```bash
python retrieve.py --validate [OPTIONS]
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| query | STRING | Yes (in search mode) | Semantic search query text |

## Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--top-k` | INT | 5 | Number of results to return (1-20) |
| `--chapter` | STRING | None | Filter results by chapter/module |
| `--validate` | FLAG | False | Run validation test suite |
| `--verbose` | FLAG | False | Show detailed timing breakdown |
| `--json` | FLAG | False | Output results as JSON |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `COHERE_API_KEY` | Yes | Cohere API authentication |
| `QDRANT_URL` | Yes | Qdrant Cloud cluster URL |
| `QDRANT_API_KEY` | Yes | Qdrant API authentication |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | No results found (search mode) or validation failed |
| 2 | Configuration error (missing env vars) |
| 3 | Connection error (Qdrant/Cohere unreachable) |

## Output Format

### Search Mode (Standard)

```
RAG Retrieval
=============
Query: "What is ROS 2 and how does it work?"
Results: 5 | Latency: 0.847s

1. [0.89] module-1-ros2
   Section: What is ROS 2?
   URL: https://physical-ai.../docs/module-1-ros2/1-1-introduction
   Preview: ROS 2 (Robot Operating System 2) is a set of software libraries...

2. [0.84] module-1-ros2
   Section: ROS 2 Architecture Overview
   URL: https://physical-ai.../docs/module-1-ros2/1-2-architecture
   Preview: The ROS 2 architecture consists of nodes that communicate...

3. [0.81] module-1-ros2
   Section: Module Overview
   URL: https://physical-ai.../docs/module-1-ros2
   Preview: This module introduces the fundamentals of ROS 2...

4. [0.76] module-1-ros2
   Section: Installing ROS 2
   URL: https://physical-ai.../docs/module-1-ros2/1-1-introduction
   Preview: To install ROS 2 Humble on Ubuntu 22.04...

5. [0.71] module-2-simulation
   Section: ROS 2 and Gazebo Integration
   URL: https://physical-ai.../docs/module-2-simulation/2-6-urdf-to-gazebo
   Preview: Loading your robot model into Gazebo requires...

Timing: Query embed: 0.312s | Search: 0.535s | Total: 0.847s
```

### Search Mode (JSON)

```json
{
  "query": "What is ROS 2?",
  "results": [
    {
      "rank": 1,
      "score": 0.89,
      "chapter": "module-1-ros2",
      "section_title": "What is ROS 2?",
      "source_url": "https://...",
      "content": "ROS 2 (Robot Operating System 2)...",
      "chunk_id": "a1b2c3d4_0"
    }
  ],
  "timing": {
    "query_embed_ms": 312,
    "search_ms": 535,
    "total_ms": 847
  },
  "metadata": {
    "top_k": 5,
    "chapter_filter": null
  }
}
```

### Validation Mode

```
RAG Retrieval Validation
========================

Test 1: "What is ROS 2 and how does it work?"
  Expected: module-1-ros2
  Found: module-1-ros2 (4/5), module-2-simulation (1/5)
  Relevance: ✓ PASS (4 of 5 from expected chapter)
  Metadata: ✓ PASS (all fields present)
  Latency: ✓ PASS (0.847s < 2.0s)

Test 2: "How do I simulate a robot in Gazebo?"
  Expected: module-2-simulation
  Found: module-2-simulation (5/5)
  Relevance: ✓ PASS (5 of 5 from expected chapter)
  Metadata: ✓ PASS (all fields present)
  Latency: ✓ PASS (0.723s < 2.0s)

... (3 more tests)

Summary
-------
Tests: 5/5 passed
Average latency: 0.812s
Metadata integrity: 100%

✓ VALIDATION PASSED
```

### Validation Mode (JSON)

```json
{
  "timestamp": "2026-01-12T14:30:00Z",
  "total_tests": 5,
  "passed_tests": 5,
  "failed_tests": 0,
  "avg_latency_ms": 812,
  "overall_pass": true,
  "results": [
    {
      "query": "What is ROS 2 and how does it work?",
      "expected_chapter": "module-1-ros2",
      "actual_chapters": {"module-1-ros2": 4, "module-2-simulation": 1},
      "relevance_pass": true,
      "metadata_complete": true,
      "latency_ms": 847,
      "latency_pass": true
    }
  ]
}
```

## Error Output

### Missing Environment Variables

```
ERROR: Missing required environment variables:
  - COHERE_API_KEY: not set

Please set them in your .env file.

Exit code: 2
```

### Connection Error

```
ERROR: Cannot connect to Qdrant Cloud
  URL: https://xxx.qdrant.io:6333
  Error: Connection timeout

Please verify your QDRANT_URL and QDRANT_API_KEY.

Exit code: 3
```

### Empty Collection

```
WARNING: Collection 'physical-ai-textbook' is empty or does not exist.

Please run the ingestion pipeline first:
  python main.py

Exit code: 1
```

### No Results

```
Query: "quantum entanglement in robotics"
Results: 0

No semantically similar content found.
Try a different query or check the collection contents.

Exit code: 1
```

## Usage Examples

### Basic Search
```bash
python retrieve.py "How do I create a ROS 2 node?"
```

### Search with More Results
```bash
python retrieve.py "navigation and path planning" --top-k 10
```

### Search Within a Chapter
```bash
python retrieve.py "sensors" --chapter module-2-simulation
```

### Run Validation Suite
```bash
python retrieve.py --validate
```

### JSON Output for Scripting
```bash
python retrieve.py "voice commands" --json > results.json
```

### Verbose Timing
```bash
python retrieve.py "robot simulation" --verbose
```
