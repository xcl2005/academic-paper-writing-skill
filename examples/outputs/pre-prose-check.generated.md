# Pre-Prose Workspace Gate

Target: `examples/generated-demo-workspace`
Decision: **BLOCKED**

## Evidence Status

Checked CSV files: 10
Errors: 0

No evidence status errors found.

## Claim-to-Evidence

Checked claim files: 1
Blockers: 8

| File | Row | Claim ID | Status | Reason | Fix suggestion |
|---|---:|---|---|---|---|
| examples/generated-demo-workspace/claim_ledger.csv | 2 | C1 | partially_supported | Factual claim is partially_supported, not supported; add evidence or retain it in the backlog. | Supply the named evidence and review record, or explicitly exclude this claim from the current output. |
| examples/generated-demo-workspace/claim_ledger.csv | 2 | C1 | partially_supported | claim: missing/invalid evidence_ids | Supply the named evidence and review record, or explicitly exclude this claim from the current output. |
| examples/generated-demo-workspace/claim_ledger.csv | 3 | C2 | blocked | Factual claim is blocked, not supported; add evidence or retain it in the backlog. | Supply the named evidence and review record, or explicitly exclude this claim from the current output. |
| examples/generated-demo-workspace/claim_ledger.csv | 3 | C2 | blocked | claim: missing/invalid evidence_ids | Supply the named evidence and review record, or explicitly exclude this claim from the current output. |
| examples/generated-demo-workspace/claim_ledger.csv | 3 | C2 | blocked | claim: missing/invalid strength | Supply the named evidence and review record, or explicitly exclude this claim from the current output. |
| examples/generated-demo-workspace/claim_ledger.csv | 4 | C3 | unknown | Factual claim is unknown, not supported; add evidence or retain it in the backlog. | Supply the named evidence and review record, or explicitly exclude this claim from the current output. |
| examples/generated-demo-workspace/claim_ledger.csv | 4 | C3 | unknown | claim: missing/invalid evidence_ids | Supply the named evidence and review record, or explicitly exclude this claim from the current output. |
| examples/generated-demo-workspace/claim_ledger.csv | 4 | C3 | unknown | claim: missing/invalid strength | Supply the named evidence and review record, or explicitly exclude this claim from the current output. |

Next action: Produce a blocked-output explanation until evidence status errors and claim blockers are resolved.

Offline structure, recorded review, and dependency checks only; not independent scientific verification or submission approval.
