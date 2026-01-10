# Tasks: Physical AI & Humanoid Robotics Book

**Input**: Design documents from `/specs/001-physical-ai-robotics-book/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, research.md, quickstart.md

**Tests**: Not explicitly requested in specification. Code sample validation is included as part of content tasks.

**Organization**: Tasks are grouped by user story (reader journey) to enable independent implementation and validation. Each module can be completed and validated before moving to the next.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Book content**: `docs/` at repository root
- **Module content**: `docs/module-{n}-{name}/`
- **Assets**: `docs/assets/diagrams/`, `docs/assets/code-samples/`
- **Config**: Root level for Docusaurus configuration

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize Docusaurus project and book scaffolding

- [X] T001 Initialize Docusaurus 3.x project with `npx create-docusaurus@latest` at repository root
- [X] T002 Configure docusaurus.config.js with book title, GitHub Pages settings, and theme
- [X] T003 [P] Create sidebars.js with module and capstone sidebar configuration
- [X] T004 [P] Create docs/intro.md with book introduction and navigation guide
- [X] T005 [P] Create docs/assets/diagrams/ directory for visual aids
- [X] T006 [P] Create docs/assets/code-samples/ directory for runnable examples
- [X] T007 Create .github/workflows/deploy.yml for GitHub Pages deployment
- [X] T008 Verify initial build passes with `npm run build`

**Checkpoint**: Empty Docusaurus site builds and deploys successfully

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Create all module directories and placeholder files with frontmatter

**⚠️ CRITICAL**: All placeholder files must exist before content writing begins

### Module Directory Structure

- [X] T009 Create docs/module-1-ros2/_category_.json with sidebar position 2
- [X] T010 [P] Create docs/module-1-ros2/index.md with module overview placeholder
- [X] T011 [P] Create docs/module-2-simulation/_category_.json with sidebar position 3
- [X] T012 [P] Create docs/module-2-simulation/index.md with module overview placeholder
- [X] T013 [P] Create docs/module-3-isaac/_category_.json with sidebar position 4
- [X] T014 [P] Create docs/module-3-isaac/index.md with module overview placeholder
- [X] T015 [P] Create docs/module-4-vla/_category_.json with sidebar position 5
- [X] T016 [P] Create docs/module-4-vla/index.md with module overview placeholder
- [X] T017 [P] Create docs/capstone/_category_.json with sidebar position 6
- [X] T018 [P] Create docs/capstone/index.md with capstone overview placeholder

### Module 1 Placeholders

- [X] T019 [P] Create docs/module-1-ros2/1-1-introduction.md with frontmatter
- [X] T020 [P] Create docs/module-1-ros2/1-2-architecture.md with frontmatter
- [X] T021 [P] Create docs/module-1-ros2/1-3-rclpy-basics.md with frontmatter
- [X] T022 [P] Create docs/module-1-ros2/1-4-urdf-fundamentals.md with frontmatter
- [X] T023 [P] Create docs/module-1-ros2/1-5-humanoid-model.md with frontmatter
- [X] T024 [P] Create docs/module-1-ros2/1-6-summary.md with frontmatter

### Module 2 Placeholders

- [X] T025 [P] Create docs/module-2-simulation/2-1-simulation-concepts.md with frontmatter
- [X] T026 [P] Create docs/module-2-simulation/2-2-gazebo-setup.md with frontmatter
- [X] T027 [P] Create docs/module-2-simulation/2-3-physics-simulation.md with frontmatter
- [X] T028 [P] Create docs/module-2-simulation/2-4-sensor-simulation.md with frontmatter
- [X] T029 [P] Create docs/module-2-simulation/2-5-unity-introduction.md with frontmatter
- [X] T030 [P] Create docs/module-2-simulation/2-6-urdf-to-gazebo.md with frontmatter
- [X] T031 [P] Create docs/module-2-simulation/2-7-summary.md with frontmatter

### Module 3 Placeholders

- [X] T032 [P] Create docs/module-3-isaac/3-1-isaac-sim-overview.md with frontmatter
- [X] T033 [P] Create docs/module-3-isaac/3-2-setup-prerequisites.md with frontmatter
- [X] T034 [P] Create docs/module-3-isaac/3-3-synthetic-data.md with frontmatter
- [X] T035 [P] Create docs/module-3-isaac/3-4-isaac-ros-integration.md with frontmatter
- [X] T036 [P] Create docs/module-3-isaac/3-5-vslam.md with frontmatter
- [X] T037 [P] Create docs/module-3-isaac/3-6-nav2-planning.md with frontmatter
- [X] T038 [P] Create docs/module-3-isaac/3-7-summary.md with frontmatter

### Module 4 Placeholders

- [X] T039 [P] Create docs/module-4-vla/4-1-embodied-ai.md with frontmatter
- [X] T040 [P] Create docs/module-4-vla/4-2-speech-recognition.md with frontmatter
- [X] T041 [P] Create docs/module-4-vla/4-3-llm-command-parsing.md with frontmatter
- [X] T042 [P] Create docs/module-4-vla/4-4-ros2-actions.md with frontmatter
- [X] T043 [P] Create docs/module-4-vla/4-5-end-to-end-pipeline.md with frontmatter
- [X] T044 [P] Create docs/module-4-vla/4-6-summary.md with frontmatter

### Capstone Placeholders

- [X] T045 [P] Create docs/capstone/cap-1-project-overview.md with frontmatter
- [X] T046 [P] Create docs/capstone/cap-2-system-architecture.md with frontmatter
- [X] T047 [P] Create docs/capstone/cap-3-voice-input.md with frontmatter
- [X] T048 [P] Create docs/capstone/cap-4-navigation.md with frontmatter
- [X] T049 [P] Create docs/capstone/cap-5-vision.md with frontmatter
- [X] T050 [P] Create docs/capstone/cap-6-manipulation.md with frontmatter
- [X] T051 [P] Create docs/capstone/cap-7-integration.md with frontmatter
- [X] T052 [P] Create docs/capstone/cap-8-conclusion.md with frontmatter

- [X] T053 Verify all placeholder files build successfully with `npm run build`

**Checkpoint**: Foundation ready - all 34 content files exist with valid frontmatter, build passes

---

## Phase 3: User Story 1 - Foundational Learning Path (Priority: P1) 🎯 MVP

**Goal**: Sequential learner can read Module 1 → Module 2 → Module 3 → Module 4 → Capstone and understand each concept before encountering dependencies

**Independent Test**: Reader completes Module 1 and can explain ROS 2 architecture, create nodes, and describe URDF without external references

### Module 1 Content (14,500 words)

- [ ] T054 [US1] Write docs/module-1-ros2/index.md with learning objectives and prerequisites (~500 words)
- [ ] T055 [US1] Write docs/module-1-ros2/1-1-introduction.md explaining ROS 2 as middleware (M1-001) (~2,000 words)
- [ ] T056 [US1] Write docs/module-1-ros2/1-2-architecture.md covering nodes, topics, services (M1-002) (~3,500 words)
- [ ] T057 [US1] Write docs/module-1-ros2/1-3-rclpy-basics.md with Python code samples (M1-003) (~3,000 words)
- [ ] T058 [US1] Write docs/module-1-ros2/1-4-urdf-fundamentals.md explaining robot description (M1-004) (~2,500 words)
- [ ] T059 [US1] Write docs/module-1-ros2/1-5-humanoid-model.md with complete URDF example (M1-005) (~3,000 words)
- [ ] T060 [US1] Write docs/module-1-ros2/1-6-summary.md with key takeaways and What's Next (~500 words)

### Module 1 Assets

- [ ] T061 [P] [US1] Create docs/assets/diagrams/ros2-architecture.md (mermaid) for pub-sub diagram
- [ ] T062 [P] [US1] Create docs/assets/diagrams/ros2-node-graph.md (mermaid) for node relationships
- [ ] T063 [P] [US1] Create docs/assets/code-samples/simple_publisher.py for rclpy example
- [ ] T064 [P] [US1] Create docs/assets/code-samples/simple_subscriber.py for rclpy example
- [ ] T065 [P] [US1] Create docs/assets/code-samples/simple_service.py for service example
- [ ] T066 [P] [US1] Create docs/assets/code-samples/humanoid.urdf for complete humanoid model

- [ ] T067 [US1] Verify Module 1 content meets M1-001 through M1-005 requirements
- [ ] T068 [US1] Verify Module 1 code samples are syntactically valid

**Checkpoint**: Module 1 complete - reader can understand ROS 2 fundamentals independently

---

## Phase 4: User Story 1 Continued - Module 2 Content

**Goal**: Reader understands simulation and can load URDF into Gazebo

### Module 2 Content (16,000 words)

- [ ] T069 [US1] Write docs/module-2-simulation/index.md with learning objectives (~500 words)
- [ ] T070 [US1] Write docs/module-2-simulation/2-1-simulation-concepts.md (M2-001) (~2,000 words)
- [ ] T071 [US1] Write docs/module-2-simulation/2-2-gazebo-setup.md with install instructions (~2,500 words)
- [ ] T072 [US1] Write docs/module-2-simulation/2-3-physics-simulation.md (M2-002) (~3,000 words)
- [ ] T073 [US1] Write docs/module-2-simulation/2-4-sensor-simulation.md (M2-004) (~3,500 words)
- [ ] T074 [US1] Write docs/module-2-simulation/2-5-unity-introduction.md (M2-003) (~2,500 words)
- [ ] T075 [US1] Write docs/module-2-simulation/2-6-urdf-to-gazebo.md (M2-005) with cross-ref to Module 1 (~2,000 words)
- [ ] T076 [US1] Write docs/module-2-simulation/2-7-summary.md with What's Next to Module 3 (~500 words)

### Module 2 Assets

- [ ] T077 [P] [US1] Create docs/assets/diagrams/simulation-architecture.md (mermaid)
- [ ] T078 [P] [US1] Create docs/assets/diagrams/sensor-types.md (mermaid)
- [ ] T079 [P] [US1] Create docs/assets/code-samples/gazebo_launch.py for launch file
- [ ] T080 [P] [US1] Create docs/assets/code-samples/lidar_config.yaml for sensor config
- [ ] T081 [P] [US1] Create docs/assets/code-samples/depth_camera_config.yaml for sensor config

- [ ] T082 [US1] Verify Module 2 content meets M2-001 through M2-005 requirements
- [ ] T083 [US1] Add cross-reference from 2-6 to Module 1 (1-5) for URDF dependency

**Checkpoint**: Module 2 complete - reader can simulate humanoid in Gazebo

---

## Phase 5: User Story 1 Continued - Module 3 Content

**Goal**: Reader understands Isaac Sim and Nav2 for AI-powered robotics

### Module 3 Content (18,000 words)

- [ ] T084 [US1] Write docs/module-3-isaac/index.md with learning objectives and GPU requirements (~500 words)
- [ ] T085 [US1] Write docs/module-3-isaac/3-1-isaac-sim-overview.md (M3-001) (~2,500 words)
- [ ] T086 [US1] Write docs/module-3-isaac/3-2-setup-prerequisites.md (M3-005) with hardware checklist (~2,000 words)
- [ ] T087 [US1] Write docs/module-3-isaac/3-3-synthetic-data.md (M3-002) (~3,500 words)
- [ ] T088 [US1] Write docs/module-3-isaac/3-4-isaac-ros-integration.md (M3-003) (~3,000 words)
- [ ] T089 [US1] Write docs/module-3-isaac/3-5-vslam.md explaining hardware-accelerated VSLAM (~3,000 words)
- [ ] T090 [US1] Write docs/module-3-isaac/3-6-nav2-planning.md (M3-004) with Nav2 config (~3,500 words)
- [ ] T091 [US1] Write docs/module-3-isaac/3-7-summary.md with What's Next to Module 4 (~500 words)

### Module 3 Assets

- [ ] T092 [P] [US1] Create docs/assets/diagrams/isaac-architecture.md (mermaid)
- [ ] T093 [P] [US1] Create docs/assets/diagrams/nav2-stack.md (mermaid)
- [ ] T094 [P] [US1] Create docs/assets/code-samples/isaac_ros_launch.py
- [ ] T095 [P] [US1] Create docs/assets/code-samples/nav2_params.yaml for navigation config
- [ ] T096 [P] [US1] Create docs/assets/code-samples/synthetic_data_script.py

- [ ] T097 [US1] Verify Module 3 content meets M3-001 through M3-005 requirements
- [ ] T098 [US1] Add cross-references to Module 1 (ROS 2) and Module 2 (simulation)

**Checkpoint**: Module 3 complete - reader understands Isaac Sim and Nav2

---

## Phase 6: User Story 1 Continued - Module 4 Content

**Goal**: Reader understands Vision-Language-Action systems

### Module 4 Content (14,500 words)

- [ ] T099 [US1] Write docs/module-4-vla/index.md with learning objectives (~500 words)
- [ ] T100 [US1] Write docs/module-4-vla/4-1-embodied-ai.md (M4-001) (~2,500 words)
- [ ] T101 [US1] Write docs/module-4-vla/4-2-speech-recognition.md (M4-002) with Whisper integration (~2,500 words)
- [ ] T102 [US1] Write docs/module-4-vla/4-3-llm-command-parsing.md (M4-003) (~3,000 words)
- [ ] T103 [US1] Write docs/module-4-vla/4-4-ros2-actions.md with action server examples (~2,500 words)
- [ ] T104 [US1] Write docs/module-4-vla/4-5-end-to-end-pipeline.md (M4-004) (~3,500 words)
- [ ] T105 [US1] Write docs/module-4-vla/4-6-summary.md with What's Next to Capstone (~500 words)

### Module 4 Assets

- [ ] T106 [P] [US1] Create docs/assets/diagrams/vla-pipeline.md (mermaid)
- [ ] T107 [P] [US1] Create docs/assets/diagrams/voice-to-action-flow.md (mermaid)
- [ ] T108 [P] [US1] Create docs/assets/code-samples/whisper_node.py for speech recognition
- [ ] T109 [P] [US1] Create docs/assets/code-samples/llm_parser.py for command parsing
- [ ] T110 [P] [US1] Create docs/assets/code-samples/action_server.py for ROS 2 actions

- [ ] T111 [US1] Verify Module 4 content meets M4-001 through M4-004 requirements
- [ ] T112 [US1] Add cross-references to Module 1 (rclpy) for action servers

**Checkpoint**: Module 4 complete - reader understands VLA systems

---

## Phase 7: User Story 3 - Capstone Project Completion (Priority: P3)

**Goal**: Reader synthesizes all learning into working autonomous humanoid

**Independent Test**: Reader completes capstone using only book content, resulting in simulated humanoid responding to voice commands

### Capstone Content (17,000 words)

- [ ] T113 [US3] Write docs/capstone/index.md with project scope and prerequisites (~500 words)
- [ ] T114 [US3] Write docs/capstone/cap-1-project-overview.md (CAP-001) (~1,500 words)
- [ ] T115 [US3] Write docs/capstone/cap-2-system-architecture.md with full system design (~2,000 words)
- [ ] T116 [US3] Write docs/capstone/cap-3-voice-input.md integrating Whisper + LLM (~2,000 words)
- [ ] T117 [US3] Write docs/capstone/cap-4-navigation.md (CAP-002, CAP-003) with Nav2 and obstacles (~2,500 words)
- [ ] T118 [US3] Write docs/capstone/cap-5-vision.md (CAP-004) with object detection (~2,500 words)
- [ ] T119 [US3] Write docs/capstone/cap-6-manipulation.md (CAP-005) with grasping (~2,500 words)
- [ ] T120 [US3] Write docs/capstone/cap-7-integration.md (CAP-006) with step-by-step instructions (~3,000 words)
- [ ] T121 [US3] Write docs/capstone/cap-8-conclusion.md with next steps and extensions (~1,000 words)

### Capstone Assets

- [ ] T122 [P] [US3] Create docs/assets/diagrams/capstone-architecture.md (mermaid)
- [ ] T123 [P] [US3] Create docs/assets/diagrams/integration-flow.md (mermaid)
- [ ] T124 [P] [US3] Create docs/assets/code-samples/capstone_main.py for main entry point
- [ ] T125 [P] [US3] Create docs/assets/code-samples/capstone_launch.py for launch file
- [ ] T126 [P] [US3] Create docs/assets/code-samples/object_detector.py for vision
- [ ] T127 [P] [US3] Create docs/assets/code-samples/gripper_controller.py for manipulation

- [ ] T128 [US3] Verify Capstone meets CAP-001 through CAP-006 requirements
- [ ] T129 [US3] Add cross-references to all modules from capstone chapters
- [ ] T130 [US3] Verify capstone can be completed in under 8 hours (SC-006)

**Checkpoint**: Capstone complete - full autonomous humanoid project works end-to-end

---

## Phase 8: User Story 2 - Module-Based Reference (Priority: P2)

**Goal**: Each module works as standalone reference with clear cross-references

**Independent Test**: Developer can read only Module 3 and understand Isaac Sim with pointers to prerequisites

### Cross-Reference Enhancement

- [ ] T131 [US2] Add "Prerequisites" callout box to docs/module-2-simulation/index.md linking to Module 1
- [ ] T132 [US2] Add "Prerequisites" callout box to docs/module-3-isaac/index.md linking to Modules 1 and 2
- [ ] T133 [US2] Add "Prerequisites" callout box to docs/module-4-vla/index.md linking to Module 1
- [ ] T134 [US2] Add "Prerequisites" callout box to docs/capstone/index.md linking to all modules

### Standalone Module Validation

- [ ] T135 [US2] Verify Module 2 explains simulation concepts without assuming Module 1 read
- [ ] T136 [US2] Verify Module 3 explains Isaac without assuming Modules 1-2 read
- [ ] T137 [US2] Verify Module 4 explains VLA without assuming Modules 1-3 read
- [ ] T138 [US2] Add glossary terms defined on first use in each module

**Checkpoint**: Each module readable as standalone reference

---

## Phase 9: User Story 4 - Hands-On Simulation Practice (Priority: P4)

**Goal**: Setup instructions work for Gazebo and Isaac Sim environments

**Independent Test**: Reader follows setup instructions and runs examples without errors

### Environment Setup Validation

- [ ] T139 [US4] Verify docs/module-2-simulation/2-2-gazebo-setup.md produces working environment
- [ ] T140 [US4] Verify docs/module-3-isaac/3-2-setup-prerequisites.md produces working environment
- [ ] T141 [US4] Add troubleshooting section to Module 2 setup chapter
- [ ] T142 [US4] Add troubleshooting section to Module 3 setup chapter
- [ ] T143 [US4] Test all code samples execute without errors (SC-008)

**Checkpoint**: All simulation setups verified working

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Final quality pass and deployment

### Content Quality

- [ ] T144 [P] Run markdown linting on all docs/ files
- [ ] T145 [P] Check Flesch-Kincaid readability score ≤ Grade 12 (SC-003)
- [ ] T146 [P] Verify word count is between 40,000-80,000 words (SC-004)
- [ ] T147 [P] Verify each module has ≥3 code samples (SC-005)
- [ ] T148 Review all internal cross-references resolve (SC-002)

### Build Validation

- [ ] T149 Run final `npm run build` with zero errors (SC-001)
- [ ] T150 Verify all images and assets load correctly
- [ ] T151 Test sidebar navigation works for all modules
- [ ] T152 Verify search functionality indexes all content

### Deployment

- [ ] T153 Deploy to GitHub Pages via workflow
- [ ] T154 Verify deployed site loads correctly
- [ ] T155 Create git tag v1.0.0 for release

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 - BLOCKS all content writing
- **US1 Phases 3-6**: Depends on Phase 2, sequential (Module 1 → 2 → 3 → 4)
- **US3 Phase 7**: Depends on Phases 3-6 (all modules complete)
- **US2 Phase 8**: Depends on Phases 3-6 (cross-references need content)
- **US4 Phase 9**: Depends on Phases 4, 5 (setup chapters exist)
- **Polish (Phase 10)**: Depends on all content phases complete

### User Story Dependencies

```
Phase 1 (Setup)
    │
    ▼
