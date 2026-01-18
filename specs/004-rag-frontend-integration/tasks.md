# Tasks: RAG Pipeline – Backend and Frontend Integration

**Input**: Design documents from `/specs/004-rag-frontend-integration/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/

**Organization**: Tasks grouped by user story for independent implementation.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)

---

## Phase 1: Setup

**Purpose**: Project initialization and dependency installation

- [x] T001 Add `fastapi>=0.109.0` and `uvicorn[standard]>=0.27.0` to backend/pyproject.toml
- [x] T002 [P] Create app.py skeleton with imports and FastAPI app instance in project root
- [x] T003 [P] Create book/src/components/Chatbot/ directory structure

---

## Phase 2: Foundational

**Purpose**: Core infrastructure required by all user stories

- [x] T004 Implement Pydantic models (QueryRequest, QueryResponse, ErrorResponse) in app.py
- [x] T005 Add CORS middleware for localhost origins in app.py
- [x] T006 Implement /health endpoint in app.py
- [x] T007 Create book/src/theme/Root.js to wrap app with chatbot component

**Checkpoint**: Backend runs, frontend loads with chatbot wrapper

---

## Phase 3: User Story 1 - Ask a Question (Priority: P1) MVP

**Goal**: User types question, receives grounded answer with citations

**Independent Test**: `curl -X POST http://localhost:8000/ask -d '{"question":"What is ROS 2?"}'`

### Implementation

- [x] T008 [US1] Implement POST /ask endpoint with agent.ask() integration in app.py
- [x] T009 [US1] Create Chatbot/index.js with input field, submit button, response display in book/src/components/Chatbot/index.js
- [x] T010 [US1] Add fetch call to backend /ask endpoint in Chatbot component
- [x] T011 [US1] Create Chatbot/styles.module.css with floating chat UI styles in book/src/components/Chatbot/styles.module.css
- [x] T012 [US1] Display source citations in response in Chatbot component
- [x] T013 [US1] Add loading spinner while awaiting response in Chatbot component

**Checkpoint**: Basic Q&A works end-to-end

---

## Phase 4: User Story 2 - Selected Text Context (Priority: P2)

**Goal**: User selects text, asks about it with enhanced context

**Independent Test**: Select text in book, click chat, verify selected_text in request

### Implementation

- [x] T014 [US2] Add selected_text support to /ask endpoint in app.py
- [x] T015 [US2] Capture window.getSelection() in Chatbot component
- [x] T016 [US2] Add "Ask about selection" button when text selected in Chatbot component
- [x] T017 [US2] Send selected_text with query and display context indicator

**Checkpoint**: Selected text queries work

---

## Phase 5: User Story 3 - Error Handling (Priority: P3)

**Goal**: Graceful error handling when backend unavailable

**Independent Test**: Stop backend, submit question, verify error message

### Implementation

- [x] T018 [US3] Add try/catch with timeout (30s) to fetch call in Chatbot component
- [x] T019 [US3] Display user-friendly error message on failure in Chatbot component
- [x] T020 [US3] Add retry button after error in Chatbot component
- [x] T021 [US3] Handle backend error responses (4xx/5xx) gracefully

**Checkpoint**: Errors handled gracefully

---

## Phase 6: Polish

**Purpose**: Input validation and edge cases

- [x] T022 [P] Add input validation (empty, max length) in Chatbot component
- [x] T023 [P] Add request validation in /ask endpoint for empty queries
- [x] T024 Verify end-to-end with quickstart.md examples

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Setup
- **User Stories (Phase 3-5)**: Depend on Foundational; can run sequentially P1→P2→P3
- **Polish (Phase 6)**: Depends on all user stories

### Within Phases

- T001-T003: Parallel (different files)
- T004-T007: Sequential (build on each other)
- T009-T013: Sequential within frontend
- T022-T023: Parallel (different concerns)

---

## Summary

| Phase | Tasks | Parallel Opportunities |
|-------|-------|------------------------|
| Setup | 3 | T002, T003 parallel |
| Foundational | 4 | Sequential |
| US1 (P1) | 6 | Sequential |
| US2 (P2) | 4 | Sequential |
| US3 (P3) | 4 | Sequential |
| Polish | 3 | T022, T023 parallel |
| **Total** | **24** | |

**MVP Scope**: Phases 1-3 (13 tasks) for basic working Q&A

**Implementation Status**: All 24 tasks completed.
