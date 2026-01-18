# Tasks: RAG Pipeline – Agent Construction with Retrieval

**Input**: Design documents from `/specs/003-rag-agent/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/

**Organization**: Tasks grouped by user story for independent implementation.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)

---

## Phase 1: Setup

**Purpose**: Project initialization and dependency installation

- [x] T001 Add `openai-agents>=0.6.6` to requirements.txt
- [x] T002 Add `OPENAI_API_KEY` placeholder to .env.example (if exists) or document in quickstart
- [x] T003 Create agent.py with module docstring, imports, and constants in project root

---

## Phase 2: Foundational

**Purpose**: Core infrastructure required by all user stories

- [x] T004 Define data classes (AgentResponse, SourceCitation) in agent.py
- [x] T005 Implement `format_context_for_agent()` to convert ResultSet to LLM-ready text in agent.py
- [x] T006 Implement `@function_tool` wrapper `retrieve_book_context()` around semantic_search in agent.py
- [x] T007 Define agent with system instructions using OpenAI Agents SDK in agent.py
- [x] T008 Implement `ask()` async function as programmatic entry point in agent.py

**Checkpoint**: Core agent infrastructure ready

---

## Phase 3: User Story 1 - Answer Book Questions (Priority: P1) MVP

**Goal**: Agent answers questions using retrieved book content

**Independent Test**: `python agent.py "What is ROS 2?"` returns grounded answer

### Implementation

- [x] T009 [US1] Implement response generation flow: query → retrieve → generate in agent.py
- [x] T010 [US1] Add relevance threshold check (0.5) to filter low-quality context in agent.py
- [x] T011 [US1] Implement `format_response()` to display answer with timing in agent.py
- [x] T012 [US1] Add CLI argument parsing with argparse (query, --top-k, --threshold) in agent.py
- [x] T013 [US1] Implement main() entry point for basic query mode in agent.py

**Checkpoint**: Basic Q&A works end-to-end

---

## Phase 4: User Story 2 - Source Citations (Priority: P2)

**Goal**: Responses include traceable source citations

**Independent Test**: Response shows chapter, section, URL for each source

### Implementation

- [x] T014 [US2] Extract SourceCitation list from ResultSet in format_context_for_agent() in agent.py
- [x] T015 [US2] Include citations in AgentResponse and format_response() output in agent.py
- [x] T016 [US2] Add --json flag for structured output with sources in agent.py

**Checkpoint**: All responses include valid citations

---

## Phase 5: User Story 3 - Handle Unanswerable Questions (Priority: P3)

**Goal**: Agent declines or shows uncertainty when context insufficient

**Independent Test**: `python agent.py "What is quantum computing?"` returns uncertainty message

### Implementation

- [x] T017 [US3] Implement low-relevance detection when all scores < threshold in agent.py
- [x] T018 [US3] Add "no relevant context" response path with helpful message in agent.py
- [x] T019 [US3] Update system prompt to instruct declining out-of-scope questions in agent.py

**Checkpoint**: Agent gracefully handles out-of-scope queries

---

## Phase 6: Polish & Validation

**Purpose**: Error handling, logging, and validation suite

- [x] T020 [P] Add error handling for Qdrant/Cohere/OpenAI failures in agent.py
- [x] T021 [P] Add logging for queries, retrieval results, and responses in agent.py
- [x] T022 Define TEST_QUERIES list (in-scope and out-of-scope) in agent.py
- [x] T023 Implement `run_validation()` function with pass/fail logic in agent.py
- [x] T024 Add --test flag to run validation suite in agent.py
- [x] T025 Add --verbose flag for detailed retrieval info in agent.py
- [x] T026 Implement `ask_sync()` wrapper for non-async usage in agent.py
- [x] T027 Verify end-to-end with quickstart.md examples

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Setup
- **User Stories (Phase 3-5)**: Depend on Foundational; can run sequentially P1→P2→P3
- **Polish (Phase 6)**: Depends on all user stories

### Within Phases

- T001-T003: Parallel (different concerns)
- T004-T008: Sequential (each builds on previous)
- User story tasks: Sequential within story, stories sequential by priority
- T020-T021: Parallel (different concerns)

---

## Parallel Example: Setup Phase

```bash
# All setup tasks can run in parallel:
Task: "Add openai-agents to requirements.txt"
Task: "Add OPENAI_API_KEY to .env.example"
Task: "Create agent.py skeleton"
```

---

## Implementation Strategy

### MVP First (User Story 1)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. **VALIDATE**: `python agent.py "What is ROS 2?"`

### Incremental Delivery

1. Setup + Foundational → Core ready
2. User Story 1 → Basic Q&A works (MVP)
3. User Story 2 → Citations added
4. User Story 3 → Handles edge cases
5. Polish → Production-ready

---

## Summary

| Phase | Tasks | Parallel Opportunities |
|-------|-------|------------------------|
| Setup | 3 | All parallel |
| Foundational | 5 | Sequential |
| US1 (P1) | 5 | Sequential |
| US2 (P2) | 3 | Sequential |
| US3 (P3) | 3 | Sequential |
| Polish | 8 | T020-T021 parallel |
| **Total** | **27** | |

**MVP Scope**: Phases 1-3 (13 tasks) for basic working agent
