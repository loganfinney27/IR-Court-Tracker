# IR-Court-Tracker

**Owner:** Logan Finney — journalist, producer/reporter, Idaho Reports / Idaho Public Television
**Repository:** github.com/loganfinney27/IR-Court-Tracker
**Organization destination:** LAF-US/LAF-PUBLIC (flat merge)

---

## Overview

IR-Court-Tracker is an automated Python scraper that monitors Idaho-related federal court cases via [CourtListener](https://www.courtlistener.com). It tracks case dockets, capturing the original filing date and the most recent docket entry for each case, then writes the results to `output.csv` for use in reporting.

A GitHub Actions workflow runs the scraper daily and commits updated output files back to the repository.

---

## How It Works

1. **`case_urls.csv`** — Input file listing cases to track (topic, CourtListener docket URL, tag/detail).
2. **`main.py`** — Entry point. Loads cases, parses each docket page, writes results.
3. **`scraper/`** — Module containing:
   - `urls.py` — Loads `case_urls.csv`
   - `fetch.py` — HTTP fetching with retry logic, 202-cooldown caching, and jitter delays
   - `parser.py` — Parses CourtListener docket pages (case title, court, first/latest entry dates and links)
   - `pipeline.py` — Merges new scraped rows with existing `output.csv`, preserving prior data when new values are unavailable
   - `failures.py` — Logs failed URLs to `failed_urls.csv`
   - `commit.py` — Commits and pushes updated output files via GitPython
4. **`output.csv`** — Output file with HTML-linked case data for embedding in reporting tools.
5. **`failed_urls.csv`** — Log of URLs that could not be fetched.

---

## Running Locally

```bash
pip install -r requirements.txt
python main.py
```

---

## LAF-US Organization

This repository is part of Logan Finney's project ecosystem and is slated for migration into the **LAF-US** GitHub Organization as `LAF-US/LAF-PUBLIC`. All files will be merged flat into the root of `LAF-PUBLIC` — no internal subdirectories.

Governance for the broader swarm is maintained in the [IDAHO-VAULT](https://github.com/loganfinney27/IDAHO-VAULT). See `AGENTS.md` in this repository for agent orientation.