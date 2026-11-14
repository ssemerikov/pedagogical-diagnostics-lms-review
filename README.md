# Pedagogical diagnostics for LMS-integrated forecasting: review data, pipeline and model specification

This repository accompanies the article *Pedagogical diagnostics as a basis for educational recommendation
systems: LMS-integrated forecasting of learning technology effectiveness* by Oleksandr H. Kolgatin, Larysa S.
Kolgatina, Nadiia S. Ponomareva and Serhiy O. Semerikov. It holds three things:

1. the **systematic review**: the per-record screening data of every search, the code that turns those data into
   every count reported in the article, and the instructions given to the language models that screened the
   review update;
2. the **full specification of the forecasting model** that the article proposes, in
   [`docs/forecasting_specification.md`](docs/forecasting_specification.md), with the provenance of every item;
3. the article's **supplementary material** S1-S4, in [`data/supplement/`](data/supplement/).

The article specifies a design and a validation protocol. **It reports no empirical results for the forecasting
model, and this repository contains none.**

## What is here

| Path | Content |
|---|---|
| [`data/`](data/) | every record of every search, with each screening, retrieval and eligibility decision, the model or person that made it, the extracted data and the adjudication; see [`docs/data_dictionary.md`](docs/data_dictionary.md) |
| [`data/supplement/`](data/supplement/) | S1 screening ledger (all records), S2 reassessment of the records originally excluded for lack of an open-access full text, S3 search strategies, S4 proposed LMS indicators for the Ehrman and Leaver dichotomies (uncalibrated; not forecaster inputs) |
| [`pipeline/`](pipeline/) | the review's scripts: Scopus harvest, full-text ingest, list of missing full texts, the count generator and the supplement builder |
| [`prompts/`](prompts/) | the eligibility criteria, the decision rules and the instructions given to each model ([`prompts/README.md`](prompts/README.md)) |
| [`docs/forecasting_specification.md`](docs/forecasting_specification.md) | the forecasting model: the triad of information models, the objective, the input vector, the masked loss, selection bias, the baseline ladder, the weight-sensitivity protocol and the validation-trial protocol |
| [`docs/prisma_flow.md`](docs/prisma_flow.md) | the PRISMA 2020 flow counts, generated from the data |
| [`docs/PRISMA_2020_checklist.md`](docs/PRISMA_2020_checklist.md) | the PRISMA 2020 checklist, with the location of each item in the article |
| [`tests/`](tests/) | the reproducibility test |

## What is not here

- **No full texts.** The studies' PDFs and text files are copyrighted and are not distributed. Short verbatim
  quotes used as evidence for an eligibility decision or an extracted number are kept, each at most 300
  characters.
- **No abstracts.** No abstract is redistributed, whatever its source. For Scopus records only the EID, DOI,
  title and year are kept. The abstracts the screening models read came from OpenAlex (matched by DOI or, where a
  record has no DOI, by identical normalised title with the year within one) and, where OpenAlex had none, from Semantic Scholar by DOI; records
  with no abstract were screened on their title and bibliographic data. The abstracts can be retrieved again from
  those services.
- **No prototype code.** The source code of the authors' prototype is not publicly available. This repository
  contains no implementation of the forecasting model and no runs on real or synthetic data.
- No personal data about students, and no data from any course.

## Who made the screening decisions

- **Original review** (OUCI, searched January 2026; 118 records and one study found by citation chaining). The
  decisions were made by the first author, after a first-pass classification by a language model (Gemini 3.0).
  They are reported as made.
- **Review update** (Scopus and an OUCI re-run, November 2026; plus the 31 records the original review could not
  retrieve). **The screening and eligibility decisions were made by two language models (a first pass and a
  second-reading adjudication) without author verification. The second reading was not blind to the first for
  about fifty records; see `prompts/05_adjudicator_notes_on_rules.md`.**
  - At title and abstract, Claude Sonnet 5.5 made the first pass and Claude Opus 5.5 audited it. A `maybe` was
    never excluded at this stage.
  - Claude Opus 5.5 assessed the full texts and extracted the data.
  - Claude Fable 5.2 adjudicated by a second reading. It re-read every full text and decided eligibility before
    comparing its decision with the assessor's, checked every extracted number against the text, and re-judged a
    10% random sample of the title/abstract exclusions not made for off-topic records. For part of the records it
    had seen the assessor's exclusion codes first; [`prompts/05_adjudicator_notes_on_rules.md`](prompts/05_adjudicator_notes_on_rules.md) says which.
  - The ten originally included studies were re-read under the update's rules (a sensitivity analysis). Their
    original inclusion is not changed.

Every record's `decided_by` field in [`data/screening_master.csv`](data/screening_master.csv) says which procedure
applies to it.

### Departures from the original protocol

