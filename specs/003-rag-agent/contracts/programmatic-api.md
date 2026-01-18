# Programmatic API Contract: RAG Agent

**Date**: 2026-01-16
**Feature Branch**: `003-rag-agent`

## Overview

The RAG agent provides a programmatic Python API for integration and testing. This document defines the public interface.

---

## Module: `agent`

### Function: `ask`

The primary entry point for querying the agent programmatically.

```python
async def ask(
    query: str,
    top_k: int = 5,
    relevance_threshold: float = 0.5
) -> AgentResponse:
    """
    Ask a question to the RAG agent.

    Args:
        query: The question to ask about the Physical AI textbook
        top_k: Number of chunks to retrieve (1-20, default: 5)
        relevance_threshold: Minimum relevance score (0.0-1.0, default: 0.5)

    Returns:
        AgentResponse with answer and source citations

    Raises:
        ValueError: If query is empty or parameters are out of range
        ConnectionError: If Qdrant or API services are unavailable
        RuntimeError: If agent execution fails
    """
```

**Example Usage**:
```python
import asyncio
from agent import ask

async def main():
    response = await ask("What is ROS 2?")
    print(response.answer)
    for source in response.sources:
        print(f"  - {source.chapter}: {source.section}")

asyncio.run(main())
```

---

### Function: `ask_sync`

Synchronous wrapper for environments that don't support async.

```python
def ask_sync(
    query: str,
    top_k: int = 5,
    relevance_threshold: float = 0.5
) -> AgentResponse:
    """
    Synchronous version of ask().

    Args:
        query: The question to ask
        top_k: Number of chunks to retrieve
        relevance_threshold: Minimum relevance score

    Returns:
        AgentResponse with answer and source citations
    """
```

**Example Usage**:
```python
from agent import ask_sync

response = ask_sync("How do I simulate a robot in Gazebo?")
print(response.answer)
```

---

### Function: `run_validation`

Run the built-in validation test suite.

```python
async def run_validation() -> ValidationReport:
    """
    Run validation test suite against the agent.

    Returns:
        ValidationReport with test results and metrics

    Raises:
        ConnectionError: If services are unavailable
    """
```

**Example Usage**:
```python
import asyncio
from agent import run_validation

async def main():
    report = await run_validation()
    print(f"Passed: {report.passed_tests}/{report.total_tests}")
    print(f"Overall: {'PASS' if report.overall_pass else 'FAIL'}")

asyncio.run(main())
```

---

## Data Classes

### AgentResponse

```python
@dataclass
class AgentResponse:
    answer: str                      # The generated answer text
    sources: list[SourceCitation]    # Citations used in answer
    has_relevant_context: bool       # Whether relevant content was found
    retrieval_time_ms: float         # Time spent on retrieval
    generation_time_ms: float        # Time spent on generation
    total_time_ms: float             # Total end-to-end time
```

### SourceCitation

```python
@dataclass
class SourceCitation:
    chapter: str          # Chapter/module identifier
    section: str          # Section title
    url: str              # Direct link to source
    relevance_score: float # Relevance score (0.0-1.0)
```

### ValidationReport

```python
@dataclass
class ValidationReport:
    timestamp: str                    # ISO timestamp
    total_tests: int                  # Number of tests run
    passed_tests: int                 # Number passed
    failed_tests: int                 # Number failed
    results: list[TestResult]         # Individual test results
    avg_response_time_ms: float       # Average response time
    overall_pass: bool                # Overall pass/fail
```

### TestResult

```python
@dataclass
class TestResult:
    query: str                   # Test query text
    expected_behavior: str       # What was expected
    actual_behavior: str         # What happened
    passed: bool                 # Pass/fail status
    response_time_ms: float      # Response time
    details: str | None          # Additional details
```

---

## Error Handling

The API raises specific exceptions for different error conditions:

| Exception | Condition | Recovery |
|-----------|-----------|----------|
| `ValueError` | Invalid input parameters | Fix input and retry |
| `ConnectionError` | Service unavailable | Check connectivity, retry later |
| `RuntimeError` | Agent execution failure | Check logs, may need investigation |

**Example Error Handling**:
```python
import asyncio
from agent import ask

async def safe_ask(query: str):
    try:
        response = await ask(query)
        return response.answer
    except ValueError as e:
        return f"Invalid query: {e}"
    except ConnectionError as e:
        return f"Service unavailable: {e}"
    except RuntimeError as e:
        return f"Agent error: {e}"

asyncio.run(safe_ask("What is ROS 2?"))
```

---

## Constants

```python
# Available for import
DEFAULT_TOP_K: int = 5
DEFAULT_RELEVANCE_THRESHOLD: float = 0.5
MAX_TOP_K: int = 20
MAX_QUERY_LENGTH: int = 2000
```

---

## Integration Example

Complete example showing programmatic usage:

```python
#!/usr/bin/env python3
"""Example: Using the RAG agent programmatically."""

import asyncio
import json
from agent import ask, run_validation, AgentResponse

async def interactive_demo():
    """Demo the agent with several queries."""

    queries = [
        "What is ROS 2?",
        "How do I create a simulation in Gazebo?",
        "What is quantum computing?",  # Out of scope
    ]

    for query in queries:
        print(f"\n{'='*60}")
        print(f"Q: {query}")
        print('='*60)

        response = await ask(query)

        if response.has_relevant_context:
            print(f"\nA: {response.answer}\n")
            print("Sources:")
            for src in response.sources:
                print(f"  - [{src.relevance_score:.2f}] {src.chapter}: {src.section}")
        else:
            print(f"\n{response.answer}")

        print(f"\n(Response time: {response.total_time_ms/1000:.2f}s)")

async def validate():
    """Run validation suite."""
    report = await run_validation()
    print(f"\nValidation: {report.passed_tests}/{report.total_tests} passed")
    return report.overall_pass

if __name__ == "__main__":
    asyncio.run(interactive_demo())
```
