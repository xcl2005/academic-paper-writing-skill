# 02 Mode Router

## Project Type Router

Project type sets context and priorities. It does not prescribe a predetermined route. Select capabilities from `capability_registry.yaml` for the current task.

### Research Paper

Use for publishable research work. Load literature, novelty, ROI, experiment, venue, integrity, writing, and review/rebuttal modules.

### Undergraduate Thesis

Use for school-assessed thesis/graduation project. Load requirement discovery, thesis engine, evidence mapping, testing, writing style, and integrity modules.

### Hybrid Capstone Research

Use when graduation is the first priority but the work may become a paper/portfolio item. Start with thesis route; upgrade only after graduation requirements and evidence are covered.

### Standalone Research Task

Use for a bounded search, paper reading, statistical audit, figure, polishing pass, review, rebuttal, data statement, or presentation. Load core invariants plus the matching capability only; a full project workspace is optional.

## Capability Composition

- Search and literature synthesis are separate capabilities; retrieval can finish without writing a review.
- Study design, statistical analysis, and figure production can share evidence, but each keeps its own acceptance checks.
- Manuscript drafting and polishing are distinct; polishing must not silently change evidence, numbers, citations, or claim strength.
- Peer-review assessment and author response are distinct contexts.
- Submission packaging and paper-to-presentation reuse source records but have separate artifact QA.

## Formatting Mode Router

### Submission Mode

Use official venue/journal/school template and current author instructions. Compliance overrides beauty.

### Publication-Style Mode

Use when the user wants a paper to look professional but not necessarily comply with a submission. Avoid fake DOI, fake journal branding, or misleading publisher metadata.

### User-Template Mode

Use the user's provided template as the source of truth. Preserve content unless the user asks for rewriting.

### School-Template Mode

For undergraduate thesis, school template and advisor instructions override generic academic style.

### Provider-Specific Mode

When an installed provider is selected, follow its detailed format, backend, and QA rules for that capability. Bind it through the registry and validate its output; do not make the provider a permanent dependency of unrelated modes.