- The update adds a title/abstract screening stage, which the original review did not have.
- Exclusion criterion E7 was amended for the update: from "full text not available in open access" to "full text
  not obtainable by the review team (open access, library access or author request)". Full texts were therefore
  sought through every legal route; [`data/fulltext_routes.jsonl`](data/fulltext_routes.jsonl) records how each
  one was obtained. The January 2026 decisions keep the original wording.

## Reproducing the counts

Requirements: Python 3 (standard library only), GNU make and git.

```sh
make counts    # data/screening_master.csv, data/prisma_counts.json, data/counts.tex, docs/prisma_flow.md
make check     # every PRISMA box must sum, and no record may be left pending
make test      # fresh clone -> make counts -> byte-for-byte comparison with the committed files
```

`data/counts.tex` holds the LaTeX macros from which the article takes every count. Apart from the generator path
and the generation stamp in its first two comment lines, it is identical to the macro file of the article. The
`generated` stamp is the newest date recorded in the input data rather than the time of the run, so running
`make counts` again on the same data changes nothing.

`tests/test_reproduce.sh` clones the committed state of the repository into a temporary directory, runs
`make counts supplement` there and requires:

- the regenerated `data/` and `docs/` files to equal the committed ones byte for byte;
- the regenerated supplement S1 and S2 to equal `data/supplement/` byte for byte, and S3 apart from its
  "Generated" date;
- every PRISMA box to sum;
- optionally, with `--ref-tex FILE`, `--ref-json FILE` or `--ref-csv FILE`, a match with external copies such as the
  article's macro file. Only the generator path and the generation stamp are normalised
  ([`tests/compare_outputs.py`](tests/compare_outputs.py)).

## The PRISMA 2020 flow

The review is reported as an updated review. The original review's flow (OUCI search and citation chaining) is
restated as it was decided in January 2026. The update has two database arms, Scopus and the OUCI re-run, after
duplicates of the original review and between the two databases are removed. As other methods, the records the
original review could not retrieve were sought again. [`docs/prisma_flow.md`](docs/prisma_flow.md) gives
every box of the flow with its count and the name of the macro that carries it into the article.

## Scripts that need inputs not distributed here

| Script | Needs | Without it |
|---|---|---|
| `pipeline/scopus_harvest.py` | a personal Scopus API key in `SCOPUS_API_KEY`; writes to `out/scopus/`, never to `data/` | says so and exits |
| `pipeline/ingest_fulltexts.py` | the full texts in `data/fulltext/<id>.pdf` and `pdftotext` | says so and exits |
| `pipeline/missing_fulltexts.py` | nothing; without `data/fulltext/` it decides from the route log | writes `out/missing_fulltexts.{csv,md}` |

The scripts are copies of the review's working scripts. They differ from them only in file locations, in the
handling of these private inputs, and in the deterministic `generated` stamp.

## Citation

Cite the article and this repository; [`CITATION.cff`](CITATION.cff) has the details. The article is under
review.

## Licences

- Code (`pipeline/`, `tests/`, `Makefile`): MIT, see [`LICENSE`](LICENSE).
- Data, prompts and documentation (`data/`, `prompts/`, `README.md`, `docs/`): CC BY 4.0, see
  [`LICENSE-DATA`](LICENSE-DATA).
- Bibliographic metadata of the screened records (titles, years, DOIs and database identifiers) come from Scopus,
  OpenAlex and OUCI and are included only to identify the records. The PRISMA 2020 checklist items are reproduced
  from Page et al. (2021), *BMJ* 372:n71, under CC BY 4.0.
- The short verbatim quotations from the assessed publications in `data/ft/` remain the copyright of their authors
  and publishers. They are reproduced as evidence for the decisions and are not covered by CC BY 4.0.

## Authors

| Author | ORCID | Affiliation |
|---|---|---|
| Oleksandr H. Kolgatin | [0000-0001-8423-2359](https://orcid.org/0000-0001-8423-2359) | Simon Kuznets Kharkiv National University of Economics, Kharkiv, Ukraine |
| Larysa S. Kolgatina | [0000-0003-2650-8921](https://orcid.org/0000-0003-2650-8921) | H. S. Skovoroda Kharkiv National Pedagogical University, Kharkiv, Ukraine |
| Nadiia S. Ponomareva | [0000-0001-9840-7287](https://orcid.org/0000-0001-9840-7287) | Kharkiv University of Technology “STEP”, Kharkiv, Ukraine |
| Serhiy O. Semerikov (corresponding author) | [0000-0003-0789-0272](https://orcid.org/0000-0003-0789-0272) | Kryvyi Rih State Pedagogical University, Kryvyi Rih; Academy of Cognitive and Natural Sciences, Kryvyi Rih; Institute for Digitalisation of Education of the NAES of Ukraine, Kyiv; Zhytomyr Polytechnic State University, Zhytomyr; Center for Information-analytical and Technical Support of Nuclear Power Facilities Monitoring of the NAS of Ukraine, Kyiv; Ukraine |

Questions and corrections: please open an issue in this repository.
