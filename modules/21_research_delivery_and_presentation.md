# 21 Research Delivery and Presentation

## Purpose

Package evidence into submission materials, data/code availability records, paper-reading notes, and research presentations without weakening traceability.

## Paper Reading Contract

For a paper, preprint, thesis, or technical report, use `templates/paper_reading_note.md` and separate:

- bibliographic facts and source boundary;
- the authors' central claim;
- research question and contribution type;
- method, study design, data, baselines, and analysis;
- key results with exact figure, table, or section pointers;
- limitations stated by the authors;
- additional limitations inferred by the agent, clearly labeled as inference;
- reproducibility assets and unresolved verification questions.

Do not infer figure values from appearance when exact values are unavailable. Do not treat a paper's own claim as independent validation.

## Data and Code Availability

For each supporting asset, map dataset or code to its access route: public repository, controlled access, supplementary material, reused public source, justified request process, restricted third-party source, or not applicable.

- Choose repository and identifier strategy before drafting the statement.
- Record licences, versions, accession numbers or DOIs, access conditions, metadata, and file relationships only when verified.
- Flag `available upon request` as weak unless a concrete legal, ethical, privacy, commercial, or third-party restriction justifies it.
- Keep Data Availability, Code Availability, materials, preregistration, and supplementary information consistent with the manuscript and `templates/data_provenance.csv`.

## Submission Package

Use `templates/submission_package_checklist.md` to reconcile:

- manuscript, title page, abstract, keywords, highlights, cover letter, and declarations;
- figures, tables, captions, source data, and supplementary files;
- references and in-text citations;
- reporting guideline or checklist when applicable;
- ethics, consent, conflicts, funding, author contributions, acknowledgements, and AI-use disclosure as required;
- data, code, model, protocol, and preregistration availability;
- venue or school formatting and file requirements.

Never invent author identities, approvals, declarations, accession numbers, reviewer suggestions, or venue requirements.

## Paper-to-Presentation Standard

1. Classify the source: discovery/mechanism, method/tool, resource/dataset, clinical/population, materials/engineering, or review/meta-analysis.
2. Define audience, purpose, language, time, and deliverable format in `templates/presentation_brief.md`.
3. Build the narrative around the scientific argument, not the manuscript section order.
4. Use figures and tables as evidence. Preserve captions, units, panel labels, and source references; crop or split dense panels instead of shrinking them beyond readability.
5. Maintain the terminology ledger across slides and notes.
6. Include interpretation, limitations, and discussion prompts proportional to the source evidence.
7. When the user requests a real deck, use an available presentation artifact skill or tool to create the actual PPTX, not only an outline. Preserve this skill's evidence and integrity rules across the handoff.
8. Render and inspect the finished deck. Check slide count, text overflow, clipping, figure crops, alignment, contrast, fonts, citations, speaker notes, and package integrity. High-severity visual or factual issues block delivery.

## Delivery Gate

A package is ready only when its source boundary, unresolved fields, consistency checks, and artifact QA are visible. Final submission, public release, authorship, ethics, and restricted-data decisions remain human decisions.
