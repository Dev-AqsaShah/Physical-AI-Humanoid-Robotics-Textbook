# Research: RAG Pipeline – Agent Construction with Retrieval

**Date**: 2026-01-16
**Feature Branch**: `003-rag-agent`

## Research Summary

This document consolidates research findings for implementing a RAG agent using the OpenAI Agents SDK integrated with the existing Qdrant retrieval pipeline.

---

## 1. OpenAI Agents SDK Integration

### Decision
Use the `openai-agents` Python package (v0.6.6) with the `@function_tool` decorator to expose the existing `semantic_search()` function as an agent tool.

### Rationale
- **Lightweight framework**: The SDK has minimal abstractions and integrates directly with OpenAI's API
- **Function tools**: The `@function_tool` decorator automatically generates JSON schemas from Python type hints, enabling seamless integration with existing code
- **Built-in tracing**: Provides debugging and monitoring via OpenAI's trace viewer
- **Production-ready**: Designed as a production upgrade from OpenAI's experimental Swarm project

### Alternatives Considered
| Alternative | Rejected Because |
|-------------|------------------|
| LangChain | Heavier framework with more abstractions than needed for this single-agent use case |
| Custom OpenAI API calls | Would require manual prompt construction and tool call handling; SDK handles this |
| Semantic Kernel | Microsoft-centric; less direct OpenAI integration |

### Key SDK Components to Use
- `Agent`: Core class for creating the RAG agent with instructions
- `Runner.run()`: Async execution method for running agent queries
- `@function_tool`: Decorator to expose retrieval as a callable tool
- `RunContextWrapper`: For passing context to tools if needed

---

## 2. Retrieval Integration Pattern

### Decision
Create a wrapper function around `semantic_search()` decorated with `@function_tool` that formats results for LLM consumption.

### Rationale
- The existing `semantic_search()` returns a `ResultSet` dataclass with `SearchResult` objects
- The agent needs context formatted as text with source citations
- Keeping retrieval logic separate maintains modularity and testability

### Implementation Pattern
```python
@function_tool
async def retrieve_book_context(query: str, top_k: int = 5) -> str:
    """Retrieve relevant content from the Physical AI textbook.

    Args:
        query: The question or topic to search for
        top_k: Number of chunks to retrieve (default 5)

    Returns:
        Formatted context with source citations
    """
    result_set = semantic_search(query=query, top_k=top_k)
    # Format results for LLM consumption
    return format_context_for_agent(result_set)
```

### Alternatives Considered
| Alternative | Rejected Because |
|-------------|------------------|
| Direct ResultSet to agent | Agent needs formatted text, not dataclass objects |
| Modify semantic_search() | Would break existing CLI interface; wrapper maintains separation |
| RAG as system prompt only | Would not allow dynamic retrieval per query |

---

## 3. Response Grounding Strategy

### Decision
Use explicit system instructions to enforce grounding, combined with relevance score thresholds to detect unanswerable queries.

### Rationale
- The agent instructions will explicitly state: "Only answer based on the provided context"
- Relevance score threshold (0.5) from the retrieval function indicates if content is relevant
- When all results have low scores, the agent is instructed to decline answering

### System Prompt Template
```
You are a helpful assistant that answers questions about the Physical AI &
Humanoid Robotics textbook. You MUST follow these rules:

1. ONLY use information from the retrieved context to answer questions
2. If the context does not contain relevant information, say so clearly
3. Always cite your sources using [Chapter: Section] format
4. Never make up information not present in the context
5. If asked about topics outside the book, explain you can only answer
   about Physical AI and Humanoid Robotics topics covered in the textbook
```

### Alternatives Considered
| Alternative | Rejected Because |
|-------------|------------------|
| Fine-tuned model | Out of scope; requires training data and ongoing maintenance |
| RAG with reranking | Adds complexity; existing Cohere embeddings provide sufficient relevance |
| Multiple retrieval rounds | Over-engineering for initial implementation |

---

## 4. Error Handling Strategy

### Decision
Wrap all API calls (Cohere, Qdrant, OpenAI) with try-except blocks and return user-friendly error messages.

### Rationale
- FR-009 requires graceful error handling
- Users should not see stack traces or technical errors
- Logging enables debugging while maintaining UX

### Error Categories
| Error Type | User Message | Action |
|------------|--------------|--------|
| Qdrant connection | "Knowledge base temporarily unavailable" | Log error, return message |
| Cohere API | "Search service temporarily unavailable" | Log error, return message |
| OpenAI API | "Response generation temporarily unavailable" | Log error, return message |
| No relevant results | "I couldn't find relevant information..." | Return with explanation |
| Empty query | "Please provide a question" | Return validation message |

---

## 5. File Structure Decision

### Decision
Create a single `agent.py` file in the project root as specified, containing all agent logic.

### Rationale
- User requirement explicitly specifies single file in project root
- Keeps agent logic self-contained and easy to run
- Imports from existing `backend/retrieve.py` for retrieval functionality

### File Organization
```python
# agent.py (project root)

# Imports
from agents import Agent, Runner, function_tool
from backend.retrieve import semantic_search, ResultSet, SearchResult

# Constants and configuration

# Tool functions (decorated)

# Agent definition

# Main execution function

# CLI entry point
```

---

## 6. Testing Approach

### Decision
Include representative test queries in the agent module for validation, with a `--test` CLI flag.

### Rationale
- Success criteria require validation against book-related queries
- Embedded test queries enable quick validation without separate test file
- Aligns with existing `retrieve.py` pattern (has `--validate` flag)

### Test Query Categories
1. **In-scope questions**: Topics covered in the book (ROS 2, Gazebo, Isaac Sim, VLA models)
2. **Out-of-scope questions**: Topics not in the book (quantum computing, web development)
3. **Edge cases**: Vague queries, typos, very specific questions

---

## 7. Dependencies

### New Dependencies Required
| Package | Version | Purpose |
|---------|---------|---------|
| `openai-agents` | ^0.6.6 | OpenAI Agents SDK |

### Existing Dependencies (already in project)
| Package | Purpose |
|---------|---------|
| `cohere` | Query embedding generation |
| `qdrant-client` | Vector database access |
| `python-dotenv` | Environment variable loading |
| `rich` | Console output formatting |

### Environment Variables Required
| Variable | Purpose |
|----------|---------|
| `OPENAI_API_KEY` | OpenAI API authentication (new) |
| `COHERE_API_KEY` | Cohere embedding API (existing) |
| `QDRANT_URL` | Qdrant Cloud endpoint (existing) |
| `QDRANT_API_KEY` | Qdrant Cloud authentication (existing) |

---

## References

- [OpenAI Agents SDK Documentation](https://openai.github.io/openai-agents-python/)
- [OpenAI Agents SDK GitHub](https://github.com/openai/openai-agents-python)
- [OpenAI Agents SDK PyPI](https://pypi.org/project/openai-agents/)
- [OpenAI Platform Agents Guide](https://platform.openai.com/docs/guides/agents-sdk)
