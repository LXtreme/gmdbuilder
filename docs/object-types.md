# Object Types

Every object in `level.objects` has a base type of `ObjectType` — essentially a `dict[str, Any]`. When iterating a mixed list you often want to work only with a specific trigger type. gmdbuilder provides two TypeGuard helpers for this.

## is_obj_id

Checks the integer ID at `a1`. The type checker narrows the object inside the `if` block:

```python
from gmdbuilder import is_obj_id, obj_id, obj_prop

for obj in level.objects:
    if is_obj_id(obj, obj_id.Trigger.MOVE):
        obj[obj_prop.Trigger.Move.TARGET_ID] = 5
        obj[obj_prop.Trigger.Move.DURATION]  = 1.0
```

## is_obj_type

Checks against a `TypedDict` subclass from `gmdbuilder.object_types`. More useful when you're working with the type directly or passing objects into typed functions:

```python
from gmdbuilder import is_obj_type, obj_prop
import gmdbuilder.object_types as td

for obj in level.objects:
    if is_obj_type(obj, td.SpawnType):
        obj[obj_prop.Trigger.Spawn.DELAY] = 0.1
```

Both do the same runtime check — they compare `a1` against the known ID for that `TypedDict`. `is_obj_id` is convenient when you have the integer handy; `is_obj_type` is better when the type itself is what you're reasoning about.

## Annotating your own functions

The TypedDicts are most valuable when you write helper functions that operate on a specific trigger type. Annotating the parameter lets the type checker verify callers pass the right object and that the body only accesses valid keys:

```python
import gmdbuilder.object_types as td
from gmdbuilder import obj_prop, obj_id, new_obj, enum

def configure_move(trigger: td.MoveType, target: int, duration: float) -> None:
    ppt = obj_prop.Trigger
    trigger[ppt.Move.TARGET_ID] = target
    trigger[ppt.Move.DURATION] = duration
    trigger[ppt.Move.EASING] = enum.Easing.EASE_IN_OUT
    trigger[ppt.SPAWN_TRIGGERED] = True
    trigger[ppt.MULTI_TRIGGERED] = True

move = new_obj(obj_id.Trigger.MOVE)  # auto-detected statically as MoveType
configure_move(move, target=10, duration=1.5)
```

Passing a `SpawnType` or any other type to `configure_move` would raise a static type error.