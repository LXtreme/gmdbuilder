from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from typing import TYPE_CHECKING, Any, Callable, Generator

from gmdbuilder.classes import Spawn
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
    """
    Raw generator helper: push fn, yield control to the caller's @contextmanager
    frame via 'yield from', then pop on exit.  Never call this directly as a
    context manager — always delegate from a @contextmanager-decorated function.
    """
    _push_operation(fn)
    try:
        yield
    finally:
        _pop_operation()


@contextmanager
def level_context(level: Level) -> NoGen:
    """Required by utilities that need level reference (e.g. autoappend)."""
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
        groups = set(obj.get(obj_prop.GROUPS, set()))
        groups.update(group_ids)
        obj[obj_prop.GROUPS] = groups
    
    yield from _operation_context(_add_groups)


@contextmanager
def targets(target: int, target_2: int | None = None) -> NoGen:
    """Automatically set target property 'a51' and secondary target 'a71' on trigger creation."""
    def _set_target(obj: ObjectType) -> None:
        if key_is_allowed(obj[obj_prop.ID], "a51") and target:
            obj["a51"] = target  # type: ignore[literal-required]
        if key_is_allowed(obj[obj_prop.ID], "a71") and target_2:
            obj["a71"] = target_2  # type: ignore[literal-required]
    
    yield from _operation_context(_set_target)


@trigger_fn(spawn_ordered=True, params=[1,2], group=4)
def func():
    a = Move()
    a.move_x = 10
    a.duration = 0.5
    wait(0.5)
    # adds 0.5 * 311.58 (player speed for spawn-ordered mode)
    # to x position for all created triggers after this
    b = Move()
    b.move_x = -10
    b.duration = 0.5


@trigger_fn(params=[1,2], group=4)
def func2():
    a = Move()
    a.move_x = 10
    a.duration = 0.5
    b = Move() # adds 2 to the X position (guarentees order of execution)
    wait(0.5)
    # creates spawn trigger for previous group, the following created triggers are under new group
    c = Move()
    c.move_x = -10
    c.duration = 0.5
    func.call()
    

@contextmanager
def delay(seconds: float = 0.0) -> NoGen:
    """Creates a spawn trigger that spawns newly created triggers after a delay"""
    lvl = _levels.get()
    if not lvl:
        raise RuntimeError("delay() requires an active level_context()")
    
    g = lvl[-1].new.group()
    def _set_delay_group(obj: ObjectType) -> None:
        groups = set(obj.get(obj_prop.GROUPS, set()))
        groups.add(g)
        obj[obj_prop.GROUPS] = groups
    
    _push_operation(_set_delay_group)
    try:
        yield
    finally:
        _pop_operation()
        spawn = Spawn()
        spawn.target_id = g
        spawn.delay = seconds
        lvl[-1].objects.append(spawn.obj)
