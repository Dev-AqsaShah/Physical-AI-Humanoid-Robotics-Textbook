# Implementation Plan: RAG Pipeline – Agent Construction with Retrieval

**Branch**: `003-rag-agent` | **Date**: 2026-01-16 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-rag-agent/spec.md`

## Summary

Build an AI agent using the OpenAI Agents SDK that answers questions about the Physical AI textbook by retrieving context from the existing Qdrant vector database. The agent uses the existing `semantic_search()` function from `backend/retrieve.py` as a tool, grounds all responses in retrieved content, and includes source citations.

## Technical Context

**Language/Version**: Python 3.9+
**Primary Dependencies**: `openai-agents` (v0.6.6), existing `cohere`, `qdrant-client`, `python-dotenv`, `rich`
**Storage**: N/A (uses existing Qdrant Cloud vector database)
**Testing**: Built-in validation suite with `--test` flag (matches existing `retrieve.py` pattern)
**Target Platform**: CLI (Windows/Linux/macOS)
**Project Type**: Single module (agent.py in project root)
**Performance Goals**: <10s end-to-end response time for 95% of queries
**Constraints**: Must use existing retrieval function, no new embeddings, no deployment concerns
**Scale/Scope**: Single-user CLI tool, same scale as existing retrieval module

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Spec-First Writing | PASS | Implementation follows approved spec.md |
| II. Clarity for Readers | PASS | Agent outputs clear answers with citations |
| III. Accuracy and Correctness | PASS | Responses grounded in verified book content |
| IV. Modular Documentation | PASS | Agent is self-contained module |
| V. Professional Technical Writing | PASS | Code follows existing patterns |
| VI. Docusaurus/GitHub Pages | N/A | Agent is backend code, not documentation |

**Post-Phase 1 Re-check**: All gates pass. The design maintains modularity by keeping agent logic separate from existing retrieval code.

## Project Structure

### Documentation (this feature)

```text
specs/003-rag-agent/
├── plan.md              # This file
├── research.md          # Phase 0 output - OpenAI Agents SDK research
├── data-model.md        # Phase 1 output - entity definitions
├── quickstart.md        # Phase 1 output - getting started guide
├── contracts/
│   ├── cli-interface.md      # CLI contract
│   └── programmatic-api.md   # Python API contract
└── tasks.md             # Phase 2 output (created by /sp.tasks)
```

### Source Code (repository root)

```text
hackathon-1/
├── agent.py             # NEW: Main agent implementation (single file)
├── backend/
│   ├── main.py          # Existing: Ingestion pipeline
│   └── retrieve.py      # Existing: Retrieval module (imported by agent)
├── .env                 # Existing: Environment variables (add OPENAI_API_KEY)
└── requirements.txt     # Existing: Dependencies (add openai-agents)
```

**Structure Decision**: Single `agent.py` file in project root as specified by user. The agent imports from `backend/retrieve.py` for retrieval functionality, maintaining separation of concerns while keeping the new code self-contained.

## Design Decisions

### 1. Agent Architecture

**Decision**: Single agent with retrieval tool, no handoffs or multi-agent orchestration.

**Rationale**:
- User explicitly excluded "advanced tool orchestration"
- Single agent is simpler and meets all requirements
- Can be extended to multi-agent later if needed

### 2. Tool Integration Pattern

**Decision**: Wrap `semantic_search()` with `@function_tool` decorator.

**Implementation**:
```python
@function_tool
async def retrieve_book_context(query: str, top_k: int = 5) -> str:
    """Retrieve relevant content from the Physical AI textbook."""
    result_set = semantic_search(query=query, top_k=top_k)
    return format_context_with_citations(result_set)
```

**Rationale**:
- Preserves existing retrieval logic
- Formats output for LLM consumption
- Automatic schema generation via decorator

### 3. Grounding Strategy

**Decision**: Explicit system instructions + relevance threshold check.

**System Prompt**:
```
You are a helpful assistant that answers questions about the Physical AI &
Humanoid Robotics textbook. You MUST:
1. ONLY use information from the retrieved context
2. Cite sources using [Chapter: Section] format
3. Say "I don't have information about that" when context is insufficient
4. Never fabricate information not in the context
```

**Threshold**: 0.5 relevance score (from spec FR-005)

### 4. Error Handling

**Decision**: Catch-all with categorized user messages.

| Error | User Message | Exit Code |
|-------|--------------|-----------|
| Missing env var | "Configuration error: {VAR} not set" | 2 |
| Qdrant failure | "Knowledge base temporarily unavailable" | 3 |
| OpenAI failure | "Response generation temporarily unavailable" | 3 |
| No results | "I couldn't find relevant information..." | 1 |

### 5. Output Format

**Decision**: Rich console output by default, JSON option for integration.

**Rationale**: Matches existing `retrieve.py` pattern with `--json` flag.

## Implementation Phases

### Phase 1: Core Agent Setup
- Create `agent.py` with imports and constants
- Define agent with system instructions
- Implement retrieval tool wrapper

### Phase 2: Response Formatting
- Format context for LLM consumption
- Parse and structure agent response
- Add source citations to output

### Phase 3: CLI Interface
- Add argument parsing (argparse)
- Implement query mode
- Implement test mode
- Add JSON output option

### Phase 4: Error Handling & Logging
- Wrap API calls with try-except
- Add logging for debugging
- Implement graceful error messages

### Phase 5: Validation Suite
- Define test queries (in-scope and out-of-scope)
- Implement validation logic
- Generate validation report

## Dependencies

### New Package

```
openai-agents>=0.6.6
```

### Existing Packages (no changes)

```
cohere
qdrant-client
python-dotenv
rich
```

### Environment Variables

| Variable | Status | Purpose |
|----------|--------|---------|
| `OPENAI_API_KEY` | NEW | OpenAI API for agent |
| `COHERE_API_KEY` | Existing | Query embeddings |
| `QDRANT_URL` | Existing | Vector database |
| `QDRANT_API_KEY` | Existing | Qdrant authentication |

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| OpenAI rate limits | Use reasonable defaults, document retry behavior |
| Hallucination | Explicit grounding instructions, relevance threshold |
| Slow responses | Log timing, set expectations (<10s in spec) |
| API changes | Pin `openai-agents` version |

## Complexity Tracking

> No constitution violations requiring justification.

The implementation stays within complexity bounds:
- Single file as requested
- Single agent (no multi-agent orchestration)
- Reuses existing retrieval code
- Follows existing project patterns

## Artifacts Generated

| Artifact | Path | Description |
|----------|------|-------------|
| Research | `specs/003-rag-agent/research.md` | SDK research and decisions |
| Data Model | `specs/003-rag-agent/data-model.md` | Entity definitions |
| CLI Contract | `specs/003-rag-agent/contracts/cli-interface.md` | Command-line interface |
| API Contract | `specs/003-rag-agent/contracts/programmatic-api.md` | Python API |
| Quickstart | `specs/003-rag-agent/quickstart.md` | Getting started guide |

## Next Steps

Run `/sp.tasks` to generate the detailed task breakdown for implementation.
