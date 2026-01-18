# Implementation Plan: RAG Pipeline – Backend and Frontend Integration

**Branch**: `004-rag-frontend-integration` | **Date**: 2026-01-17 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-rag-frontend-integration/spec.md`

## Summary

Integrate the existing RAG agent with the Docusaurus book frontend by creating a FastAPI backend (`app.py`) that exposes query endpoints, and embedding a chatbot UI component in the book frontend. The frontend communicates with the backend via HTTP requests, enabling readers to ask questions and receive grounded answers with citations.

## Technical Context

**Language/Version**: Python 3.11+ (backend), JavaScript/React 19 (frontend via Docusaurus 3.9)
**Primary Dependencies**: FastAPI, uvicorn, pydantic (backend); React, Docusaurus (frontend)
**Storage**: N/A (uses existing Qdrant vector database via agent.py)
**Testing**: Manual end-to-end validation; curl/browser testing
**Target Platform**: Local development (localhost)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: Response within 15 seconds per query (per SC-001)
**Constraints**: Local-only, no authentication, reuse existing agent.py
**Scale/Scope**: Single user local development

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Spec-First Writing | ✅ PASS | Implementation follows approved spec.md |
| II. Clarity for Readers | ✅ PASS | UI designed for beginner-friendly Q&A |
| III. Accuracy and Correctness | ✅ PASS | Reuses verified agent.py and retrieve.py |
| IV. Modular Documentation | ✅ PASS | Chatbot is separate component, doesn't alter content |
| V. Professional Technical Writing | ✅ PASS | Error messages are user-friendly |
| VI. Docusaurus Compatibility | ✅ PASS | Custom component follows Docusaurus patterns |

**Gate Result**: PASS - No violations

## Project Structure

### Documentation (this feature)

```text
specs/004-rag-frontend-integration/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── api.yaml         # OpenAPI spec
└── tasks.md             # Phase 2 output (created by /sp.tasks)
```

### Source Code (repository root)

```text
# Backend (project root)
app.py                   # FastAPI application - single file
agent.py                 # Existing RAG agent (reused)
backend/
├── retrieve.py          # Existing retrieval logic (reused)
└── pyproject.toml       # Add fastapi, uvicorn dependencies

# Frontend (book directory)
book/
├── src/
│   ├── components/
│   │   └── Chatbot/
│   │       ├── index.js       # Main chatbot component
│   │       └── styles.module.css
│   ├── theme/
│   │   └── Root.js            # Wrap app with chatbot
│   └── css/
│       └── custom.css         # Chatbot styling additions
├── docusaurus.config.js       # No changes needed
└── package.json               # No new dependencies (use fetch API)
```

**Structure Decision**: Web application pattern with backend at project root (`app.py`) and frontend components embedded in existing `book/` Docusaurus structure. No new dependencies in frontend—use native fetch API.

## Complexity Tracking

> No Constitution violations requiring justification.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |
