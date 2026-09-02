# Evidence Contract

The scripts check offline record consistency. They cannot certify scientific truth,
perform an independent peer review, or authorize a submission. A review record must
describe a review that actually happened; do not fill it with an invented person or date.

## Records

`schemas/workspace_contract.yaml` is the single CSV contract. Legacy schema filenames
point to it. Templates are generated from its columns; records are checked against
its required values, enums, and unique IDs.

| Record | Identifier | Links |
|---|---|---|
| Literature matrix, including official requirement sources | `paper_id` | URL/DOI or workspace-relative source file; read scope and recorded reviewer/date |
| Experiment matrix | `experiment_id` | Actual result summary, artifact, data IDs, procedure, code version |
| Evidence records | `evidence_id` | `source_id` references `paper_id`; `result_id` references `experiment_id`; or a local artifact |
| Claim ledger | `claim_id` | `evidence_ids` and exact output section |
| Requirement register | `requirement_id` | Verified official source, locator, applicability, acceptance criteria |
| Graduation evidence map | `requirement_id` | Evidence IDs showing the applicable requirement is met |

Separate multiple IDs with semicolons. Local artifact paths are relative to the
research workspace and must stay inside it. Restricted data can use an explicit
access route; no automatic upload or reading outside the workspace is performed.

## Claims

Active factual claims require `status=supported`, a stated strength and evidence type,
and `evidence_ids`. Every evidence record must name the supported claim, a precise
locator, review status, reviewer and date, and a source, result or actual artifact.
Sources must have verified provenance and a recorded read scope. Results must be
achieved, not planned or preliminary, with actual output and data provenance.
Changing a source/result state blocks claims that depend on it on the next check.

`evidence_source` remains a readable legacy pointer; it is not proof and is not used
instead of evidence IDs. Source `user_provided` and result `achieved` are not claim
support statuses.

An explicit limitation, proposal or assumption uses `claim_kind=limitation|proposal|assumption`,
`status=unknown`, and `strength=low|none`. It can remain in a bounded draft, but its
uncertain label must survive export. Do not relabel a factual result to evade checks.
The script cannot interpret every sentence; final wording still needs human review.

Use `output_scope=backlog` for a claim not used in the current output. Keep the record,
do not delete it merely to get a passing result. `--section Results` checks only active
claims in that exact section. Empty selections and nonexistent targets are blocked.

## Gate Decisions

| Decision | Meaning |
|---|---|
| `blocked` | Missing/invalid records, unfinished artifacts, or inconsistent dependencies |
| `structure_valid` | Initialization structure is valid; no stage completion asserted |
| `evidence_review_required` | Machine checks passed but recorded human sign-off is absent/incomplete |
| `ready_for_handoff` | Applicable offline checks and a recorded stage review passed |
| `not_applicable` | A supported non-quantitative analysis exemption has an explicit reason and review |

The pre-prose command returns `ready_for_human_review`, not final prose or submission
approval. A stage review is recorded in `project_state.yaml`, for example:

```yaml
gate_reviews:
  drafting:
    decision: ready
    reviewed_by: "Name of the actual reviewer"
    reviewed_at: "YYYY-MM-DD"
    scope: "Which claims, artifacts, and limitations were actually reviewed"
```

The placeholder date is intentionally invalid until replaced with the real review.
Markdown stage artifacts need an explicit `Gate status: ready` or `complete`, no
unchecked tasks, and no empty fields. For non-applicable fields record a reason.
Writing `ready` alone does not satisfy a stage gate.

All project types share literature and analysis templates. Thesis/hybrid submission,
final and defense also require verified requirements and complete evidence mappings.
Proposal and midterm keep the requirement context without pretending the thesis is done.
For a theoretical/review/qualitative project with no quantitative analysis, a reviewed
`gate_exemptions.analysis` mapping may specify `reason`, `reviewed_by`, and `reviewed_at`.
An experimental project cannot use this exemption.

## Validation Boundaries

Checks cover schema/enum errors, duplicate and unresolved IDs, selected claim status,
source/result downgrades, missing attachments, recorded review fields, stage applicability,
and unfinished checklists. They do not prove that a PDF supports a sentence, that a
reviewer identity is genuine, or that an uploaded experimental artifact is honest.
No model hallucination reduction percentage or end-to-end provider ranking is claimed.
