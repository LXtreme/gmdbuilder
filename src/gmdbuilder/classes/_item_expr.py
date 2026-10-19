"""
Expression parsing helpers for ItemEdit / ItemCompare.

Operands (case-insensitive):
    i<ID>  item        t<ID>  timer
    p      points      m      main time (platformer)      a      attempts

Sign functions:  abs(x), neg(x)
Rounding:        round(x), floor(x), ceil(x)
Sign is applied AFTER rounding, so write abs(floor(x)), never floor(abs(x)).

Sources for the allowed operations:
    HDanke's GD Editor Docs (Item Edit / Item Compare), the GD wiki, and
    FlowVix's gd-info-explorer property table (props 476-486, 578, 579).
"""

import re
from dataclasses import dataclass

from gmdbuilder.mappings.obj_enum import Item

MAX_ID = 9999

_O = r"(?:i\d+|t\d+|p|m|a)"
_N = r"-?(?:\d+\.?\d*|\.\d+)"

_SIGN_FUNCS = {"abs": Item.SignOp.ABSOLUTE, "neg": Item.SignOp.NEGATIVE}
_ROUND_FUNCS = {"round": Item.RoundOp.ROUND, "floor": Item.RoundOp.FLOOR, "ceil": Item.RoundOp.CEILING}
_MATH_OPS = {
    "+": Item.MathOp.ADD,
    "-": Item.MathOp.SUBTRACT,
    "*": Item.MathOp.MULTIPLY,
    "/": Item.MathOp.DIVIDE,
}
_ASSIGN_OPS = {
    "=": Item.MathOp.ASSIGN,
    "+=": Item.MathOp.ADD,
    "-=": Item.MathOp.SUBTRACT,
    "*=": Item.MathOp.MULTIPLY,
    "/=": Item.MathOp.DIVIDE,
}
COMPARE_OPS = {
    "==": Item.CompareOp.EQ,
    ">": Item.CompareOp.GT,
    ">=": Item.CompareOp.GTE,
    "<": Item.CompareOp.LT,
    "<=": Item.CompareOp.LTE,
    "!=": Item.CompareOp.NE,
}


@dataclass
class Operand:
    type: Item.ItemType
    id: int = 0


NONE_OPERAND = Operand(Item.ItemType.DEFAULT, 0)


@dataclass
class Funcs:
    sign: Item.SignOp = Item.SignOp.NONE
    round: Item.RoundOp = Item.RoundOp.NONE


def clean(expr: str) -> str:
    if not expr.strip():
        raise ValueError("Expression must be a non-empty string")
    return re.sub(r"\s+", "", expr).lower()


def parse_operand(tok: str) -> Operand:
    kind = tok[0]
    if kind in "pma":
        return Operand({"p": Item.ItemType.POINTS, "m": Item.ItemType.MAINTIME, "a": Item.ItemType.ATTEMPTS}[kind])
    num = int(tok[1:])
    if not 1 <= num <= MAX_ID:
        raise ValueError(f"Item/timer ID must be between 1 and {MAX_ID}, got {num} in '{tok}'")
    return Operand(Item.ItemType.ITEM if kind == "i" else Item.ItemType.TIMER, num)


def _unwrap(s: str, names: dict[str, int]) -> tuple[int | None, str]:
    m = re.match(r"(\w+)\(", s)
    if not m or m.group(1) not in names:
        return None, s
    depth = 0
    for i in range(m.end() - 1, len(s)):
        if s[i] == "(":
            depth += 1
        elif s[i] == ")":
            depth -= 1
            if depth == 0:
                if i == len(s) - 1:
                    return names[m.group(1)], s[m.end():i]
                return None, s
    raise ValueError(f"Unbalanced parentheses in '{s}'")


def strip_funcs(s: str) -> tuple[Funcs, str]:
    """Peel an optional sign(...) then an optional round(...) off the outside of s."""
    f = Funcs()
    sign, s = _unwrap(s, _SIGN_FUNCS)
    if sign is not None:
        f.sign = sign
    rnd, s = _unwrap(s, _ROUND_FUNCS)
    if rnd is not None:
        f.round = rnd
    if re.match(r"(abs|neg|round|floor|ceil)\(", s):
        raise ValueError(
            "Sign/rounding functions must wrap a whole side, at most one of each, "
            "with sign outermost (rounding happens before sign): e.g. abs(floor(...))"
        )
    return f, s


def parse_number(tok: str) -> float:
    return float(tok)


def check_divisor(op: Item.MathOp, mod: float) -> None:
    if op == Item.MathOp.DIVIDE and mod == 0:
        raise ValueError("Cannot divide by a mod of 0")


# ----------------------------------------------------------------------
# Item Edit
# ----------------------------------------------------------------------

@dataclass
class EditSpec:
    target: Operand
    assign_op: Item.MathOp
    item_1: Operand
    item_2: Operand
    param_op: Item.MathOp
    mod_op: Item.MathOp
    mod: float
    mod_funcs: Funcs  # applied to the mod result (button group 1)
    out_funcs: Funcs  # applied to the assignment result (button group 2)


