from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from typing import TYPE_CHECKING, Any, Callable, Generator

from gmdbuilder.fields import key_is_allowed
from gmdbuilder.mappings import obj_prop

from .object_types import ObjectType

if TYPE_CHECKING:
    from .level import Level

Transform = Callable[[ObjectType], None]

NoGen = Generator[None, None, None]

# ---------------------------------------------------------------------------
# ContextVar Management
# ---------------------------------------------------------------------------

_operations: ContextVar[list[Transform]] = ContextVar('_operations', default=[])

_levels: ContextVar[list[Level]] = ContextVar('_levels', default=[])


def _push_operation(fn: Transform) -> None:
    current = _operations.get()
    _operations.set(current + [fn])


def _pop_operation() -> None:
    current = _operations.get()
    assert current
    _operations.set(current[:-1])


def _push_level(level: Level) -> None:
    current = _levels.get()
    _levels.set(current + [level])


def _pop_level() -> None:
    current = _levels.get()
    assert current
    _levels.set(current[:-1])


# ---------------------------------------------------------------------------
# Public helpers
# ---------------------------------------------------------------------------

def post_object_creation(obj: ObjectType) -> None:
    """
    Called internally on every new object creation (new_obj, from_object_string).
    Runs all active context operations against the object in registration order.
    """
    for fn in _operations.get():
        fn(obj)



# ---------------------------------------------------------------------------
# Context managers
# ---------------------------------------------------------------------------

def _operation_context(fn: Transform) -> NoGen:
    """Shared push/yield/pop body. Use via transform() or as a building block."""
    _push_operation(fn)
    try:
        yield
    finally:
        _pop_operation()


@contextmanager
def level_context(level: Level) -> NoGen:
    """Required by utilities that need level refence (e.g. autoappend)."""
    _push_level(level)
    try:
        yield
    finally:
        _pop_level()


@contextmanager
def autoappend() -> NoGen:
    """Requires active level_context. Automatically appends newly created objects."""
    lvl = _levels.get()
    if not lvl:
        raise RuntimeError("autoappend() requires an active level_context()")
    
    yield from _operation_context(lambda obj: lvl[-1].objects.append(obj))


@contextmanager
def transform(fn: Transform) -> NoGen:
    """
    Applies `fn(obj)` to every newly created object.
    `fn` receives the object and mutates it in place.
    """
    yield from _operation_context(fn)



@contextmanager
def set_prop(key: str, value: Any) -> NoGen:
    """Automatically set a specific property on every newly created object."""
    def _set_property(obj: ObjectType) -> None:
        if key_is_allowed(obj[obj_prop.ID], key):
            obj[key] = value  # type: ignore[literal-required]
    
    yield from _operation_context(_set_property)


@contextmanager
def groups(*group_ids: int) -> NoGen:
    """Adds one or more group IDs to every newly created object."""
    def _add_groups(obj: ObjectType) -> None:
        existing = obj.get(obj_prop.GROUPS)
        current: set[int] = existing if existing is not None else set()
        current.update(group_ids)
        obj[obj_prop.GROUPS] = current
    
    yield from _operation_context(_add_groups)


@contextmanager
def target(target: int, target_2: int | None = None) -> NoGen:
    """Automatically set target property 'a51' and secondary target 'a71' on trigger creation."""
    def _set_target(obj: ObjectType) -> None:
        if key_is_allowed(obj[obj_prop.ID], "a51") and target:
            obj["a51"] = target  # type: ignore[literal-required]
        if key_is_allowed(obj[obj_prop.ID], "a71") and target_2:
            obj["a71"] = target_2  # type: ignore[literal-required]
    
    yield from _operation_context(_set_target)
