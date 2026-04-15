from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from typing import TYPE_CHECKING, Any, Callable, Generator

from .mappings import obj_id
from .fields import key_is_allowed
from .mappings import obj_prop
from .object_types import ObjectType, SpawnType

if TYPE_CHECKING:
    from .level import Level

Transform = Callable[[ObjectType], None]

NoGen = Generator[None, None, None]

# ---------------------------------------------------------------------------
# Context state
# ---------------------------------------------------------------------------

class _ContextState:
    """Central namespace for all of gmdbuilder's active build state."""

    level: ContextVar[Level | None] = ContextVar('gmdbuilder.level', default=None)
    
    autoappend: ContextVar[bool] = ContextVar('gmdbuilder.autoappend', default=False)
    operations: ContextVar[tuple[Transform, ...]] = ContextVar('gmdbuilder.operations', default=())

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

    spawn_ordered: ContextVar[bool | None] = ContextVar('gmdbuilder.spawn_ordered', default=None)
    """
    Whether objects get their X position set from x_cursor (not None), and whether
    x_cursor auto-increments per object (False) or only via wait() calls (True).
    Set to False/True by order() or by TriggerFunction._build. None opts out entirely.
    """


ctx = _ContextState()
"""Singleton access point for all active gmdbuilder build state."""


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def push_op(fn: Transform) -> None:
    """Push a transform operation onto the active operations tuple. Intra-package use only."""
    ctx.operations.set(ctx.operations.get() + (fn,))

def pop_op() -> None:
    """Pop the last transform operation from the active operations tuple. Intra-package use only."""
    ctx.operations.set(ctx.operations.get()[:-1])


def _operation_context(fn: Transform) -> NoGen:
    """Raw generator helper: push fn onto the operations tuple, yield, then pop."""
    push_op(fn)
    try:
        yield
    finally:
        pop_op()


def post_object_creation(obj: ObjectType) -> None:
    """Called on every new object (new_obj, from_object_string, wrapper constructors)."""
    for fn in ctx.operations.get():
        fn(obj)

    fn_group = ctx.fn_group.get()
    if fn_group is not None:
        g = set(obj.get(obj_prop.GROUPS) or set())
        g.add(fn_group)
        obj[obj_prop.GROUPS] = g
    
    ordered = ctx.spawn_ordered.get()
    if ordered is not None:
        x = ctx.x_cursor.get()
        obj[obj_prop.X] = x
        if ordered is False:
            ctx.x_cursor.set(x + 1)
    
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
def level_context(level: Level, autoappend: bool = False) -> NoGen:
    """
    Sets the active level for the current scope.

    autoappend (default False): 
        newly created objects are automatically appended to the level.

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
    """Enables auto-append for a narrower scope within an already-active level_context."""
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
def order(spawn_ordered: bool | None = False) -> NoGen:
    """
    Sets the trigger ordering mode for this scope.
    
        In spawn_ordered=False, created objects auto-increment x_cursor += 1.
        This guarentees trigger ordering but does not affect timing.
        
        In spawn_ordered=True, no auto-increment. wait() advances the X cursor by t * 311.58 units, and triggers are effectively spawned at their X positions in timed sequence.
        
        In spawn_ordered=None, opts out of both for the current scope (as an escape hatch).
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


@contextmanager
def delay(t: float) -> NoGen:
    """
    Creates a new group and a spawn trigger (delay=t) targeting it, then sets all
    objects created within this scope to belong to that new group.

    Requires an active level_context() with autoappend enabled.
    Forces spawn_ordered=False for its scope so that objects inside are
    auto-spaced along the X cursor for guaranteed sub-tick ordering.
    """
    old_cursor = ctx.x_cursor.get()
    old_fn_group = ctx.fn_group.get()
    old_ordered = ctx.spawn_ordered.get()
    
    lvl = ctx.level.get()
    if lvl is None or ctx.autoappend.get() is False:
        raise RuntimeError("delay() requires an active level_context() with autoappend enabled.")

    new_group = lvl.new.group()
    spawn: SpawnType = {
        obj_prop.ID: obj_id.Trigger.SPAWN,
        obj_prop.X: 0.0,
        obj_prop.Y: 0.0,
        obj_prop.Trigger.INTERACTIBLE: True,
        obj_prop.Trigger.Spawn.TARGET_ID: new_group,
        obj_prop.Trigger.Spawn.DELAY: t,
    }
    post_object_creation(spawn)
    
    ctx.fn_group.set(new_group)
    ctx.spawn_ordered.set(False)
    ctx.x_cursor.set(0.0)
    try:
        yield
    finally:
        ctx.x_cursor.set(old_cursor)
        ctx.fn_group.set(old_fn_group)
        ctx.spawn_ordered.set(old_ordered)


def wait(t: float = 1/240) -> None:
    """
    Advances the X cursor by t * 311.58 units (player speed in studs/s). 
    This means new triggers created after are placed at the new X position.
    Primarily used in spawn-ordered mode to create a sequence of triggers with specific timing.
    """
    ctx.x_cursor.set(ctx.x_cursor.get() + t * 311.58)

