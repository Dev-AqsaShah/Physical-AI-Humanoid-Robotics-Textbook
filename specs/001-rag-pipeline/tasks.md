# Tasks: RAG Pipeline – Content Ingestion, Embeddings, and Vector Storage

**Input**: Design documents from `/specs/001-rag-pipeline/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Not requested - manual verification via sample queries per plan.md

**Organization**: Tasks grouped by user story for independent implementation.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: User story mapping (US1, US2, US3)
- All code in `backend/main.py` per user specification

---

## Phase 1: Setup

**Purpose**: Initialize Python project with uv

- [x] T001 Create `backend/` directory at repository root
- [x] T002 Initialize Python project with `uv init` in backend/
- [x] T003 Add dependencies: cohere, qdrant-client, python-dotenv, rich via `uv add`
- [x] T004 [P] Create `backend/.env.example` with COHERE_API_KEY, QDRANT_URL, QDRANT_API_KEY
- [x] T005 [P] Add `backend/.env` to `.gitignore`

---

## Phase 2: Foundational

**Purpose**: Core functions in main.py that all user stories depend on

- [x] T006 Create `backend/main.py` with imports and environment loading
- [x] T007 Add `discover_markdown_files()` function - glob for `**/docs/**/*.md`
- [x] T008 Add `parse_frontmatter()` function - extract title, sidebar_position from YAML
- [x] T009 Add `extract_content()` function - strip frontmatter, return body text

**Checkpoint**: File discovery and parsing ready

---

## Phase 3: User Story 1 - Content Ingestion (Priority: P1)

**Goal**: Ingest all book content into Qdrant with correct metadata

**Independent Test**: Run pipeline, verify all 40 pages processed with vectors in Qdrant

### Implementation

- [x] T010 [US1] Add `chunk_content()` function - split on H2/H3 headers, 500-1500 chars
- [x] T011 [US1] Add `generate_chunk_id()` function - deterministic UUID from path+index
- [x] T012 [US1] Add `create_cohere_client()` function - initialize with API key
- [x] T013 [US1] Add `generate_embeddings()` function - batch Cohere API calls with retry
- [x] T014 [US1] Add `create_qdrant_client()` function - connect to Qdrant Cloud
- [x] T015 [US1] Add `ensure_collection()` function - create collection if not exists (1024 dims, Cosine)
- [x] T016 [US1] Add `store_vectors()` function - upsert points with payload metadata
- [x] T017 [US1] Add `build_source_url()` function - derive web URL from file path
- [x] T018 [US1] Add `process_page()` function - orchestrate extract→chunk→embed→store
- [x] T019 [US1] Add progress logging with rich console (page count, chunk count)
- [x] T020 [US1] Add `main()` function - loop through all pages, call process_page()

**Checkpoint**: Full ingestion pipeline functional

---

## Phase 4: User Story 2 - Idempotent Re-ingestion (Priority: P2)

**Goal**: Safe re-runs without duplicates

**Independent Test**: Run pipeline twice, verify zero duplicate vectors

### Implementation

- [x] T021 [US2] Add `compute_content_hash()` function - MD5 of chunk content
- [x] T022 [US2] Update `generate_chunk_id()` to use deterministic hash for point ID
- [x] T023 [US2] Update `store_vectors()` to use upsert (overwrites existing by ID)
- [x] T024 [US2] Add duplicate detection logging (log when overwriting existing vector)

**Checkpoint**: Idempotent ingestion verified

---

## Phase 5: User Story 3 - Verification (Priority: P3)

**Goal**: Confirm vector store is queryable with relevant results

**Independent Test**: Execute sample query, verify top-5 results contain related content

### Implementation

- [x] T025 [US3] Add `verify_ingestion()` function - query vector count
- [x] T026 [US3] Add `run_sample_query()` function - search "What is ROS 2?"
- [x] T027 [US3] Add result display - show top-5 results with scores and metadata
- [x] T028 [US3] Add verification pass/fail check - at least 3 relevant results in top-5
- [x] T029 [US3] Call verification after main ingestion completes

**Checkpoint**: Full pipeline with verification complete

---

## Phase 6: Polish

**Purpose**: Error handling and edge cases

- [x] T030 [P] Add graceful error handling for missing .env vars (exit code 2)
- [x] T031 [P] Add connection error handling for Qdrant/Cohere (exit code 3)
- [x] T032 [P] Add exponential backoff for Cohere rate limits (max 3 retries)
- [x] T033 [P] Add empty content skip (log warning, continue)
- [x] T034 Add final summary output (pages processed, chunks created, time elapsed)
- [x] T035 Add CLI entry point with `if __name__ == "__main__"`

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup) → Phase 2 (Foundational) → Phase 3 (US1) → Phase 4 (US2) → Phase 5 (US3) → Phase 6 (Polish)
```

### User Story Dependencies

| Story | Depends On | Can Parallel With |
|-------|------------|-------------------|
| US1 | Phase 2 | - |
| US2 | US1 (uses same functions) | - |
| US3 | US1 (needs vectors stored) | - |

### Parallel Opportunities

**Phase 1**: T004, T005 can run in parallel
**Phase 6**: T030, T031, T032, T033 can run in parallel

---

## Summary

| Phase | Tasks | Story | Status |
|-------|-------|-------|--------|
| Setup | 5 | - | ✅ Complete |
| Foundational | 4 | - | ✅ Complete |
| User Story 1 | 11 | US1 | ✅ Complete |
| User Story 2 | 4 | US2 | ✅ Complete |
| User Story 3 | 5 | US3 | ✅ Complete |
| Polish | 6 | - | ✅ Complete |
| **Total** | **35** | | **✅ All Complete** |

### MVP Scope

Complete Phase 1-3 for minimum viable pipeline (US1 only = full ingestion).

### All Code Location

Single file: `backend/main.py` (per user specification)
