"""
extract_dates.py
----------------
Scans the directory where this script lives, extracts a date from each
filename, then MOVES every file into a sub-folder named "DD Month"
(e.g. "15 March", "3 June").

Files whose date cannot be determined are moved into "_unmatched".
Sub-folders are created automatically if they don't already exist.

Usage:
    python extract_dates.py
"""

import re
import os
import shutil
from datetime import datetime, date
from typing import Optional

# pip install python-dateutil
from dateutil import parser as dateutil_parser

UNMATCHED_FOLDER = "_unmatched"

# ---------------------------------------------------------------------------
# Month name → number mapping
# ---------------------------------------------------------------------------
MONTH_NAMES: dict[str, int] = {
    "january": 1,  "jan": 1,
    "february": 2, "feb": 2,
    "march": 3,    "mar": 3,
    "april": 4,    "apr": 4,
    "may": 5,
    "june": 6,     "jun": 6,
    "july": 7,     "jul": 7,
    "august": 8,   "aug": 8,
    "september": 9,"sep": 9,
    "october": 10, "oct": 10,
    "november": 11,"nov": 11,
    "december": 12,"dec": 12,
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _make_date(year: int, month: int, day: int) -> Optional[date]:
    try:
        return date(year, month, day)
    except ValueError:
        return None


def folder_name(d: date) -> str:
    """Format a date as 'DD Month', e.g. '15 March', '3 June'."""
    return f"{d.day} {d.strftime('%B')}"


def extract_date_from_filename(filename: str) -> Optional[date]:
    """
    Try multiple regex strategies in order of specificity.
    Returns a date object on success, None on failure.
    """
    name = re.sub(r'\.[a-zA-Z0-9]{2,5}$', '', filename).lower()

    # Strategy 1 — ISO 8601: 2024-03-15 / 2024_03_15
    m = re.search(r'(\d{4})[-_.](\d{2})[-_.](\d{2})', name)
    if m:
        return _make_date(int(m[1]), int(m[2]), int(m[3]))

   
    # Strategy 7 — dateutil fuzzy fallback
    try:
        cleaned = re.sub(r'[-_]', ' ', name)
        parsed = dateutil_parser.parse(cleaned, fuzzy=True)
        if 1970 <= parsed.year <= 2100:
            return parsed.date()
    except (ValueError, OverflowError):
        pass

    return None


def move_file(src: str, dest_dir: str, filename: str) -> str:
    """
    Move src into dest_dir/filename.
    If a file with the same name already exists in dest_dir, append a
    counter suffix to avoid silent overwrites: file(1).pdf, file(2).pdf …
    Returns the final destination path.
    """
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, filename)

    if os.path.exists(dest):
        base, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(dest):
            dest = os.path.join(dest_dir, f"{base}({counter}){ext}")
            counter += 1

    shutil.move(src, dest)
    return dest


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    script_dir  = os.path.dirname(os.path.abspath(__file__))
    script_name = os.path.basename(__file__)

    # Collect files only — skip this script, sub-folders, and _unmatched
    entries = [
        f for f in os.listdir(script_dir)
        if os.path.isfile(os.path.join(script_dir, f))
        and f != script_name
    ]

    if not entries:
        print("No files found in the script's directory.")
        return

    moved:    list[tuple[str, str]] = []   # (filename, destination folder)
    unmatched: list[str]            = []

    for filename in sorted(entries, key=str.lower):
        src = os.path.join(script_dir, filename)
        extracted = extract_date_from_filename(filename)

        if extracted:
            target_folder = os.path.join(script_dir, folder_name(extracted))
            move_file(src, target_folder, filename)
            moved.append((filename, folder_name(extracted)))
        else:
            target_folder = os.path.join(script_dir, UNMATCHED_FOLDER)
            #move_file(src, target_folder, filename)
            unmatched.append(filename)

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    col_w = max((len(f) for f, _ in moved), default=20) + 2 if moved else 40

    print("=" * (col_w + 22))
    print(f"  Directory : {script_dir}")
    print(f"  Processed : {len(entries)} file(s)")
    print("=" * (col_w + 22))

    if moved:
        print(f"\n  {'FILE':<{col_w}}  MOVED TO")
        print(f"  {'─' * col_w}  {'─' * 16}")
        for filename, folder in moved:
            print(f"  {filename:<{col_w}}  {folder}/")

    if unmatched:
        print(f"\n  ⚠  {len(unmatched)} file(s) with no recognisable date → '{UNMATCHED_FOLDER}/'")
        print(f"  {'─' * 44}")
        for filename in unmatched:
            print(f"     {filename}")

    print()


if __name__ == "__main__":
    main()