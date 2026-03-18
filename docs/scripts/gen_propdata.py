"""
gen_propdata.py
Converts build_tools/typemap.tsv into docs/propdata.json for the VitePress
property reference page.

TSV columns (tab-separated, first row is a header):
    key     — raw numeric string (e.g. "51") or alphanumeric (e.g. "kA1", "kS38")
    type    — type string (e.g. "int", "float", "bool", "EASING")
    labels  — comma-separated NAME(count) tokens for numeric rows,
              or a single plain NAME for kA/kS rows

Output JSON schema (one object per row, numeric keys first then alpha):
    key     — "a<num>" for numeric keys, raw key otherwise (e.g. "kA1")
    num     — integer for numeric keys, 99999 for non-numeric
    type    — type string from TSV
    names   — list of label strings, ordered by descending count then alpha

Run from the repo root:
    python docs/scripts/gen_propdata.py
"""

import csv
import json
import re
from pathlib import Path

TSV_FILE = Path("build_tools/typemap.tsv")
OUT_FILE  = Path("docs/propdata.json")

_LABEL_RE = re.compile(r'^(.+)\((\d+)\)$')


def parse_names(raw: str) -> list[str]:
    """Parse a labels cell and return names ordered by descending count then alpha.

    Handles both formats:
      - "NAME(count), NAME(count), ..."   (numeric rows)
      - "NAME"                            (plain kA/kS rows)
    """
    pairs: list[tuple[str, int]] = []
    for part in (p.strip() for p in raw.split(',') if p.strip()):
        m = _LABEL_RE.match(part)
        pairs.append((m.group(1), int(m.group(2))) if m else (part, 1))
    pairs.sort(key=lambda x: (-x[1], x[0]))
    return [name for name, _ in pairs]


def sort_key(raw_key: str) -> tuple[int, int | str]:
    """Numeric keys sort before alpha keys; numeric keys sort by int value."""
    return (0, int(raw_key)) if raw_key.isdigit() else (1, raw_key)


def main() -> None:
    rows: list[tuple[str, str, str]] = []  # (raw_key, type_str, labels_raw)

    with TSV_FILE.open(encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        next(reader)  # skip header
        for row in reader:
            if len(row) < 2 or not row[0].strip():
                continue
            raw_key  = row[0].strip()
            type_str = row[1].strip()
            labels   = row[2].strip() if len(row) > 2 else ''
            rows.append((raw_key, type_str, labels))

    rows.sort(key=lambda r: sort_key(r[0]))

    data = [
        {
            'key':   f"a{raw_key}" if raw_key.isdigit() else raw_key,
            'num':   int(raw_key) if raw_key.isdigit() else 99999,
            'type':  type_str,
            'names': parse_names(labels),
        }
        for raw_key, type_str, labels in rows
    ]

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(json.dumps(data, indent=2), encoding='utf-8')

    numeric = sum(1 for e in data if e['num'] != 99999)
    print(f"Wrote {len(data)} entries to {OUT_FILE}  ({numeric} numeric, {len(data) - numeric} alphanumeric)")


if __name__ == '__main__':
    main()
