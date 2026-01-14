# Tasks: RAG Pipeline – Retrieval & Validation

**Input**: Design documents from `/specs/002-rag-retrieval/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: User story label (US1, US2, US3)
- All code in `backend/retrieve.py`

---

## Phase 1: Setup

- [x] T001 Create `backend/retrieve.py` with module docstring and imports
- [x] T002 Define constants (COLLECTION_NAME, EMBEDDING_MODEL) matching main.py

---

## Phase 2: Foundational

- [x] T003 [P] Implement `create_cohere_client()` (reuse pattern from main.py)
- [x] T004 [P] Implement `create_qdrant_client()` (reuse pattern from main.py)
- [x] T005 Implement `check_collection_exists()` returning bool (read-only, no create)
- [x] T006 Define `SearchResult` and `ResultSet` dataclasses per data-model.md

**Checkpoint**: Client initialization and data structures ready

---

## Phase 3: User Story 1 – Semantic Search (P1) 🎯 MVP

**Goal**: Execute semantic search queries and return relevant chunks

**Independent Test**: `python retrieve.py "What is ROS 2?"` returns top-5 results with scores

### Implementation

- [x] T007 [US1] Implement `generate_query_embedding(query: str)` using Cohere
- [x] T008 [US1] Implement `semantic_search(query, top_k, chapter_filter)` using query_points()
- [x] T009 [US1] Implement `format_results(results)` for console output
- [x] T010 [US1] Add CLI argument parsing (query, --top-k, --chapter, --json)
- [x] T011 [US1] Implement `main()` entry point with basic search flow

**Checkpoint**: Basic search works: `python retrieve.py "query"`

---

## Phase 4: User Story 2 – Metadata Verification (P2)

**Goal**: Verify all metadata fields are present and valid

**Independent Test**: `python retrieve.py --validate` checks metadata completeness

### Implementation

- [x] T012 [US2] Define `ValidationResult` and `ValidationReport` dataclasses
- [x] T013 [US2] Implement `validate_metadata(result)` checking required fields
- [x] T014 [US2] Implement `validate_content_integrity(result)` checking content_hash
- [x] T015 [US2] Add `--validate` CLI flag calling validation suite

**Checkpoint**: Metadata validation reports completeness percentage

---

## Phase 5: User Story 3 – Performance Validation (P3)

**Goal**: Measure and report query latency

**Independent Test**: `python retrieve.py --validate` reports timing metrics

### Implementation

- [x] T016 [US3] Add timing to `semantic_search()` using time.perf_counter()
- [x] T017 [US3] Implement `run_validation_suite()` with 5 test queries
- [x] T018 [US3] Implement `display_validation_report()` with pass/fail summary
- [x] T019 [US3] Add latency threshold checks (<2s per query, <1s average)

**Checkpoint**: Full validation suite runs with timing metrics

---

## Phase 6: Polish

- [x] T020 [P] Add `--stats` flag to show collection info
- [x] T021 [P] Add JSON output format for `--json` flag
- [x] T022 Handle edge cases (empty query, no results, connection errors)
- [x] T023 Final verification: run quickstart.md test scenarios

---

## Dependencies

```
Phase 1 (Setup) → Phase 2 (Foundational) → Phase 3 (US1/MVP)
                                        → Phase 4 (US2) [can parallel with US3]
                                        → Phase 5 (US3) [can parallel with US2]
                                        → Phase 6 (Polish)
```

**User Story Independence**:
- US1: Core search - no dependencies on other stories
- US2: Metadata validation - depends on US1 search results
- US3: Performance timing - depends on US1 search execution

---

## Parallel Execution Example

```bash
# Phase 2 - run in parallel:
T003: create_cohere_client()
T004: create_qdrant_client()

# Phase 4 & 5 - can run in parallel after US1:
T012-T015 (US2 metadata)
T016-T019 (US3 timing)
```

---

## Summary

| Phase | Tasks | Parallel |
|-------|-------|----------|
| Setup | 2 | 0 |
| Foundational | 4 | 2 |
| US1 (MVP) | 5 | 0 |
| US2 | 4 | 0 |
| US3 | 4 | 0 |
| Polish | 4 | 2 |
| **Total** | **23** | **4** |

**MVP Scope**: Phases 1-3 (T001-T011) = 11 tasks
