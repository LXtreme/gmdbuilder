from __future__ import annotations

from contextvars import copy_context
from typing import TYPE_CHECKING, Callable, overload

from .context import ctx, push_op, pop_op
from .mappings import obj_prop, obj_id
from .object_types import ObjectType

if TYPE_CHECKING:
    from .level import Level

# GD's tick duration in seconds — used as the default wait() delay in regular mode.
_TICK_DELAY: float = 1 / 240

# GD's unit-to-second constant for spawn ordered mode: at 1x speed, 311.58 units = 1 second.
_UNITS_PER_SECOND: float = 311.58


class TriggerFunction:
    """
    A named, reusable trigger function bound to a single group.

    Created by the @trigger_fn decorator. Never instantiated directly.

    The function body runs exactly once per level (the build phase), triggered
    on the first .call() or .group access for that level. Subsequent .call()
    invocations only emit a new spawn trigger targeting the already-built group.

    See trigger-fn.md for full design documentation and usage examples.
    """

    def __init__(
        self,
        body: Callable[[], None],
        *,
        explicit_group: int | None,
        spawn_ordered: bool,
        params: list[int] | None,
    ) -> None:
        self._body = body
        self._explicit_group = explicit_group
        self._spawn_ordered = spawn_ordered
        self._params = list(params) if params is not None else None

        # Snapshot the full ContextVar state at decoration time.
        # At build time, the body runs inside this captured context so that
        # context managers active at definition (groups, transform, etc.) are
        # inherited by the body, while infrastructure vars (level, autoappend,
        # fn_group, x_cursor) are overridden with build-time values.
        self._definition_ctx = copy_context()

        self._built_levels: set[int] = set()   # id(level) for every level built on
        self._group: int | None = explicit_group
        self._objects: list[ObjectType] = []

    # ---------------------------------------------------------------------------
    # Properties
    # ---------------------------------------------------------------------------

    @property
    def group(self) -> int:
        """
        The group ID this trigger function is bound to.

        For explicit group= values: available immediately, no level required.
        For auto-allocated groups: lazily calls level.new.group() on first access.
        Raises RuntimeError if accessed without an active level_context before
        the group has been allocated.
        """
        if self._group is None:
            lvl = ctx.level.get()
            if lvl is None:
                raise RuntimeError(
                    "Cannot auto-allocate a trigger_fn group: no active level_context(). "
                    "Either provide group= explicitly or access .group within a level_context."
                )
            self._group = int(lvl.new.group())
        return self._group

    @property
    def params(self) -> list[int] | None:
        """The required remap key list, or None if params were not specified."""
        return self._params

    @property
    def objects(self) -> list[ObjectType]:
        """
        Every object built into this trigger function, including objects in
        sub-groups created by wait(). Empty before the first .call().
        The list holds live references — mutations are reflected immediately.
        """
        return self._objects

    # ---------------------------------------------------------------------------
    # Build
    # ---------------------------------------------------------------------------

    def _build(self, level: Level) -> None:
        """
        Run the function body exactly once for the given level.
        Must be called with level_context and autoappend active.
        """
        g = self.group  # allocate group ID now, before entering the definition context

        def _run() -> None:
            # Override infrastructure ContextVars with build-time values.
            # ctx.operations is NOT overridden — it inherits from the definition-time
            # snapshot, so transforms/groups active at decoration time carry through.
            ctx.level.set(level)
            ctx.autoappend.set(True)
            ctx.fn_group.set(g)
            ctx.x_cursor.set(0.0)
            ctx.spawn_ordered.set(self._spawn_ordered)

            # Push three build-time operations onto the (inherited) operations tuple.
            # They read ContextVar state dynamically so they stay correct after
            # wait() switches ctx.fn_group and ctx.x_cursor to a new sub-group.

            def _stamp_group(obj: ObjectType) -> None:
                # Add the active fn_group to this object's group set.
                # Uses replacement semantics: nested trigger functions set their
                # own fn_group, so this always reads the innermost active group.
                current = ctx.fn_group.get()
                if current is not None:
                    grps = set(obj.get(obj_prop.GROUPS, set()))
                    grps.add(current)
                    obj[obj_prop.GROUPS] = grps

            def _apply_x(obj: ObjectType) -> None:
                # Place the object at the current X cursor position.
                # In regular mode, advance the cursor by 1.3 units per object to
                # guarantee sub-tick execution order without relying on object-list
                # position. In spawn_ordered mode, the cursor is only advanced by
                # explicit wait(t) calls — multiple objects share the same X and
                # fire simultaneously.
                obj[obj_prop.X] = ctx.x_cursor.get()
                if not ctx.spawn_ordered.get():
                    ctx.x_cursor.set(ctx.x_cursor.get() + 1.3)

            def _track(obj: ObjectType) -> None:
                # Record every built object, including sub-group objects from wait().
                self._objects.append(obj)

            push_op(_stamp_group)
            push_op(_apply_x)
            push_op(_track)
            try:
                self._body()
            finally:
                pop_op()  # _track
                pop_op()  # _apply_x
                pop_op()  # _stamp_group

        self._definition_ctx.run(_run)
        self._built_levels.add(id(level))

    # ---------------------------------------------------------------------------
    # Call
    # ---------------------------------------------------------------------------

    def call(
        self,
        delay: float = 0.0,
        remap: dict[int, int] | None = None,
    ) -> ObjectType:
        """
        Emit a spawn trigger that calls this trigger function.

        Builds the function body the first time it's called for the active level
        (requires both level_context and autoappend at that point).

        Returns the created spawn trigger. If autoappend is active at the call site,
        the spawn trigger is automatically appended; otherwise the caller handles it.

        delay:  seconds before the spawn fires.
        remap:  group ID substitutions applied at spawn time. If params was
                specified on this trigger function, all listed param IDs must be
                present in remap — omitting any raises ValueError.
        """
        # Validate params before doing anything else.
        if self._params is not None:
            if remap is None:
                raise ValueError(
                    f"This trigger_fn declares params={self._params!r}. "
                    f"Every .call() must provide remap={{...}} covering all listed IDs."
                )
            missing = [p for p in self._params if p not in remap]
            if missing:
                raise ValueError(
                    f"trigger_fn remap is missing required param IDs: {missing!r}. "
                    f"All of params={self._params!r} must be present in the remap dict."
                )

        # Build on the active level if not yet done.
        lvl = ctx.level.get()
        if lvl is not None and id(lvl) not in self._built_levels:
            if not ctx.autoappend.get():
                raise RuntimeError(
                    "The first .call() on a level requires both level_context and "
                    "autoappend to be active. Open the scope with "
                    "`with level_context(level):` (autoappend defaults to True)."
                )
            self._build(lvl)

        # Emit the spawn trigger in the call-site context (not the definition-time
        # context). It inherits whatever operations and autoappend are active here,
        # so if .call() is inside another trigger function's body, the spawn trigger
        # is correctly stamped with the outer fn_group and tracked in its objects.
        from .classes import Spawn
        s = Spawn()
        s.target_id = self.group
        s.delay = delay
        if remap:
            s.remaps = remap

        return s.obj


