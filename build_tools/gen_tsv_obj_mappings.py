#!/usr/bin/env python3
"""
Step 2: Generate/refresh a TSV type map from a nested Enum python file.

Usage:
  python gen_type_map_tsv.py path/to/enums.py path/to/types.tsv

TSV columns:
  key<TAB>type<TAB>labels

Rules:
- Regenerates key + labels every run (from enums.py).
- Preserves the 'type' cell for existing keys in the TSV.
- Keys are the *int* values found in enum member assignments (NAME = 123).
- Labels are aggregated across the entire enum file, counting how often each NAME appears for that key.
- Non-int enum values are skipped (warned to stderr).
"""

from __future__ import annotations

import argparse
import ast
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, Tuple


def read_existing_types(tsv_path: Path) -> Dict[str, str]:
    if not tsv_path.exists():
        return {}

    types: Dict[str, str] = {}
    text = tsv_path.read_text(encoding="utf-8", errors="replace")
    for i, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) < 2:
            continue

        key = parts[0].strip()
        typ = parts[1].strip()

        # Skip header-ish rows
        if i == 1 and key.lower() in {"key", "id", "number"}:
            continue
        if not key.isdigit():
            continue

        types[key] = typ

    return types


def is_enum_subclass(classdef: ast.ClassDef) -> bool:
    for b in classdef.bases:
        if isinstance(b, ast.Name) and b.id == "Enum":
            return True
        if isinstance(b, ast.Attribute) and b.attr == "Enum":
            return True
    return False


def iter_enum_members(tree: ast.AST) -> Iterable[Tuple[str, int]]:
    """
    Yields (member_name, member_int_value) for all Assign/AnnAssign inside Enum subclasses,
    including nested Enum subclasses.
    """

    def walk_class(cls: ast.ClassDef, inside_enum: bool) -> Iterable[Tuple[str, int]]:
        here_is_enum = inside_enum or is_enum_subclass(cls)

        for node in cls.body:
            if isinstance(node, ast.ClassDef):
                # BUGFIX: must recurse with `yield from`
                yield from walk_class(node, here_is_enum)
                continue

            if not here_is_enum:
                continue

            # NAME = <value>
            if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                name = node.targets[0].id
                val = node.value
                if isinstance(val, ast.Constant) and isinstance(val.value, int):
                    yield (name, val.value)
                else:
                    try:
                        vsrc = ast.unparse(val)  # py3.9+
                    except Exception:
                        vsrc = "<non-int>"
                    print(f"[warn] skipping non-int enum value: {name} = {vsrc}", file=sys.stderr)

            # NAME: T = <value>
            if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.value is not None:
                name = node.target.id
                val = node.value
                if isinstance(val, ast.Constant) and isinstance(val.value, int):
                    yield (name, val.value)
                else:
                    try:
                        vsrc = ast.unparse(val)
                    except Exception:
                        vsrc = "<non-int>"
                    print(f"[warn] skipping non-int enum value: {name} = {vsrc}", file=sys.stderr)

    for node in getattr(tree, "body", []):
        if isinstance(node, ast.ClassDef):
            yield from walk_class(node, inside_enum=False)


def build_label_counts(enums_py: Path) -> Dict[str, Counter]:
    src = enums_py.read_text(encoding="utf-8", errors="replace")
    tree = ast.parse(src)

    counts: Dict[str, Counter] = defaultdict(Counter)
    for label, key in iter_enum_members(tree):
        counts[str(key)][label] += 1
    return counts


def format_labels(counter: Counter) -> str:
    items = sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))
    return ", ".join(f"{name}({n})" for name, n in items)


def write_tsv(out_path: Path, rows: Iterable[Tuple[str, str, str]], include_header: bool) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    if include_header:
        lines.append("key\ttype\tlabels")
    for k, t, labels in rows:
        lines.append(f"{k}\t{t}\t{labels}")
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("enums_py", type=Path)
    ap.add_argument("out_tsv", type=Path)
    ap.add_argument("--no-header", action="store_true")
    args = ap.parse_args()

    if not args.enums_py.exists() or not args.enums_py.is_file():
        raise SystemExit(f"enums_py does not exist or is not a file: {args.enums_py}")

    existing_types = read_existing_types(args.out_tsv)
    label_counts = build_label_counts(args.enums_py)

    def key_sort(k: str) -> int:
        return int(k) if k.isdigit() else 10**18

    rows = []
    for key in sorted(label_counts.keys(), key=key_sort):
        typ = existing_types.get(key, "")
        labels = format_labels(label_counts[key])
        rows.append((key, typ, labels))

    write_tsv(args.out_tsv, rows, include_header=not args.no_header)

    # Print a helpful summary (so it doesn't feel like "nothing happened")
    print(f"Wrote {args.out_tsv} with {len(rows)} keys (preserved {sum(1 for k,_,_ in rows if existing_types.get(k,''))} types).")


if __name__ == "__main__":
    main()
