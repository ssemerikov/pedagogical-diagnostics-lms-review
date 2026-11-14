#!/usr/bin/env python3
# Public-repository copy of the review's working script, derived automatically: only paths, output
# locations and the handling of private inputs differ from the working copy (see README.md).
"""Ingest full texts saved into data/fulltext/ (by scripts or by hand) and log how each was obtained (decision D8).

Run from the repository root:  python3 -I pipeline/ingest_fulltexts.py
Full texts are not distributed with this repository: without data/fulltext/ the script says so and exits.
- converts every <id>.pdf without a usable <id>.txt with `pdftotext -layout`;
- route: `oa_auto` if a retrieval log records the id as retrieved, else `manual_user`
  (an `author` route is set by hand in data/fulltext_routes.jsonl when a copy comes from the authors);
- checks the text against the expected title/DOI, flags scanned or duplicate files;
- keeps a private log with checksums in data/fulltext/ingest_log.jsonl (git-ignored) and appends one line
  (id, route, date) per newly logged file to data/fulltext_routes.jsonl (append-only);
- writes the check table to out/ingest_report.md.
"""
import csv, glob, hashlib, json, os, re, shutil, subprocess, sys, datetime, unicodedata

L = lambda p: [json.loads(l) for l in open(p, encoding='utf-8') if l.strip()] if os.path.exists(p) else []
FT = 'data/fulltext'
if not os.path.isdir(FT):
    print('ingest_fulltexts: data/fulltext/ is absent. Full texts are not distributed with this repository '
          '(copyright); save PDFs there as <id>.pdf to run this step.', file=sys.stderr)
    raise SystemExit(0)
if shutil.which('pdftotext') is None:
    print('ingest_fulltexts: pdftotext (poppler-utils) is required and was not found.', file=sys.stderr)
    raise SystemExit(0)
PRIVATE_LOG = os.path.join(FT, 'ingest_log.jsonl')
now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

# expected metadata ----------------------------------------------------------------------------
meta = {}
for x in L('data/scopus/records.jsonl'):
    meta[x['eid']] = {'title': x.get('title'), 'doi': x.get('doi'), 'arm': 'S'}
for p, arm in (('data/ouci/openalex.jsonl', 'O2'), ('data/noaa/openalex.jsonl', 'N'), ('data/reextract/openalex.jsonl', 'R')):
    for x in L(p):
        m = meta.setdefault(x['id'], {'title': None, 'doi': None, 'arm': arm})
        m['title'] = m['title'] or x.get('oa_title'); m['doi'] = m['doi'] or x.get('oa_doi')
for p, arm in (('data/ouci/new_records.jsonl', 'O2'), ('data/noaa/in.jsonl', 'N'), ('data/reextract/in.jsonl', 'R')):
    for x in L(p):
        i = x.get('id') or ('OUCI2-' + x['ouci_work'] if x.get('ouci_work') else None)
        if not i: continue
        m = meta.setdefault(i, {'title': None, 'doi': None, 'arm': arm})
        m['title'] = m['title'] or x.get('title'); m['doi'] = m['doi'] or x.get('doi'); m['arm'] = arm
tier = {}
if os.path.exists('out/missing_fulltexts.csv'):
    for r in csv.DictReader(open('out/missing_fulltexts.csv', encoding='utf-8')):
        tier[r['id']] = r['tier']
auto = set()
for p in glob.glob('data/*/retrieval_log.jsonl'):
    for r in L(p):
        if r.get('result') == 'retrieved': auto.add(r['id'])
logged = {(r['id'], r['sha256']) for r in L(PRIVATE_LOG)}

def norm(s):
    s = unicodedata.normalize('NFKD', s or '').lower()
    s = re.sub(r'-\s*\n\s*', '', s)
    return re.sub(r'[^\w]+', ' ', s)

def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()

