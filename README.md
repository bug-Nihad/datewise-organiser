# datewise-organiser

A zero-config Python script that scans its own directory, extracts dates from filenames, and moves each file into a sub-folder named **`DD Month`** (e.g. `15 March`, `3 June`).

---

## Features

- Handles many date formats automatically — no configuration needed
- Detects multiple dates in a single filename and picks the first (most relevant) one
- Files with no recognisable date are **left in place** and reported
- Duplicate filenames in the same destination folder are renamed safely (`file(1).pdf`, `file(2).pdf` …)
- Works on Windows, macOS, and Linux

## Supported date formats

| Format | Example filename |
|---|---|
| ISO 8601 | `report_2024-03-15_final.pdf` |
| Compact 8-digit | `backup_20240315_120000.zip` |
| Numeric separators | `photo_03.15.2024.jpg` |
| Named month (short) | `invoice_15Mar2024.docx` |
| Named month (full) | `meeting_notes_March_15_2024.txt` |
| Month + year only | `Q1_sales_Jan-2024.xlsx` → `1 January/` |
| ISO week number | `log_2024_W12.txt` → `18 March/` |
| Fuzzy fallback | anything `python-dateutil` can parse |

## Installation

Requires Python 3.9+ and one dependency:

```bash
pip install python-dateutil
```

## Usage

1. Drop `datewise_organiser.py` into the folder containing your files.
2. Run it:

```bash
python datewise_organiser.py
```

### Example output

```
  [multi-date] 'compare_2024-01-01_vs_2024-06-30.csv' has 2 ISO dates → using first

  ====================================================================
  Directory : /path/to/your/folder
  Processed : 10 file(s)
  ====================================================================

  FILE                                    MOVED TO            STRATEGY
  ──────────────────────────────────────  ──────────────────  ────────────────────
  backup_20240610_120000.zip              10 June/            compact YYYYMMDD
  compare_2024-01-01_vs_2024-06-30.csv   1 January/          ISO 8601
  invoice_15Mar2024.docx                  15 March/           named month (mar)
  report_2024-03-15_final.pdf             15 March/           ISO 8601

  ⚠  2 file(s) left in place (no date found):
  ────────────────────────────────────────────
     readme.md  (no date pattern found)
     notes.txt  (no date pattern found)
```

## How it works

The script tries seven strategies in order of specificity, stopping at the first match:

1. **ISO 8601** — `2024-03-15`
2. **Compact 8-digit** — `20240315`
3. **Numeric separators** — `15.03.2024`, `03/15/2024`
4. **Named month** — `15Mar2024`, `March_15_2024`, `Jan-2024`
5. **ISO week** — `2024_W12`
6. **Year + month only** — `2024-03`
7. **`dateutil` fuzzy fallback** — anything the library can parse

## License

MIT
"# datewise-organiser" 
