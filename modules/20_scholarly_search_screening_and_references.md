# 20 Scholarly Search, Screening, and Reference Management

## Purpose

Run reproducible scholarly discovery and reference workflows. Use for paper lookup, multi-source search, scoping or systematic reviews, citation verification, citation-network expansion, deduplication, and BibTeX/RIS/NBIB management.

## Select the Search Mode

- `lookup`: find or verify a known title, DOI, PMID, arXiv ID, author, or paper.
- `rapid_scan`: map a field quickly and state coverage limits.
- `scoping_review`: characterize concepts, evidence types, and gaps broadly.
- `systematic_review`: use a protocol, reproducible screening, quality assessment, and an appropriate reporting guideline.
- `citation_audit`: verify that cited sources exist and support the attached claims.
- `living_search`: preserve queries and dates so the search can be rerun.

Do not label a rapid scan as systematic. Do not claim exhaustive coverage when database access, language, date, query, or full-text limits remain.

## Search Protocol

Before substantial retrieval, fill `templates/search_protocol.md` with:

- review question or lookup target;
- search mode and reporting guideline when applicable;
- databases, indexes, repositories, citation graphs, and official sources;
- exact query strings, controlled vocabulary, field filters, date run, and limits;
- inclusion and exclusion criteria;
- deduplication and screening procedure;
- quality or risk-of-bias approach;
- update or stopping rule.

## Retrieval Standard

1. Expand concepts into synonyms, acronyms, spelling variants, broader and narrower terms, controlled vocabulary, and adjacent-field terminology.
2. Route by source strength and task fit. Prefer publisher or repository records and primary papers for factual verification; use broad indexes for discovery and citation graphs for expansion.
3. Search more than one source for high-stakes novelty, systematic, or citation audits when feasible.
4. Preserve each query, source, timestamp, limits, reported result count, actual retrieved count, and failure. Never hide a partial result as complete.
5. Deduplicate by stable identifiers first, then normalized title, author, year, and version. Prefer the published version when a preprint and final article represent the same work, while retaining version history when relevant.
6. Screen title/abstract and full text as separate stages. Record one explicit reason for every exclusion in `templates/screening_log.csv`.
7. Verify technical claims against full text, supplementary material, official code, data, or venue policy when the claim requires that depth.
8. Record retractions, corrections, expressions of concern, and inaccessible full text when discovered.

## Citation and Reference Standard

- Verify title, authors, year, venue, identifier, version, and source URL before final citation.
- Check that the source supports the exact nearby claim; topical similarity is not enough.
- Keep paper metadata separate from the agent's interpretation.
- Validate citation keys, in-text/reference-list consistency, duplicates, and required fields.
- Export BibTeX, RIS, NBIB, CSL JSON, or formatted references only from verified metadata.
- Never invent a DOI, PMID, page range, issue, volume, or access URL.

## Synthesis Handoff

Pass included and verified records to `modules/06_literature_engine.md`. Keep excluded, duplicate, unresolved, and inaccessible records in the screening log so the coverage boundary remains auditable.