def parse_edit(expr: str) -> EditSpec:
    s = clean(expr)
    out_funcs, s = strip_funcs(s)

    m = re.fullmatch(r"(i\d+|t\d+|p)(\+=|-=|\*=|/=|=)(.+)", s)
    if not m:
        raise ValueError(
            f"Could not parse Item Edit '{expr}'. Expected '<target> <assign> <expression>' "
            "where target is i<ID>, t<ID> or p and assign is one of = += -= *= /= "
            "(maintime and attempts cannot be written to)"
        )
    target = parse_operand(m.group(1))
    assign_op = _ASSIGN_OPS[m.group(2)]
    mod_funcs, rhs = strip_funcs(m.group(3))

    item_1: Operand
    item_2 = NONE_OPERAND
    param_op = Item.MathOp.ADD
    mod_op = Item.MathOp.MULTIPLY
    mod = 1.0

    if m2 := re.fullmatch(rf"({_O})(?:([+\-*/])({_O}))?", rhs):
        item_1 = parse_operand(m2.group(1))
        if m2.group(2):
            param_op, item_2 = _MATH_OPS[m2.group(2)], parse_operand(m2.group(3))
    elif m2 := re.fullmatch(rf"\(({_O})(?:([+\-*/])({_O}))?\)([*/])({_N})", rhs):
        item_1 = parse_operand(m2.group(1))
        if m2.group(2):
            param_op, item_2 = _MATH_OPS[m2.group(2)], parse_operand(m2.group(3))
        mod_op, mod = _MATH_OPS[m2.group(4)], parse_number(m2.group(5))
    elif m2 := re.fullmatch(rf"({_O})([*/])({_N})", rhs):
        item_1 = parse_operand(m2.group(1))
        mod_op, mod = _MATH_OPS[m2.group(2)], parse_number(m2.group(3))
    elif m2 := re.fullmatch(rf"({_O})([*/])({_O})([*/])({_N})", rhs):
        item_1, item_2 = parse_operand(m2.group(1)), parse_operand(m2.group(3))
        param_op, mod_op, mod = _MATH_OPS[m2.group(2)], _MATH_OPS[m2.group(4)], parse_number(m2.group(5))
    elif re.fullmatch(rf"{_O}[+\-]{_O}[*/]{_N}", rhs):
        raise ValueError(
            f"Ambiguous '{expr}': GD applies Mod to the result of I1 <op> I2, so write "
            "'(i1 + i2) * 3' with parentheses"
        )
    else:
        raise ValueError(
            f"Unsupported Item Edit right-hand side in '{expr}'. Item Edit computes "
            "(I1 [+ - * /] I2) [* /] mod, optionally wrapped in rounding/sign functions. "
            "It cannot add, subtract or assign a constant (Mod only multiplies/divides) "
            "-- use a Pickup trigger for that"
        )

    check_divisor(mod_op, mod)
    return EditSpec(target, assign_op, item_1, item_2, param_op, mod_op, mod, mod_funcs, out_funcs)


# ----------------------------------------------------------------------
# Item Compare
# ----------------------------------------------------------------------

@dataclass
class Side:
    item: Operand
    op: Item.MathOp
    mod: float
    funcs: Funcs


@dataclass
class CompareSpec:
    left: Side
    cmp: Item.CompareOp
    right: Side


def _parse_side(raw: str, full: str) -> Side:
    funcs, s = strip_funcs(raw)
    if m := re.fullmatch(_O, s):
        return Side(parse_operand(m.group(0)), Item.MathOp.MULTIPLY, 1.0, funcs)
    if m := re.fullmatch(rf"({_O})([+\-*/])({_N})", s):
        op, mod = _MATH_OPS[m.group(2)], parse_number(m.group(3))
        check_divisor(op, mod)
        return Side(parse_operand(m.group(1)), op, mod, funcs)
    if re.fullmatch(_N, s):
        return Side(NONE_OPERAND, Item.MathOp.ASSIGN, parse_number(s), funcs)
    if re.fullmatch(rf"{_O}[+\-*/]{_O}", s):
        raise ValueError(
            f"Item Compare has no operation between two items (in '{full}'); each side is "
            "one item with an optional constant: 'i1 + 2', 't3 * 0.5', or just a constant"
        )
    raise ValueError(f"Unsupported Item Compare side '{raw}' in '{full}'")


def parse_compare(expr: str) -> CompareSpec:
    s = clean(expr)
    m = re.fullmatch(r"(.+?)(==|!=|<=|>=|<|>)(.+)", s)
    if not m:
        raise ValueError(
            f"Could not parse Item Compare '{expr}'. Expected '<left> <cmp> <right>' "
            "where cmp is one of == != < <= > >="
        )
    return CompareSpec(_parse_side(m.group(1), expr), COMPARE_OPS[m.group(2)], _parse_side(m.group(3), expr))
