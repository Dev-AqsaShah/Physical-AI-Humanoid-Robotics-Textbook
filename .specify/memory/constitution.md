<!--
=============================================================================
SYNC IMPACT REPORT
=============================================================================
Version change: 0.0.0 → 1.0.0 (MAJOR - Initial constitution adoption)

Modified principles: N/A (initial version)

Added sections:
- Core Principles (6 principles defined)
- Content Standards section
- Development Workflow section
- Governance section

Removed sections: N/A (initial version)

Templates requiring updates:
- .specify/templates/plan-template.md: ✅ Compatible (Constitution Check section exists)
- .specify/templates/spec-template.md: ✅ Compatible (Requirements section aligns)
- .specify/templates/tasks-template.md: ✅ Compatible (Phase structure supports content workflow)

Follow-up TODOs: None
=============================================================================
-->

# AI/Spec-Driven Book Creation Constitution

## Core Principles

### I. Spec-First Writing

All content MUST follow the approved specification before any writing begins. No chapter, section, or paragraph may be authored without a corresponding spec entry that defines its scope, purpose, and acceptance criteria.

**Non-negotiables:**
- Every content piece traces to an approved spec item
- Deviations from spec require explicit approval and spec amendment
- Assumptions or missing requirements MUST be explicitly stated in the spec before implementation

**Rationale:** Spec-first ensures alignment between stakeholder intent and delivered content, preventing scope creep and enabling traceability.

### II. Clarity for Readers

All technical explanations MUST be written for beginner to intermediate technical readers. Complex concepts require progressive disclosure—introduce simply, then add depth.

**Non-negotiables:**
- Avoid jargon without definition on first use
- Use concrete examples over abstract descriptions
- Structure content with clear headings, bullet points, and visual breaks
- Each section MUST be comprehensible without requiring external references

**Rationale:** The target audience spans skill levels; clarity ensures accessibility without sacrificing technical accuracy.

### III. Accuracy and Correctness

All technical content MUST be verifiable and factually correct. No invented tools, APIs, commands, features, or behaviors are permitted.

**Non-negotiables:**
- Every code sample MUST be syntactically valid and runnable
- Command-line instructions MUST produce the described output
- API references MUST match actual documented behavior
- Version numbers, URLs, and tool names MUST be current and accurate
- No hallucinated or unsupported information

**Rationale:** Technical readers rely on documentation to work correctly the first time; inaccuracies destroy trust and waste reader time.

### IV. Modular Documentation

Content MUST be structured for static site generation and independent navigation. Each chapter and section MUST function as a standalone unit suitable for Docusaurus.

**Non-negotiables:**
- Clear separation of chapters and sections for GitHub version control
- Each markdown file MUST be self-contained with proper frontmatter
- Cross-references use relative links that resolve in Docusaurus
- No circular dependencies between sections
- Structure MUST support sidebar navigation and search

**Rationale:** Docusaurus and GitHub Pages require modular content for proper rendering, versioning, and navigation.

### V. Professional Technical Writing

All content MUST meet professional documentation standards: simple, clear English with consistent terminology and formatting across all chapters.

**Non-negotiables:**
- Writing style: Simple, clear English suitable for international readers
- Consistent terminology—define terms once, use consistently throughout
- Consistent formatting patterns for code blocks, notes, warnings, and tips
- No casual language, slang, or unnecessary humor
- Active voice preferred; passive voice only when appropriate

**Rationale:** Professional writing ensures the book is taken seriously as a reference and remains accessible to non-native English speakers.

### VI. Docusaurus and GitHub Pages Compatibility

All output MUST be valid Markdown (.md/.mdx) that builds successfully with Docusaurus and deploys cleanly to GitHub Pages.

**Non-negotiables:**
- Output format: Markdown (.md) or MDX (.mdx) only
- All content MUST pass Docusaurus build without errors or warnings
- Images and assets use relative paths that resolve in GitHub Pages
- Frontmatter follows Docusaurus conventions
- No platform-specific features that break cross-browser compatibility

**Rationale:** The delivery platform is non-negotiable; content that fails to build or render correctly is unusable regardless of quality.

## Content Standards

### Output Requirements

- **Format**: Valid Markdown (.md) or MDX (.mdx) files only
- **Encoding**: UTF-8 without BOM
- **Line endings**: LF (Unix-style) for cross-platform compatibility
- **Maximum line length**: No hard limit, but prefer wrapping at ~100 characters for readability in diff views

### Structural Requirements

- **Frontmatter**: Every content file MUST include Docusaurus-compatible frontmatter
- **Heading hierarchy**: Start at H1, no skipped levels (H1 → H2 → H3)
- **File naming**: Kebab-case (e.g., `getting-started.md`, `api-reference.md`)
- **Directory structure**: Mirrors book structure; one directory per major section

### Quality Gates

Before any content is considered complete:
1. Markdown linting passes (no syntax errors)
2. Docusaurus local build succeeds
3. All internal links resolve
4. Code samples execute without error
5. Content matches approved specification

## Development Workflow

### Content Creation Process

1. **Specification**: Content requirements defined in `specs/<feature>/spec.md`
2. **Planning**: Technical approach documented in `specs/<feature>/plan.md`
3. **Task Breakdown**: Atomic writing tasks listed in `specs/<feature>/tasks.md`
4. **Authoring**: Content written following spec and constitution principles
5. **Review**: Content validated against acceptance criteria
6. **Integration**: Merged to main branch after passing quality gates

### Review Checklist

All content reviews MUST verify:
- [ ] Content adheres to approved specification
- [ ] Writing meets clarity standards for target audience
- [ ] All technical claims are accurate and verifiable
- [ ] Structure is modular and navigation-friendly
- [ ] Markdown is valid and builds successfully
- [ ] Terminology is consistent with glossary/prior content

### Scope Control

- No extra sections beyond what specification requests
- No feature additions without spec amendment
- Smallest viable content change per task
- Each PR/commit should be independently reviewable

## Governance

### Constitution Authority

This constitution supersedes all other practices and guidelines. When conflicts arise between this document and other guidance, this constitution takes precedence.

### Amendment Process

1. **Proposal**: Changes proposed via PR with rationale
2. **Review**: All stakeholders review impact
3. **Approval**: Explicit approval required before merge
4. **Migration**: Existing content assessed for compliance
5. **Documentation**: Amendment recorded with version increment

### Version Policy

- **MAJOR**: Backward-incompatible principle changes or removals
- **MINOR**: New principles added or existing principles materially expanded
- **PATCH**: Clarifications, wording improvements, typo fixes

### Compliance

- All content PRs MUST verify compliance with constitution principles
- Complexity beyond constitution guidelines MUST be justified in writing
- Non-compliance discovered post-merge requires remediation plan

**Version**: 1.0.0 | **Ratified**: 2026-01-09 | **Last Amended**: 2026-01-09
