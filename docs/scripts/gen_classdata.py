"""
gen_classdata.py
Parses all wrapper classes in src/gmdbuilder/classes/ via AST (no imports needed)
and writes docs/classdata.json for the VitePress wrapper class reference page.

Run from the repo root:
    python docs/scripts/gen_classdata.py
"""

import ast
import json
import re
from pathlib import Path
from typing import Any

CLASSES_DIR = Path("src/gmdbuilder/classes")
OUT_FILE    = Path("docs/classdata.json")

_KEY_RE = re.compile(r'\(([a-zA-Z]\d+)\)\s*$')


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_docstring(node: ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    """Return the docstring of a class or function node, or ''."""
    first = node.body[0] if node.body else None
    if (
        isinstance(first, ast.Expr)
        and isinstance(first.value, ast.Constant)
        and isinstance(first.value.value, str)
    ):
        return first.value.value.strip()
    return ""


def following_docstring(body: list[ast.stmt], idx: int) -> str:
    """Return the string literal immediately after body[idx], or ''."""
    if idx + 1 < len(body):
        nxt = body[idx + 1]
        if (
            isinstance(nxt, ast.Expr)
            and isinstance(nxt.value, ast.Constant)
            and isinstance(nxt.value.value, str)
        ):
            return nxt.value.value.strip()
    return ""


def extract_key(doc: str) -> str | None:
    """Pull the trailing (aXXX) prop key out of a property docstring."""
    m = _KEY_RE.search(doc)
    return m.group(1) if m else None


# ---------------------------------------------------------------------------
# Property extraction
# ---------------------------------------------------------------------------

def extract_props(node: ast.ClassDef) -> list[dict[str, str | None]]:
    """Collect ObjField descriptor assignments of the form:
        foo = ObjField[T](key_expr)
        \"\"\"docstring\"\"\"
    """
    props: list[dict[str, str | None]] = []

    for idx, item in enumerate(node.body):
        # Only plain assignments: `foo = ObjField[T](...)`
        if not isinstance(item, ast.Assign):
            continue
        val = item.value
        # Must be a Call whose func is a Subscript (ObjField[T])
        if not (isinstance(val, ast.Call) and isinstance(val.func, ast.Subscript)):
            continue

        type_str = ast.unparse(val.func.slice)
        doc = following_docstring(node.body, idx)

        for target in item.targets:
            if isinstance(target, ast.Name):
                props.append({
                    "name": target.id,
                    "type": type_str,
                    "doc":  doc,
                    "key":  extract_key(doc),
                })

    return props


# ---------------------------------------------------------------------------
# Method extraction
# ---------------------------------------------------------------------------

def build_signature(func: ast.FunctionDef) -> str:
    """Build a human-readable signature string (without 'self')."""
    args = func.args
    all_pos = args.posonlyargs + args.args
    defaults_offset = len(all_pos) - len(args.defaults)
    parts: list[str] = []

    for i, a in enumerate(all_pos):
        if a.arg == "self":
            continue
        part = a.arg
        if a.annotation:
            part += f": {ast.unparse(a.annotation)}"
        di = i - defaults_offset
        if di >= 0:
            part += f" = {ast.unparse(args.defaults[di])}"
        parts.append(part)

    if args.vararg:
        va = f"*{args.vararg.arg}"
        if args.vararg.annotation:
            va += f": {ast.unparse(args.vararg.annotation)}"
        parts.append(va)

    for i, a in enumerate(args.kwonlyargs):
        part = a.arg
        if a.annotation:
            part += f": {ast.unparse(a.annotation)}"
        kd = args.kw_defaults[i]
        if kd is not None:
            part += f" = {ast.unparse(kd)}"
        parts.append(part)

    ret = f" -> {ast.unparse(func.returns)}" if func.returns else ""
    return f"def {func.name}({', '.join(parts)}){ret}"


def extract_methods(node: ast.ClassDef) -> list[dict[str, str]]:
    return [
        {
            "name": item.name,
            "sig":  build_signature(item),
            "doc":  get_docstring(item),
        }
        for item in node.body
        if isinstance(item, ast.FunctionDef) and not item.name.startswith("_")
    ]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_classes() -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []

    for pyfile in sorted(CLASSES_DIR.glob("*.py")):
        if pyfile.name.startswith("_"):
            continue
        tree = ast.parse(pyfile.read_text(encoding="utf-8"))
        # Iterate tree.body directly so we only visit top-level classes and
        # preserve their source order (ast.walk is unordered breadth-first).
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                results.append({
                    "name": node.name,
                    "file": pyfile.name,
                    "doc": get_docstring(node),
                    "bases": [
                        b.attr if isinstance(b, ast.Attribute) else b.id
                        for b in node.bases
                        if isinstance(b, (ast.Attribute, ast.Name))
                    ],
                    "props": extract_props(node),
                    "methods": extract_methods(node),
                })

    return results


if __name__ == "__main__":
    data = parse_classes()
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"Wrote {len(data)} classes to {OUT_FILE}")
    for cls in data:
        print(f"  {cls['name']:30s}  {len(cls['props']):3d} props  {len(cls['methods']):2d} methods")
