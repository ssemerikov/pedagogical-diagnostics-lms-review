# Prompts and decision rules of the review update

The screening and eligibility decisions of the review update were made by two language models (a first pass and a
second reading at each stage) without author verification. This folder holds the instructions those models
were given, so that every decision in `data/` can be read against the rule it applied.

| File | What it is | Given to | Label in the data |
|---|---|---|---|
| [`01_title_abstract_first_pass.md`](01_title_abstract_first_pass.md) | review question, eligibility criteria (verbatim from the article), title/abstract codes and verdicts | Claude Sonnet 5.5 (three shards, A-C) | `screener: claude-sonnet-5-5 (WP02b first pass)` |
| [`02_title_abstract_audit.md`](02_title_abstract_audit.md) | audit of the exclusions; priorities for the `maybe` verdicts | Claude Opus 5.5 | `auditor: claude-opus-5-5 (WP02b audit)` |
| [`03_fulltext_assessment.md`](03_fulltext_assessment.md) | full-text eligibility, the `NOREL` code, the extraction schema, re-extraction of the ten originally included studies | Claude Opus 5.5 | `assessor: claude-opus-5-5 (WP02d)` |
| [`03b_fulltext_decision_rules.md`](03b_fulltext_decision_rules.md) | the decision rules the full-text assessors fixed before their first record, verbatim | written by the assessors; applied by the assessors and the adjudicator | `Rule I` and the codes in `data/ft/` |
| [`04_adjudication.md`](04_adjudication.md) | adjudication by a second reading: Part A every full-text decision and extraction, Part B a sample of title/abstract exclusions, Part C the re-reading of the ten originally included studies | Claude Fable 5.2 | `adjudicator: claude-fable-5-2 (WP05b ...)` |
| [`05_adjudicator_notes_on_rules.md`](05_adjudicator_notes_on_rules.md) | the adjudicator's own notes on how it applied the rules, including what was and was not blind | written by Claude Fable 5.2 | `rule_notes` |

## How the texts were edited

Each file is the text the model was given (files 01-04) or wrote (03b, 05), with one kind of change: references
to internal working files were replaced by `[bracketed descriptions]` or by links to the other files in this
folder. Nothing else was changed, and the first line of each file says so. The replacements are made
mechanically by the export script, which refuses to publish a prompt in which a reference remains.

The prompts name files that are **not** in this repository because they hold abstracts or full texts:
`data/scopus/screen_in_<SHARD>.jsonl` and the audit inputs (titles, abstracts and Scopus metadata), the worklists of
the full-text assessors, the adjudicator's input for the title/abstract sample (its result is
`data/ft/adjudicate_ta_sample.jsonl`), and `data/fulltext/` (the full texts). The progress logs the prompts mention are not
published either; the decisions they recorded are all in `data/`. Where a note says that its figures are
superseded, the data files are the final state. Section 10 of prompt 05 is a snapshot taken before the
Rule I sweep of section 11, so its counts differ from `data/counts.tex`. Where the adjudicator's notes call a
decision "blind", they mean that it was recorded before the assessor's record was opened; section 1 of prompt 05
lists the records for which the assessor's codes had been seen first.

The prompts also contain labels of the working process: `WP02b`, `WP02d` and `WP05b` name the stages; `D2` and `D8`
are decisions of the review's decision log (two-model screening without author verification, and the amendment of
criterion E7); "the orchestrator" is the coordinating model that ran the scripts and set up each stage; "the
user" is the corresponding author. See also [`docs/data_dictionary.md`](../docs/data_dictionary.md).

## Instructions not reproduced here

Some instructions reached the models as short messages when a stage was started or resumed. No verbatim copy of
them is on file with the review's working documents, so they are not reproduced. Their substance is recorded in
the published files:

- the start-up messages that named each model's input shard or worklist;
- the instruction to the assessors of the later full-text worklists to apply the main assessor's decision rules
  (prompt 03b reproduces those rules, and the rules the last assessor added);
- the follow-up instruction to the adjudicator for Part D, an abstract-only triage of the originally unretrieved
  records still without a full text. Its result is `data/ft/noaa_abstract_triage.jsonl`, and the adjudicator
  describes what it did in prompt 05, section 9.

## The original review

The screening of the original review (OUCI, January 2026) is not part of this pipeline. Its decisions were made by
the first author, after a first-pass classification by a language model (Gemini 3.0), and they are reported as made
(`data/original/supplementary_screening.csv`).
