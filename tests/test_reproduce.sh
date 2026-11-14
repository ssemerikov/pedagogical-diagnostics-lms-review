#!/usr/bin/env bash
# Reproducibility test.
#   bash tests/test_reproduce.sh [--ref-tex FILE] [--ref-json FILE] [--ref-csv FILE]
# 1. Clones the committed state of this repository into a temporary directory (uncommitted edits are ignored).
# 2. Runs `make counts supplement` in the clone.
# 3. The regenerated data/screening_master.csv, data/prisma_counts.json, data/counts.tex and docs/prisma_flow.md
#    must equal the committed files byte for byte. (`generated` is the newest date in the input data, so it is
#    deterministic too.)
# 4. out/supplement/S1 and S2 must equal data/supplement/ byte for byte; S3 apart from its "Generated <date>".
# 5. Every PRISMA box must sum and no record may be pending (tests/check_prisma_sums.py).
# 6. Optional references (for example the article's counts.tex) are compared with the regenerated files; only the
#    generator path and the generation stamp are normalised (see tests/compare_outputs.py).
# Exit status 0 only if every check passes.
set -euo pipefail
repo="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ref_tex=""; ref_json=""; ref_csv=""
while [ $# -gt 0 ]; do
  case "$1" in
    --ref-tex)  ref_tex="$(realpath "$2")";  shift 2 ;;
    --ref-json) ref_json="$(realpath "$2")"; shift 2 ;;
    --ref-csv)  ref_csv="$(realpath "$2")";  shift 2 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT
git clone --quiet "$repo" "$work/clone"
cd "$work/clone"
echo "testing commit $(git rev-parse --short HEAD) in a fresh clone"
fail=0
make --no-print-directory counts supplement > "$work/make.log" 2>&1 || { cat "$work/make.log"; echo "FAIL make"; exit 1; }
if [ -z "$(git status --porcelain -- data docs)" ]; then
  echo "PASS bytes committed data/ and docs/ reproduced by make counts"
else
  echo "FAIL bytes make counts changed committed files:"; git status --short -- data docs; fail=1
fi
for f in S1_screening_ledger.csv S2_noOA_reassessment.csv; do
  python3 -I tests/compare_outputs.py bytes "out/supplement/$f" "data/supplement/$f" || fail=1
done
python3 -I tests/compare_outputs.py s3 out/supplement/S3_search_strategies.md data/supplement/S3_search_strategies.md || fail=1
if python3 -I tests/check_prisma_sums.py > "$work/sums.log"; then
  echo "PASS sums  every PRISMA box sums; $(tail -1 "$work/sums.log")"
else
  grep -v '^OK' "$work/sums.log"; echo "FAIL sums  see above"; fail=1
fi
if [ -n "$ref_tex" ];  then python3 -I tests/compare_outputs.py tex   data/counts.tex          "$ref_tex"  || fail=1; fi
if [ -n "$ref_json" ]; then python3 -I tests/compare_outputs.py json  data/prisma_counts.json  "$ref_json" || fail=1; fi
if [ -n "$ref_csv" ];  then python3 -I tests/compare_outputs.py bytes data/screening_master.csv "$ref_csv" || fail=1; fi
if [ "$fail" -eq 0 ]; then echo "ALL CHECKS PASSED"; else echo "SOME CHECKS FAILED"; fi
exit "$fail"
