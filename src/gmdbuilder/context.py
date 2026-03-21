from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from typing import TYPE_CHECKING, Any, Callable, Generator, TypeVar

from gmdbuilder.fields import key_is_allowed
from gmdbuilder.mappings import obj_prop

from .object_types import ObjectType

if TYPE_CHECKING:
    from .level import Level

Transform = Callable[[ObjectType], None]

NoGen = Generator[None, None, None]

# ---------------------------------------------------------------------------
# Context state
# ---------------------------------------------------------------------------

T = TypeVar("T")


class _ContextState:
    """Central namespace for all of gmdbuilder's active build state."""

    level: ContextVar[Level | None] = ContextVar('gmdbuilder.level', default=None)
    
    autoappend: ContextVar[bool] = ContextVar('gmdbuilder.autoappend', default=False)
    operations: ContextVar[tuple[Transform, ...]] = ContextVar('gmdbuilder.operations', default=())
    """
    Ordered tuple of transform functions applied to every new object.
    Each entry is a closure added by a context manager (groups, targets, set_prop, etc.).
    """

    fn_group: ContextVar[int | None] = ContextVar('gmdbuilder.fn_group', default=None)
    """The active trigger function group ID."""

    x_cursor: ContextVar[float] = ContextVar('gmdbuilder.x_cursor', default=0.0)
    """
    Current X position for trigger placement within a trigger function scope.
    Managed by trigger_fn's build mechanism and by wait():
      - Regular mode: advanced by 1.3 units per object created (via a pushed operation).
      - Spawn-ordered mode: advanced by t * 311.58 units per wait(t) call.
    Reset to 0 when entering an order() scope or when trigger_fn starts a build.
    """

    spawn_ordered: ContextVar[bool] = ContextVar('gmdbuilder.spawn_ordered', default=False)
    """
    Whether wait() advances the X cursor (True) or creates a spawn-trigger chain (False).
    Set by order() or by @trigger_fn(spawn_ordered=True).
    """


ctx = _ContextState()
"""Singleton access point for all active gmdbuilder build state."""


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _push_op(fn: Transform) -> None:
    ctx.operations.set(ctx.operations.get() + (fn,))

def _pop_op() -> None:
    ctx.operations.set(ctx.operations.get()[:-1])


def _operation_context(fn: Transform) -> NoGen:
    """Raw generator helper: push fn onto the operations tuple, yield, then pop."""
    _push_op(fn)
    try:
        yield
    finally:
        _pop_op()


# ---------------------------------------------------------------------------
# Object creation hook
# ---------------------------------------------------------------------------

def post_object_creation(obj: ObjectType) -> None:
    """
    Called on every new object (new_obj, from_object_string, wrapper constructors).
    Applies all active context state to the object in a defined order:

      1. operations  — all active transform closures: groups, targets, set_prop,
                       and any operations pushed by trigger_fn at build time
                       (fn_group assignment, x-cursor advance, etc.)
      2. autoappend  — append to the active level after all mutations are done

    trigger_fn drives fn_group assignment and x-cursor positioning by pushing
    the appropriate operations before running the body, via the captured
    definition-time context. This function has no special knowledge of those
    concerns — it only sees the operations tuple.
    """
    for fn in ctx.operations.get():
        fn(obj)

    if ctx.autoappend.get():
        lvl = ctx.level.get()
        if lvl is None:
            raise RuntimeError(
                "autoappend is active but there is no active level_context(). "
                "This should not happen — please file a bug report."
            )
        lvl.objects.append(obj)


# ---------------------------------------------------------------------------
# Context managers
# ---------------------------------------------------------------------------

@contextmanager
def level_context(level: Level, autoappend: bool = True) -> NoGen:
    """
    Sets the active level for the current scope.

    autoappend (default True): newly created objects are automatically appended
    to the level. Pass False when loading or reading a level without intending
    to add objects in the current scope.

    Nested level_context calls are supported — the inner context takes full
    control for its duration, and the outer level is restored on exit.
    """
    old_level = ctx.level.get()
    old_autoappend = ctx.autoappend.get()
    ctx.level.set(level)
    ctx.autoappend.set(autoappend)
    try:
        yield
    finally:
        ctx.level.set(old_level)
        ctx.autoappend.set(old_autoappend)


@contextmanager
def autoappend() -> NoGen:
    """
    Enables auto-append for a narrower scope within an already-active level_context.
    Useful when level_context was opened with autoappend=False and you need
    auto-append behaviour for a specific block.
    """
    if ctx.level.get() is None:
        raise RuntimeError("autoappend() requires an active level_context()")
    old = ctx.autoappend.get()
    ctx.autoappend.set(True)
    try:
        yield
    finally:
        ctx.autoappend.set(old)


@contextmanager
def transform(fn: Transform) -> NoGen:
    """Applies fn(obj) to every newly created object within this scope."""
    yield from _operation_context(fn)


@contextmanager
def set_prop(key: str, value: Any) -> NoGen:
    """Automatically sets a specific property on every newly created object."""
    def _apply(obj: ObjectType) -> None:
        if key_is_allowed(obj[obj_prop.ID], key):
            obj[key] = value  # type: ignore[literal-required]
    yield from _operation_context(_apply)


@contextmanager
def groups(*group_ids: int) -> NoGen:
    """
    Additively adds group IDs to every newly created object within this scope.
    Crosses trigger function scope boundaries — intended for cross-cutting group
    membership such as editor selection groups or debug groups.
    For trigger function grouping, trigger_fn handles group assignment via fn_group.
    """
    def _apply(obj: ObjectType) -> None:
        g = set(obj.get(obj_prop.GROUPS, set()))
        g.update(group_ids)
        obj[obj_prop.GROUPS] = g
    yield from _operation_context(_apply)


@contextmanager
def targets(target: int, target_2: int | None = None) -> NoGen:
    """
    Sets the target group (a51) and optional secondary target (a71)
    on every newly created trigger within this scope.
    """
    def _apply(obj: ObjectType) -> None:
        if key_is_allowed(obj[obj_prop.ID], "a51"):
            obj["a51"] = target  # type: ignore[literal-required]
        if target_2 is not None and key_is_allowed(obj[obj_prop.ID], "a71"):
            obj["a71"] = target_2  # type: ignore[literal-required]
    yield from _operation_context(_apply)


@contextmanager
def order(spawn_ordered: bool = True) -> NoGen:
    """
    Sets the trigger ordering mode for this scope and resets the X cursor to 0.

    spawn_ordered=True:
        wait(t) advances the X cursor by t * 311.58 units. All triggers in the
        same group are sequenced by X position. No extra groups or spawn triggers
        are needed for timing, but timing is baked in at build time.

    spawn_ordered=False (default when not in any order() scope):
        wait(t) allocates a new group chained via a spawn trigger with the given
        delay. Triggers within each group are auto-spaced by X += 1.3 to
        guarantee sub-tick execution order without relying on object-list position.

    Entering order() always resets the X cursor to 0 so the sequence starts clean.
    The previous cursor position is restored on exit.
    """
    old_ordered = ctx.spawn_ordered.get()
    old_cursor = ctx.x_cursor.get()
    ctx.spawn_ordered.set(spawn_ordered)
    ctx.x_cursor.set(0.0)
    try:
        yield
    finally:
        ctx.spawn_ordered.set(old_ordered)
        ctx.x_cursor.set(old_cursor)