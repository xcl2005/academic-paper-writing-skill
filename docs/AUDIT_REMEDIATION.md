# Reliability Fixes in 2.1.0

Baseline: `6ec2c6f`. This record distinguishes repaired defects from longer-term
design proposals. It does not claim that every item in an external audit is a bug,
or that offline tests establish scientific truth.

| Audit issue | Implemented correction | Regression evidence |
|---|---|---|
| P1-01 | Selected factual claims need real evidence records; explicit uncertain notes/backlog are separate | Empty support, multilingual numeric unknowns, legitimate limitation, section selection |
| P1-02 | Stable IDs connect claims, sources, results, data and artifacts with recorded review | Dangling/duplicate IDs, missing files, source downgrade, planned results, missing data |
| P1-03 | Shared validation plus stage applicability and recorded human review | Empty Markdown, missing status, unchecked items, unsupported claims, structure-only output |
| P1-04 | All initializers persist project type; shared matrices exist; thesis requirements affect delivery | Three modes, type-conflict preservation, reviewed N/A, missing requirement/evidence mapping |
| P1-05 | One canonical CSV contract, generated templates/schema references, legacy migration | Required columns, enum validation, canonical examples, migration preview/backup/idempotence |
| P1-06 | Non-discoverable fixture extension, materialized only in temporary tests | Exactly one installable `SKILL.md`; isolated provider roots |
| P1-07 | Pinned dependency and explicit runtime/working-directory documentation | New Python environment without PyYAML, dependency install, complete checks |
| P2-19/20 | Provider metadata/resources/companions and explicit Codex/Claude discovery roots | Invalid/empty provider, missing resources/companion, duplicate precedence, host roots |
| P2-21 | Owned-demo replacement, guarded paths, generate before replacing | Unowned folder, repository/ancestor, user additions, simulated generation failure |
| Additional | Nonexistent inputs and empty selections cannot pass | Empty directory, nonexistent path, wrong input type |

Related improvements include cheaper module loading, source/instruction authority
separation, clearer provider-screening limits and negation handling, one maintainer
check, and pinned cross-platform CI. Existing modes, provider mappings, and the public
README's core-feature/skill-first layout are retained.

## Not Claimed by This Release

- Independent verification of scientific conclusions or genuine reviewer identity.
- End-to-end execution/ranking of all 18 third-party research providers.
- Complete disciplinary thesis profiles or a complete systematic-review database.
- Measured README conversion or star-growth improvements.
- A new private vulnerability-reporting channel or changed GitHub administration settings.

The broader novelty/ROI methodology, discipline-specific recipes, richer delivery
templates, real-study demonstrations, and artwork/marketing proposals remain separate
design work. See [Evidence Contract](EVIDENCE_CONTRACT.md), [Migration](MIGRATION.md),
and the actual test results when evaluating the scope of the reliability fixes.