ids = sorted({os.path.basename(p).rsplit('.', 1)[0] for p in glob.glob(f'{FT}/*.pdf') + glob.glob(f'{FT}/*.html')})
rows, by_sha = [], {}
for i in ids:
    pdf, html, txt = f'{FT}/{i}.pdf', f'{FT}/{i}.html', f'{FT}/{i}.txt'
    src = pdf if os.path.exists(pdf) else html
    converted = False
    if src == pdf and (not os.path.exists(txt) or os.path.getsize(txt) < 2000 or os.path.getmtime(pdf) > os.path.getmtime(txt)):
        subprocess.run(['pdftotext', '-layout', pdf, txt], capture_output=True, timeout=300)
        converted = True
    text = open(txt, encoding='utf-8', errors='replace').read() if os.path.exists(txt) else ''
    words = len(text.split())
    head = norm(text[:15000])
    m = meta.get(i, {})
    toks = [t for t in norm(m.get('title')).split() if len(t) >= 4]
    tmatch = round(sum(t in head for t in toks) / len(toks), 2) if toks else None
    doi = (m.get('doi') or '').lower()
    dmatch = bool(doi) and doi in text.lower().replace(' ', '')
    cyr = sum('Ѐ' <= c <= 'ӿ' for c in text[:20000]); lat = sum('a' <= c.lower() <= 'z' for c in text[:20000])
    lang = 'cyrillic' if cyr > lat else 'latin'
    h = sha(src)
    by_sha.setdefault(h, []).append(i)
    route = 'oa_auto' if i in auto else 'manual_user'
    flag = []
    if words < 800: flag.append('short_or_scanned')
    if toks and tmatch is not None and tmatch < 0.6 and not dmatch: flag.append('title_mismatch?')
    rows.append({'id': i, 'arm': m.get('arm', '?'), 'tier': tier.get(i, ''), 'route': route, 'file': os.path.basename(src),
                 'bytes': os.path.getsize(src), 'sha256': h, 'words': words, 'title_match': tmatch, 'doi_in_text': dmatch,
                 'script': lang, 'converted_now': converted, 'flags': flag, 'title': (m.get('title') or '')[:120]})
for r in rows:
    dup = [j for j in by_sha[r['sha256']] if j != r['id']]
    if dup: r['flags'].append('same_file_as:' + ','.join(dup))

with open(PRIVATE_LOG, 'a', encoding='utf-8') as f, open('data/fulltext_routes.jsonl', 'a', encoding='utf-8') as pub:
    for r in rows:
        if (r['id'], r['sha256']) in logged: continue
        f.write(json.dumps({'id': r['id'], 'arm': r['arm'], 'route': r['route'], 'file': r['file'], 'bytes': r['bytes'],
                            'sha256': r['sha256'], 'words': r['words'], 'title_match': r['title_match'],
                            'doi_in_text': r['doi_in_text'], 'flags': r['flags'], 'logged_on': now}, ensure_ascii=False) + '\n')
        pub.write(json.dumps({'id': r['id'], 'route': r['route'], 'logged_on': now[:10]}, ensure_ascii=False) + '\n')

md = [f'# Full-text ingest report ({now})', '', f'{len(rows)} files; routes: ' +
      ', '.join(f"{k} {sum(r['route'] == k for r in rows)}" for k in ('oa_auto', 'manual_user')), '',
      '| id | arm | tier | route | words | title match | DOI in text | script | flags | expected title |', '|---|---|---|---|---|---|---|---|---|---|']
for r in sorted(rows, key=lambda r: (not r['flags'], r['route'], r['id'])):
    md.append(f"| {r['id']} | {r['arm']} | {r['tier']} | {r['route']} | {r['words']} | {r['title_match']} | {r['doi_in_text']} | {r['script']} | {' '.join(r['flags'])} | {r['title']} |")
os.makedirs('out', exist_ok=True)
open('out/ingest_report.md', 'w', encoding='utf-8').write('\n'.join(md) + '\n')
print(len(rows), 'files;', sum(r['converted_now'] for r in rows), 'converted now;',
      sum(r['route'] == 'manual_user' for r in rows), 'manual_user;', sum(bool(r['flags']) for r in rows), 'flagged')
for r in rows:
    if r['flags']: print(r['id'], r['arm'], r['words'], r['title_match'], r['doi_in_text'], r['flags'], '|', r['title'][:70])
