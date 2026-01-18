# CLI Interface Contract: RAG Agent

**Date**: 2026-01-16
**Feature Branch**: `003-rag-agent`

## Overview

The RAG agent provides a command-line interface for querying the Physical AI textbook. This document defines the CLI contract.

---

## Command Syntax

```bash
python agent.py [OPTIONS] [QUERY]
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `QUERY` | string | No | The question to ask (required unless using --test) |

## Options

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--top-k` | `-k` | int | 5 | Number of chunks to retrieve |
| `--threshold` | `-t` | float | 0.5 | Minimum relevance score threshold |
| `--json` | `-j` | flag | false | Output response as JSON |
| `--test` | | flag | false | Run validation test suite |
| `--verbose` | `-v` | flag | false | Show detailed retrieval info |
| `--help` | `-h` | flag | | Show help message |

---

## Usage Examples

### Basic Query
```bash
python agent.py "What is ROS 2?"
```

### Query with Options
```bash
python agent.py -k 10 -t 0.6 "How do I simulate a robot in Gazebo?"
```

### JSON Output
```bash
python agent.py --json "What are vision-language-action models?"
```

### Run Test Suite
```bash
python agent.py --test
```

### Verbose Mode
```bash
python agent.py -v "Explain the capstone project requirements"
```

---

## Output Formats

### Standard Output (Default)

```
Question: What is ROS 2?

Answer:
ROS 2 (Robot Operating System 2) is a set of software libraries and tools for
building robot applications. According to the textbook, ROS 2 provides...

Sources:
[1] Module 1: ROS 2 Fundamentals > Introduction to ROS 2
    https://physical-ai-textbook.../docs/module-1-ros2/intro
[2] Module 1: ROS 2 Fundamentals > ROS 2 Architecture
    https://physical-ai-textbook.../docs/module-1-ros2/architecture

Response time: 2.3s (retrieval: 0.8s, generation: 1.5s)
```

### No Relevant Context Output

```
Question: What is quantum computing?

I couldn't find relevant information about "quantum computing" in the Physical
AI & Humanoid Robotics textbook. This topic may not be covered in the current
curriculum.

The textbook covers topics including:
- ROS 2 fundamentals
- Robot simulation with Gazebo
- NVIDIA Isaac Sim
- Vision-Language-Action models
- Capstone projects

Would you like to ask about one of these topics instead?
```

### JSON Output Format

```json
{
  "query": "What is ROS 2?",
  "answer": "ROS 2 (Robot Operating System 2) is a set of...",
  "has_relevant_context": true,
  "sources": [
    {
      "chapter": "module-1-ros2",
      "section": "Introduction to ROS 2",
      "url": "https://physical-ai-textbook.../docs/module-1-ros2/intro",
      "relevance_score": 0.89
    }
  ],
  "timing": {
    "retrieval_ms": 823,
    "generation_ms": 1502,
    "total_ms": 2325
  }
}
```

### Error Output

```
Error: Knowledge base temporarily unavailable.

Please ensure:
- QDRANT_URL and QDRANT_API_KEY are set in your environment
- Network connectivity to Qdrant Cloud is available

For debugging, run with --verbose flag.
```

### Test Suite Output

```
RAG Agent Validation Suite
==========================
Running 8 test queries...

[PASS] "What is ROS 2?" -> module-1-ros2 (0.89, 1.2s)
[PASS] "How do I simulate in Gazebo?" -> module-2-simulation (0.85, 1.1s)
[PASS] "What is Isaac Sim?" -> module-3-isaac (0.82, 1.3s)
[PASS] "How do VLA models work?" -> module-4-vla (0.78, 1.4s)
[PASS] "Capstone requirements?" -> capstone (0.81, 1.2s)
[PASS] "What is quantum computing?" -> [NO CONTEXT] (0.23, 0.9s)
[PASS] "Tell me about web dev" -> [NO CONTEXT] (0.18, 0.8s)
[PASS] "ros2 nod list" (typo) -> module-1-ros2 (0.72, 1.1s)

Summary
-------
Tests: 8/8 passed
Average response time: 1.1s
Out-of-scope detection: 2/2 correct

[PASS] VALIDATION PASSED
```

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | No relevant context found (graceful) |
| 2 | Configuration error (missing env vars) |
| 3 | Connection error (Qdrant/Cohere/OpenAI) |
| 4 | Validation test failure |

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key for agent |
| `COHERE_API_KEY` | Yes | Cohere API key for embeddings |
| `QDRANT_URL` | Yes | Qdrant Cloud endpoint |
| `QDRANT_API_KEY` | Yes | Qdrant Cloud API key |

---

## Verbose Output

When `--verbose` is enabled, additional information is displayed:

```
Question: What is ROS 2?

[Retrieval]
Query embedding time: 234ms
Vector search time: 589ms
Results returned: 5

[Context Chunks]
1. [0.89] module-1-ros2 > Introduction to ROS 2
   "ROS 2 (Robot Operating System 2) is the next generation..."
2. [0.85] module-1-ros2 > ROS 2 Architecture
   "The architecture of ROS 2 differs significantly from..."
3. [0.79] module-1-ros2 > Getting Started
   "To begin working with ROS 2, you first need to..."
4. [0.71] module-1-ros2 > Nodes and Topics
   "In ROS 2, nodes are the fundamental building blocks..."
5. [0.68] module-2-simulation > ROS 2 Integration
   "Gazebo integrates seamlessly with ROS 2 through..."

[Generation]
Model: gpt-4o
Tokens: 847 (prompt) + 256 (completion)
Generation time: 1502ms

Answer:
ROS 2 (Robot Operating System 2) is a set of software libraries and tools...

Sources:
[1] Module 1: ROS 2 Fundamentals > Introduction to ROS 2
...
```
