from contextvars import copy_context
from functools import update_wrapper
from typing import Any, Callable, Iterable, Literal, overload, Generic, ParamSpec, TypeVar


from .mappings import obj_id, obj_prop
from .core import ObjectType, new_obj
from .classes.control import Spawn
from .context import ctx, push_op, pop_op
from .fields import key_is_allowed


P = ParamSpec('P')
R = TypeVar('R')


class TriggerFunction(Generic[P, R]):
    def __init__(
        self, fn: Callable[P, R], *,
        spawn_ordered: bool = False,
        params: Iterable[int] | None = None,
        group: int | None = None,
    ) -> None:
        self._fn = fn
        self.spawn_ordered = spawn_ordered
        self.params = list(params) if params is not None else None
        self._group = group
        self.objects: list[ObjectType] = []

        self._definition_context = copy_context()

        # Makes this object look more like the original function
        update_wrapper(self, fn)

    @property
    def group(self) -> int:
        """The group ID assigned to this trigger function."""
        if self._group is not None:
            return self._group

        lvl = ctx.level.get()
        if lvl is None:
            raise RuntimeError(
                f"'{self._fn.__name__}.group' cannot be allocated: no active level_context(). "
                "Either pin a group with @trigger_fn(group=N), or access .group "
                "within an active level_context()."
            )

        self._group = lvl.new.group()
        return self._group

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> None:
        """
        Build (or extend) the trigger function body by running _fn with the given arguments.
        Can be called multiple times to dynamically add more triggers to the same group.
        """
        self._build(*args, **kwargs)

    def _build(self, *args: Any, **kwargs: Any) -> None:
        """
        Execute the function body inside the definition-time context, with
        autoappend and ordering forced on, and collect the resulting objects.
        
        Called automatically on the first .call() if objects is still empty,
        or directly via myfunc() for dynamic/extended builds.
        """
        calling_level = ctx.level.get()
        if calling_level is None:
            raise RuntimeError(
                f"'{self._fn.__name__}()' requires an active level_context() to build."
            )

        def _set_trigger_flags(obj: ObjectType) -> None:
            if key_is_allowed(obj[obj_prop.ID], obj_prop.Trigger.SPAWN_TRIGGER):
                # is TriggerType so contains both spawn and multi.
                obj[obj_prop.Trigger.SPAWN_TRIGGER] = True  # type: ignore[literal-required]
                obj[obj_prop.Trigger.MULTI_TRIGGER] = True  # type: ignore[literal-required]

        before_count = len(calling_level.objects)

        def _run() -> None:
            ctx.level.set(calling_level)
            ctx.autoappend.set(True)
            ctx.fn_group.set(self.group)
            ctx.spawn_ordered.set(self.spawn_ordered)
            ctx.x_cursor.set(0.0)
            push_op(_set_trigger_flags)
            try:
                self._fn(*args, **kwargs)
            finally:
                pop_op()

        self._definition_context.run(_run)
        self.objects.extend(calling_level.objects[before_count:])

    @overload
    def call(self, delay: float = 0, remaps: dict[int, int] | None = None, *, wrap: Literal[False] = False) -> ObjectType: ...
    @overload
    def call(self, delay: float = 0, remaps: dict[int, int] | None = None, *, wrap: Literal[True]) -> Spawn: ...
    @overload
    def call(self, delay: float = 0, remaps: dict[int, int] | None = None, *, wrap: bool) -> ObjectType | Spawn: ...
    def call(self, delay: float = 0, remaps: dict[int, int] | None = None, *, wrap: bool = False) -> Spawn | ObjectType:
        """
        Call this trigger function.

        Creates and returns a spawn trigger targeting this function's group.
        If the function body has not been built yet, builds it first.

        delay:  spawn trigger delay in seconds.
        remaps: optional dict of {from_group: to_group} applied to the spawn trigger.
                Keys must be in params if params was declared.
        wrap:   if True, returns the spawn trigger as a Spawn wrapper instead of a raw ObjectType.
        """
        if remaps:
            if self.params is not None:
                if len(self.params) == 0:
                    raise ValueError(
                        f"'{self._fn.__name__}' declares params=[] — no remaps are permitted."
                    )
                invalid = {k for k in remaps if k not in self.params}
                if invalid:
                    raise ValueError(
                        f"Remap keys {invalid} are not declared in "
                        f"'{self._fn.__name__}'.params={self.params}"
                    )

        if not self.objects:
            self() # type: ignore[call-arg]

        spawn = new_obj(obj_id.Trigger.SPAWN)
        spawn[obj_prop.Trigger.Spawn.TARGET_ID] = self.group
        spawn[obj_prop.Trigger.Spawn.DELAY] = delay
        if remaps:
            spawn[obj_prop.Trigger.Spawn.REMAPS] = remaps

        return Spawn.wrap(spawn) if wrap else spawn


# ---------------------------------------------------------------------------
# Decorator factory
# ---------------------------------------------------------------------------


@overload
def trigger_fn(fn: Callable[P, R], /) -> TriggerFunction[P, R]: ...
@overload
def trigger_fn(
    *,
    spawn_ordered: bool = False,
    params: Iterable[int] | None = None,
    group: int | None = None,
) -> Callable[[Callable[P, R]], TriggerFunction[P, R]]: ...
def trigger_fn(
    fn: Callable[P, R] | None = None,
    /,*, spawn_ordered: bool = False,
    params: Iterable[int] | None = None,
    group: int | None = None,
) -> TriggerFunction[P, R] | Callable[[Callable[P, R]], TriggerFunction[P, R]]:
    """
    Decorator that turns a plain function into a TriggerFunction.

    Usage:
        @trigger_fn(spawn_ordered=True, params=[45, 67], group=5)
        def my_fn(): ...
    """
    def decorator(f: Callable[P, R]) -> TriggerFunction[P, R]:
        return TriggerFunction(
            f,
            spawn_ordered=spawn_ordered,
            params=params,
            group=group,
        )

    if fn is not None:
        return decorator(fn)

    return decorator