# ---------------------------------------------------------------------------
# Decorator
# ---------------------------------------------------------------------------

@overload
def trigger_fn(func: Callable[[], None]) -> TriggerFunction: ...

@overload
def trigger_fn(
    func: None = ...,
    *,
    group: int | None = ...,
    spawn_ordered: bool = ...,
    params: list[int] | None = ...,
) -> Callable[[Callable[[], None]], TriggerFunction]: ...

def trigger_fn(
    func: Callable[[], None] | None = None,
    *,
    group: int | None = None,
    spawn_ordered: bool = False,
    params: list[int] | None = None,
) -> TriggerFunction | Callable[[Callable[[], None]], TriggerFunction]:
    """
    Decorator that converts a plain function into a TriggerFunction.

    Usage:
        @trigger_fn
        def my_fn(): ...

        @trigger_fn(group=5, spawn_ordered=True, params=[45, 67])
        def my_fn(): ...

    group:         Bind to a specific group ID. If omitted, a group is lazily
                   allocated from the active level on first .call() or .group access.
    spawn_ordered: If True, wait(t) advances the X cursor by t * 311.58 units
                   instead of creating a new spawn-trigger chain. Equivalent to
                   wrapping the entire body in order(spawn_ordered=True).
    params:        List of group IDs that must all appear in the remap dict on
                   every .call(). Extra remap keys beyond this list are allowed.
                   Omit to disable remap validation entirely.
    """
    def _decorate(f: Callable[[], None]) -> TriggerFunction:
        return TriggerFunction(
            f,
            explicit_group=group,
            spawn_ordered=spawn_ordered,
            params=params,
        )

    if func is not None:
        # Called as @trigger_fn with no parentheses — func is the decorated function.
        return _decorate(func)

    # Called as @trigger_fn(...) — return the actual decorator.
    return _decorate


# ---------------------------------------------------------------------------
# wait()
# ---------------------------------------------------------------------------

def wait(seconds: float | None = None) -> None:
    """
    Advance time within a trigger function body.

    Must be called during a trigger function's build phase (i.e. inside the body
    of a @trigger_fn decorated function).

    Spawn-ordered mode (spawn_ordered=True or inside order(spawn_ordered=True)):
        wait(t)  — advances the X cursor by t * 311.58 units.
        wait()   — advances the X cursor by 1.3 units (one tick gap for
                   sub-tick ordering only, no meaningful time passes).

    Regular mode (default):
        wait(t)  — allocates a new sub-group, creates a spawn trigger in the
                   current group targeting the new sub-group with the given delay,
                   then switches all subsequent object creation to the new sub-group.
        wait()   — same as wait(1/240): a one-tick delay, the minimum meaningful
                   gap. Use this to create a group boundary without a real delay.
    """
    if ctx.spawn_ordered.get():
        if seconds is None:
            ctx.x_cursor.set(ctx.x_cursor.get() + 1.3)
        else:
            ctx.x_cursor.set(ctx.x_cursor.get() + seconds * _UNITS_PER_SECOND)
        return

    # Regular mode: chain via a new group and a spawn trigger.
    effective_delay = _TICK_DELAY if seconds is None else seconds

    lvl = ctx.level.get()
    if lvl is None:
        raise RuntimeError(
            "wait() requires an active level_context(). "
            "Call wait() only inside a trigger function body during build."
        )

    new_group = int(lvl.new.group())

    # Build the spawn trigger inside the current fn_group context.
    # post_object_creation will stamp it with the current fn_group and X cursor,
    # append it to the level (autoappend is True during build), and add it to
    # self._objects via the active tracking operation.
    # Properties are set after construction — the dict is a live reference in
    # level.objects, so mutations here are visible at export time.
    from .core import new_obj
    spawn_obj = new_obj(obj_id.Trigger.SPAWN)
    spawn_obj[obj_prop.Trigger.SPAWN_TRIGGER] = True
    spawn_obj[obj_prop.Trigger.MULTI_TRIGGER] = True
    spawn_obj[obj_prop.Trigger.Spawn.TARGET_ID] = new_group
    spawn_obj[obj_prop.Trigger.Spawn.DELAY] = effective_delay

    # Switch the active fn_group to the new sub-group and reset the X cursor so
    # all objects created after this wait() land in the new group, correctly
    # sequenced from X=0.
    ctx.fn_group.set(new_group)
    ctx.x_cursor.set(0.0)