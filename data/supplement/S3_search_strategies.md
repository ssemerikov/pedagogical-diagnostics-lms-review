# S3. Search strategies

Generated 2026-11-14 from the run records in the review data.

## 1. OUCI, original search (January 2026)
- Database: Open Ukrainian Scientific Content Initiative (OUCI), https://ouci.dntb.gov.ua/
- Field: the simple-search field (`title=` parameter), which covers title, abstract and DOI
- Query (vertical bar = OR, juxtaposition = AND):

```
(LMS | "learning  management system" | "distance learning")  (empirical | experiment | experimental  | "real-life") (sign  | signs | measurement | measure | criteria | criterion | parameter | factor ) ("learning style" | "cognitive style" | "personality type" | "sensory preference" | "modality" | "Personality Computing" | "Automatic Personality Recognition" | "Automatic Personality Perception" | systematicity | motivation | stability | mobilisation | reflection | prognosis | Self-management)
```
- Run: early January 2026 (full-text retrieval attempts dated 4–5 January 2026); no date, language or document-type limits
- Records: 118

## 2. Scopus (update)
- Database: Scopus (Elsevier Scopus Search API, STANDARD view)
- Field: TITLE-ABS-KEY; limits: none (no date, language or document-type limits)
- Query:

```
TITLE-ABS-KEY ( ( LMS OR "learning management system" OR "distance learning" ) AND ( empirical OR experiment OR experimental OR "real-life" ) AND ( sign OR signs OR measurement OR measure OR criteria OR criterion OR parameter OR factor ) AND ( "learning style" OR "cognitive style" OR "personality type" OR "sensory preference" OR "modality" OR "Personality Computing" OR "Automatic Personality Recognition" OR "Automatic Personality Perception" OR systematicity OR motivation OR stability OR mobilisation OR reflection OR prognosis OR Self-management ) )
```
- Run: 2026-11-12T00:16:46+02:00; records: 596

## 3. OUCI re-run (update)
- Same query and field as search 1
- Run: 2026-11-12T08:16:25+02:00 – 2026-11-12T08:23:04+02:00; records stated by OUCI: 184 публікацій; collected: 184
- Field scope evidence: The simple-search field that the 'title=' parameter fills is labelled 'Назва, анотація, DOI' (Title, abstract, DOI) on the results page; keywords are not named.

## 4. Other methods
- Citation chaining from included studies (original review: 1 study).
- Full texts not retrievable automatically were sought by the review team through open-access sources, library access and author request (protocol amendment to exclusion criterion E7; see S1, column `route`).
