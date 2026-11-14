# Reproduce the review's counts and supplement from the data in this repository.
# Requirements: Python 3 (standard library only), GNU make, git (for `make test`).
PYTHON ?= python3

.PHONY: all counts supplement check missing test clean

all: counts supplement

# data/screening_master.csv, data/prisma_counts.json, data/counts.tex and docs/prisma_flow.md
counts:
	$(PYTHON) -I pipeline/make_counts.py
	$(PYTHON) -I pipeline/prisma_flow.py

# out/supplement/S1-S3, which tests/test_reproduce.sh compares with data/supplement/
supplement: counts
	$(PYTHON) -I pipeline/build_supplement.py

# every box of the PRISMA flow must sum, and no record may be left pending
check: counts
	$(PYTHON) -I tests/check_prisma_sums.py

# out/missing_fulltexts.{csv,md}: the records whose full text was not obtained
missing:
	$(PYTHON) -I pipeline/missing_fulltexts.py

# fresh clone -> make counts supplement -> byte-for-byte comparison with the committed files
test:
	bash tests/test_reproduce.sh

clean:
	rm -rf out
