# Research: RAG Pipeline – Backend and Frontend Integration

**Feature**: 004-rag-frontend-integration
**Date**: 2026-01-17

## Research Summary

This document captures technology decisions and best practices for integrating the RAG agent with the Docusaurus frontend.

---

## Decision 1: FastAPI Backend Framework

**Decision**: Use FastAPI with uvicorn for the backend API

**Rationale**:
- User constraint explicitly requires FastAPI
- Native async support matches agent.py's async `ask()` function
- Automatic OpenAPI documentation generation
- Pydantic integration for request/response validation
- Lightweight and fast for local development

**Alternatives Considered**:
- Flask: Simpler but no native async, would require wrapping async calls
- Django: Overkill for a single endpoint API
- Starlette: Lower-level, FastAPI provides better developer experience

**Implementation Notes**:
- Single `app.py` file at project root per user requirements
- Import and call `ask()` from agent.py directly
- Use `CORSMiddleware` for cross-origin requests
- Run with: `uvicorn app:app --reload --port 8000`

---

## Decision 2: Frontend Component Architecture

**Decision**: Create a floating chatbot component embedded via Docusaurus theme wrapper

**Rationale**:
- User requires chatbot UI "as part of the book interface"
- Must not alter existing content pages
- Docusaurus `Root.js` theme wrapper is the standard pattern for global components
- Floating UI allows access from any page without modifying docs

**Alternatives Considered**:
- Sidebar plugin: Would alter navigation structure
- MDX component on each page: Requires modifying content files
- Separate page: Breaks "part of the book interface" requirement

**Implementation Notes**:
- Create `book/src/theme/Root.js` to wrap app
- Create `book/src/components/Chatbot/` with React component
- Use CSS modules for scoped styling
- Fixed position at bottom-right corner
- Collapsible/expandable toggle button

---

## Decision 3: Frontend-Backend Communication

**Decision**: Use native Fetch API with JSON payloads

**Rationale**:
- No additional npm dependencies required
- Modern browsers support fetch natively
- Simple JSON request/response pattern
- Easy error handling with try/catch

**Alternatives Considered**:
- Axios: Additional dependency, overkill for single endpoint
- SWR/React Query: Caching unnecessary for chat queries
- WebSocket: More complex, not needed for request/response pattern

**Implementation Notes**:
- POST to `http://localhost:8000/ask`
- Send `{ question, selected_text?, top_k?, threshold? }`
- Receive `{ answer, sources, has_relevant_context, timing }`
- Handle loading, success, and error states

---

## Decision 4: CORS Configuration

**Decision**: Enable CORS for localhost origins during development

**Rationale**:
- Docusaurus dev server runs on port 3000
- FastAPI backend runs on port 8000
- Cross-origin requests require CORS headers

**Implementation Notes**:
- Use `fastapi.middleware.cors.CORSMiddleware`
- Allow origins: `["http://localhost:3000", "http://127.0.0.1:3000"]`
- Allow methods: `["POST", "OPTIONS"]`
- Allow headers: `["Content-Type"]`

---

## Decision 5: Selected Text Feature

**Decision**: Combine selected text with user question for enhanced retrieval

**Rationale**:
- User story P2 requires passing selected text for context
- Enhances retrieval by providing additional context
- Simple string concatenation in backend query

**Implementation Notes**:
- Frontend captures `window.getSelection().toString()`
- Backend receives `selected_text` in request body
- If present, prepend to query: `f"Context: {selected_text}\n\nQuestion: {question}"`
- Agent uses combined text for retrieval

---

## Decision 6: Error Handling Strategy

**Decision**: Graceful degradation with user-friendly messages

**Rationale**:
- User story P3 requires handling unavailable backend
- SC-004 requires error messages within 5 seconds
- Professional UX for edge cases

**Implementation Notes**:
- Frontend: 10-second timeout on fetch requests
- Backend: Return structured error responses with status codes
- Error messages: "Unable to connect to assistant. Please try again later."
- Loading states prevent double-submission

---

## Dependencies to Add

### Backend (backend/pyproject.toml)

```toml
dependencies = [
    # ... existing
    "fastapi>=0.109.0",
    "uvicorn[standard]>=0.27.0",
]
```

### Frontend (book/package.json)

No new dependencies required. Native Fetch API is sufficient.

---

## API Endpoint Design

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/ask` | POST | Submit question, receive answer |
| `/health` | GET | Health check for frontend |

---

## Security Considerations (Local Development)

- No authentication required per spec
- CORS restricted to localhost only
- No rate limiting per spec
- Input validation via Pydantic models

---

## Performance Considerations

- Agent response time: ~5-15 seconds (LLM + retrieval)
- Frontend timeout: 30 seconds (generous for slow connections)
- Loading indicator required for UX
- No caching (each query is unique)
