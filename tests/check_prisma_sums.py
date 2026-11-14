#!/usr/bin/env python3
# Public-repository copy of the review's working script, derived automatically: only paths, output
# locations and the handling of private inputs differ from the working copy (see README.md).
"""Check that every PRISMA box in data/counts.tex sums. Run from the repository root after pipeline/make_counts.py (`make check`)."""
import re, json, sys
m = dict(re.findall(r'\\newcommand\{\\(\w+)\}\{([^}]*)\}', open('data/counts.tex').read()))
g = lambda k: int(m[k]); s = lambda *ks: sum(g(k) for k in ks)
c = json.load(open('data/prisma_counts.json'))
chk = [
 ('O1: sought = notret + assessed', g('nSought'), s('nNotRetrieved', 'nAssessedFT')),
 ('O1: assessed = excluded + included', g('nAssessedFT'), s('nExcludedFT', 'nIncluded')),
 ('S: records = overlap + screened', g('nScopusRecords'), s('nScopusOverlapOuci', 'nScopusScreened')),
 ('S: screened = TAexcl + sought', g('nScopusScreened'), s('nScopusTAExcluded', 'nScopusSought')),
 ('S: sought = notret + assessed', g('nScopusSought'), s('nScopusNotRetrieved', 'nScopusAssessed')),
 ('S: assessed = ftexcl + incl', g('nScopusAssessed'), s('nScopusFTExcluded', 'nScopusIncluded')),
 ('O2: records = dupO1 + dupS + new', g('nOuciRerunRecords'), s('nOuciRerunDupOrig', 'nOuciRerunDupScopus', 'nOuciRerunNew')),
 ('O2: new = TAexcl + sought', g('nOuciRerunNew'), s('nOuciRerunTAExcluded', 'nOuciRerunSought')),
 ('O2: sought = notret + assessed', g('nOuciRerunSought'), s('nOuciRerunNotRetrieved', 'nOuciRerunAssessed')),
 ('O2: assessed = ftexcl + incl', g('nOuciRerunAssessed'), s('nOuciRerunFTExcluded', 'nOuciRerunIncluded')),
 ('N: resought = notret + assessed', g('nNoOAReSought'), s('nNoOANotRetrieved', 'nNoOAAssessed')),
 ('N: assessed = ftexcl + incl', g('nNoOAAssessed'), s('nNoOAFTExcluded', 'nNoOAIncluded')),
 ('Upd: screened = S + O2', g('nUpdateScreened'), s('nScopusScreened', 'nOuciRerunNew')),
 ('Upd: TAexcl = S + O2', g('nUpdateTAExcluded'), s('nScopusTAExcluded', 'nOuciRerunTAExcluded')),
 ('Upd: sought = S + O2', g('nUpdateSought'), s('nScopusSought', 'nOuciRerunSought')),
 ('Upd: assessed = S + O2', g('nUpdateAssessed'), s('nScopusAssessed', 'nOuciRerunAssessed')),
 ('Upd: FTexcl = S + O2', g('nUpdateFTExcluded'), s('nScopusFTExcluded', 'nOuciRerunFTExcluded')),
 ('Upd: includedDB = S + O2', g('nUpdateIncludedDB'), s('nScopusIncluded', 'nOuciRerunIncluded')),
 ('Upd: included = DB + N', g('nUpdateIncluded'), s('nUpdateIncludedDB', 'nNoOAIncluded')),
 ('FT routes = assessed S+O2+N', s('nFTAuto', 'nFTManual'), s('nUpdateAssessed', 'nNoOAAssessed')),
 ('Residual = upd notret + N notret', g('nResidualNotRetrieved'), s('nUpdateNotRetrieved', 'nNoOANotRetrieved')),
 ('Total included', g('nIncludedTotal'), s('nIncluded', 'nUpdateIncluded')),
 ('TA codes sum = update TA excluded', sum(c['taExcludedByCode'].values()), g('nUpdateTAExcluded')),
 ('FT codes sum = FT excluded S+O2+N', sum(c['ftExcludedByCode'].values()), s('nUpdateFTExcluded', 'nNoOAFTExcluded')),
 ('Report base = total included', g('nReportBase'), g('nIncludedTotal')),
]
bad = 0
for name, a, b in chk:
    print('OK ' if a == b else 'BAD', name, a, b); bad += a != b
print('pending records:', m['nUpdatePending'])
sys.exit(1 if bad or m['nUpdatePending'] != '0' else 0)
