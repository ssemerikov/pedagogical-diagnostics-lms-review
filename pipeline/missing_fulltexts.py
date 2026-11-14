#!/usr/bin/env python3
# Public-repository copy of the review's working script, derived automatically: only paths, output
# locations and the handling of private inputs differ from the working copy (see README.md).
"""List every record that should have a full text but does not yet (for manual retrieval). Run from the repository root."""
import json, glob, csv, os, sys, datetime
from collections import Counter
L = lambda p: [json.loads(l) for l in open(p)] if os.path.exists(p) else []
route = {}
for d in L('data/fulltext_routes.jsonl'): route[d['id']] = d['route']   # last line wins; 'invalid' = wrong/unusable file
if not os.path.isdir('data/fulltext'):  # public repository: no full texts; the route log says which were obtained
    print('missing_fulltexts: data/fulltext/ is absent (full texts are not distributed); deciding from '
          'data/fulltext_routes.jsonl', file=sys.stderr)
    have = lambda i: route.get(i) in ('oa_auto', 'manual_user', 'author')
else:
  have = lambda i: route.get(i) != 'invalid' and any(os.path.exists(f'data/fulltext/{i}.{e}') and os.path.getsize(f'data/fulltext/{i}.{e}') > 2000 for e in ('txt', 'pdf', 'html'))
pri = {}
for f in glob.glob('data/scopus/ta_audit/maybe*.jsonl'):
    for d in L(f): pri[d['id']] = d['priority']
ta = {}
for f in glob.glob('data/scopus/ta_batches/*.jsonl'):
    for d in L(f): ta[d['id']] = d
skip = {o['id'] for o in json.load(open('data/scopus/screening_setup.json'))['overlap_with_ouci118']} | {'2-s2.0-105009000141', '2-s2.0-85108022090'}
meta = {}
for x in L('data/scopus/records.jsonl'): meta[x['eid']] = (x['doi'], x['year'], x.get('first_author', ''), x['title'], x.get('open_access_flag'))
for p in ('data/scopus/openalex.jsonl', 'data/ouci/openalex.jsonl', 'data/noaa/openalex.jsonl', 'data/reextract/openalex.jsonl'):
    for x in L(p):
        if x['id'] not in meta: meta[x['id']] = (x.get('oa_doi'), x.get('oa_year'), '', x.get('oa_title'), None)
oaflag = {}
for p in ('data/scopus/openalex.jsonl', 'data/ouci/openalex.jsonl', 'data/noaa/openalex.jsonl', 'data/reextract/openalex.jsonl'):
    for x in L(p): oaflag[x['id']] = x.get('is_oa')
rows = []
def add(tier, arm, i, screen):
    d, y, a, t, sf = meta.get(i, (None, '', '', '', None))
    if route.get(i) == 'invalid': screen += ' | WRONG FILE saved, please re-save'
    rows.append({'tier': tier, 'arm': arm, 'id': i, 'doi': d or '', 'year': y or '', 'first_author': a or '', 'title': (t or '')[:150], 'screen': screen,
                 'oa': 'OA-listed' if (oaflag.get(i) or sf in (True, 'true')) else '', 'save_as': f'data/fulltext/{i}.pdf'})
for x in L('data/reextract/in.jsonl'):
    if not have(x['id']): add(0, 'Already-included study (re-extraction)', x['id'], 'included')
for p, arm in (('data/scopus/retrieval_log.jsonl', 'Scopus'), ('data/ouci/retrieval_log.jsonl', 'OUCI re-run (new)')):
    for r in L(p):
        i = r['id']
        if i in skip or i == 'OUCI2-4VPazBzY' or r['result'] == 'retrieved' or have(i): continue
        v = ta.get(i, {}); band = 'pass' if v.get('verdict') == 'pass' else pri.get(i, 'maybe')
        add({'pass': 1, 'high': 1, 'medium': 2, 'maybe': 2, 'low': 3}.get(band, 2), arm, i, band)
for r in L('data/noaa/retrieval_log.jsonl'):
    if r['result'] != 'retrieved' and not have(r['id']): add(2, 'Original OUCI 2026-01 (excluded: no OA)', r['id'], 'orig no-OA')
rows.sort(key=lambda x: (x['tier'], x['oa'] != 'OA-listed', x['arm'], str(x['year'])))
os.makedirs('out', exist_ok=True)
with open('out/missing_fulltexts.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
md = ['# Studies still missing full texts (generated ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M') + ')', '',
      'Save each file EXACTLY at `save_as` (relative to the repository root); .pdf preferred. Re-run `python3 pipeline/missing_fulltexts.py` to refresh.',
      'Tier 0 = already-included studies (re-extraction of n/effect sizes); 1 = passed screening or high priority; 2 = medium + the originally no-OA records; 3 = low priority.',
      '`OA-listed` = an open-access copy is listed (OpenAlex/Scopus) but our scripts were blocked.', '',
      '| Tier | Arm | DOI | Year | First author | Title | Screen | OA | Save as |', '|---|---|---|---|---|---|---|---|---|']
md += [f"| {r['tier']} | {r['arm']} | {r['doi']} | {r['year']} | {r['first_author']} | {r['title'][:110]} | {r['screen']} | {r['oa']} | `{r['save_as']}` |" for r in rows]
open('out/missing_fulltexts.md', 'w').write('\n'.join(md) + '\n')
print(len(rows), sorted(Counter((r['tier'], r['arm'][:8]) for r in rows).items()), 'OA-listed', sum(1 for r in rows if r['oa']))
for r in rows:
    if r['tier'] <= 1: print(f"T{r['tier']} | {r['doi'] or '(no DOI)'} | {r['year']} | {r['first_author']} | {r['title'][:80]} | {r['oa']} | {r['save_as']}")