Phase 2 (Foundational)
    │
    ├──────────────────────────────────────┐
    │                                      │
    ▼                                      ▼
Phase 3-6 (US1: Module 1→2→3→4)      Phase 9 (US4: partial)
    │                                      │
    ├──────────────────────────────────────┤
    │                                      │
    ▼                                      ▼
Phase 7 (US3: Capstone)              Phase 8 (US2: Cross-refs)
    │                                      │
    └──────────────────────────────────────┘
                     │
                     ▼
              Phase 10 (Polish)
```

### Parallel Opportunities

- **Phase 2**: All placeholder tasks T009-T052 can run in parallel
- **Within Modules**: Diagram and code sample tasks marked [P] can run in parallel with content
- **Phase 8-9**: Can run in parallel after US1 content complete
- **Phase 10**: Linting tasks T144-T147 can run in parallel

---

## Parallel Example: Module 1 Content

```bash
# Sequential content writing (must be in order for flow):
Task: T054 Write index.md
Task: T055 Write 1-1-introduction.md
Task: T056 Write 1-2-architecture.md
# ... etc

# Parallel asset creation (can run alongside or after content):
Task: T061 Create ros2-architecture diagram
Task: T062 Create ros2-node-graph diagram
Task: T063 Create simple_publisher.py
Task: T064 Create simple_subscriber.py
Task: T065 Create simple_service.py
Task: T066 Create humanoid.urdf
```

---

## Implementation Strategy

### MVP First (User Story 1 - Modules Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational placeholders
3. Complete Phase 3: Module 1 (ROS 2)
4. **STOP and VALIDATE**: Build passes, Module 1 content readable
5. Deploy partial book for early feedback

### Incremental Delivery

1. Setup + Foundational → Empty book deployed
2. Add Module 1 → Test → Deploy (readers can learn ROS 2)
3. Add Module 2 → Test → Deploy (readers can simulate)
4. Add Module 3 → Test → Deploy (readers can use Isaac)
5. Add Module 4 → Test → Deploy (readers can build VLA)
6. Add Capstone → Test → Deploy (readers can complete project)
7. Polish + Cross-refs → Final release v1.0.0

### Suggested MVP Scope

**MVP = Phase 1 + Phase 2 + Phase 3 (Module 1 only)**

This delivers:
- Working Docusaurus site
- Complete Module 1: ROS 2 (14,500 words)
- 6 code samples
- Immediate value for readers learning ROS 2

---

## Task Summary

| Phase | User Story | Tasks | Parallel Tasks |
|-------|------------|-------|----------------|
| 1 | Setup | 8 | 4 |
| 2 | Foundational | 45 | 43 |
| 3 | US1 - Module 1 | 15 | 6 |
| 4 | US1 - Module 2 | 15 | 5 |
| 5 | US1 - Module 3 | 15 | 5 |
| 6 | US1 - Module 4 | 14 | 5 |
| 7 | US3 - Capstone | 18 | 6 |
| 8 | US2 - Cross-refs | 8 | 0 |
| 9 | US4 - Setup validation | 5 | 0 |
| 10 | Polish | 12 | 4 |
| **Total** | | **155** | **78** |

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks
- [US#] label maps task to specific user story for traceability
- Each module should be independently completable and testable
- Commit after each chapter or logical group of tasks
- Stop at any checkpoint to validate and deploy partial progress
- Word count targets per chapter are guidelines, adjust for content quality

---

**Tasks Version**: 1.0.0
**Generated**: 2026-01-09
**Total Tasks**: 155
**Parallel Opportunities**: 78 tasks (50%)
