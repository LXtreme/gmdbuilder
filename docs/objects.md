# Add & Edit Objects

## Creating objects

Use `new_obj()` to create a new object with its default properties populated. Pass either an integer ID or a constant from `obj_id`:

```python
from gmdbuilder import new_obj, obj_id

trigger = new_obj(obj_id.Trigger.MOVE)
orb     = new_obj(obj_id.Orb.YELLOW)
portal  = new_obj(obj_id.Portal.CUBE)
```

`new_obj()` returns an `ObjectType` dict with all default properties already set, matching what GD would give you if you placed that object in the editor with no changes.

You can also parse a raw GD object string directly — useful if you've copied one from an external tool:

```python
from gmdbuilder import from_object_string

# Translates "1,1611,2,50,3,45" → {"a1": 1611, "a2": 50.0, "a3": 45.0, ...}
obj = from_object_string("1,1611,2,50,3,45;")
```

## Setting properties

Assign properties using keys from the `obj_prop` namespace. Every assignment is validated immediately:

```python
from gmdbuilder import obj_prop, obj_enum

trigger = new_obj(obj_id.Trigger.MOVE)

trigger[obj_prop.X]                        = 300
trigger[obj_prop.Y]                        = 105
trigger[obj_prop.Trigger.Move.DURATION]    = 1.5
trigger[obj_prop.Trigger.Move.TARGET_ID]   = 12
trigger[obj_prop.Trigger.Move.EASING]      = obj_enum.Easing.EASE_IN_OUT
trigger[obj_prop.GROUPS]                   = {4, 8}
```

::: tip Property key naming
All trigger-specific properties live under `obj_prop.Trigger.<TriggerName>.*`. Common properties shared by all objects (`X`, `Y`, `GROUPS`, `COLOR_1`, `ROTATION`, etc.) live directly on `obj_prop`.
:::

Property keys are just string literals like `"a51"` under the hood. `obj_prop` is a namespace of those string constants so you never have to remember or look up the numbers.

## Enum values

Some properties take a fixed set of integer values — easing types, pulse modes, target types, and so on. Use `obj_enum` to avoid magic numbers:

```python
from gmdbuilder import obj_enum, obj_prop

trigger[obj_prop.Trigger.Move.EASING] = obj_enum.Easing.EASE_IN_OUT
trigger[obj_prop.Trigger.Move.EASING] = obj_enum.Easing.BOUNCE_OUT
```

The enum values are plain `int` subclasses, so they work anywhere an integer is accepted.

## Adding objects to a level

Use `level.objects.append()` to add a single object, or `extend()` for multiple:

```python
level.objects.append(trigger)
level.objects.extend([move_a, move_b, spawn])
```

Every object appended this way automatically receives the level's `tag_group` added to its `GROUPS` set. This is how gmdbuilder tracks which objects were added by your script — on the next load, those objects are filtered out and the level starts clean again.

::: info
`insert()` behaves the same way as `append()` — it validates the object and applies the tag group.
:::

## Editing existing objects

Index directly into `level.objects` to get a reference to an existing object. Mutations are validated in place:

```python
obj = level.objects[0]
obj[obj_prop.X] = 500          # validated immediately
obj[obj_prop.GROUPS] = {1, 2}  # replaces the group set
```

You can iterate the full list and edit conditionally:

```python
from gmdbuilder import obj_prop, obj_id

for obj in level.objects:
    if obj[obj_prop.ID] == obj_id.Trigger.SPAWN:
        obj[obj_prop.Trigger.Spawn.DELAY] = 0.0
```

## Type narrowing with is_obj_id and is_obj_type

When iterating a generic object list, you often want to edit only objects of a specific type while keeping the type checker happy. gmdbuilder provides two TypeGuard helpers for this.

`is_obj_id()` checks the integer ID:

```python
from gmdbuilder import is_obj_id, obj_id, obj_prop

for obj in level.objects:
    if is_obj_id(obj, obj_id.Trigger.MOVE):
        # obj is narrowed to MoveType here
        obj[obj_prop.Trigger.Move.TARGET_ID] = 5
```

`is_obj_type()` checks against a TypedDict subclass:

```python
from gmdbuilder import is_obj_type, obj_prop
import gmdbuilder.object_types as td

for obj in level.objects:
    if is_obj_type(obj, td.SpawnType):
        # obj is narrowed to SpawnType here
        obj[obj_prop.Trigger.Spawn.DELAY] = 0.1
```

Both do the same runtime check — `is_obj_type` is more useful when you're working with the TypedDict type directly (for example when passing objects to typed functions).

## Deleting objects

`delete_where()` removes objects matching a condition. It returns the number of objects deleted.

**Filter by a dict** — every key/value in the filter must match:

```python
# Delete all move triggers
level.objects.delete_where({obj_prop.ID: obj_id.Trigger.MOVE})

# Delete objects in group 5 (None is a wildcard for the value)
level.objects.delete_where({obj_prop.GROUPS: None})
```

**Filter by a predicate**:

```python
# Delete all objects whose X position is negative
level.objects.delete_where(lambda obj: obj[obj_prop.X] < 0)
```

**Limit how many are deleted**:

```python
# Delete only the first 3 matching objects
level.objects.delete_where({obj_prop.ID: obj_id.Trigger.MOVE}, limit=3)
```

::: warning
`delete_where` is not available in live editor mode. The live editor only supports adding objects, not removing them through gmdbuilder.
:::

## A complete example

```python
from gmdbuilder import Level, new_obj, is_obj_id, obj_id, obj_prop, obj_enum

level = Level.from_file("my_level.gmd")

# Remove all existing move triggers
level.objects.delete_where({obj_prop.ID: obj_id.Trigger.MOVE})

# Give every spawn trigger a zero delay
for obj in level.objects:
    if is_obj_id(obj, obj_id.Trigger.SPAWN):
        obj[obj_prop.Trigger.Spawn.DELAY] = 0.0

# Add a new move trigger
move = new_obj(obj_id.Trigger.MOVE)
move[obj_prop.X]                      = 300
move[obj_prop.Y]                      = 105
move[obj_prop.Trigger.Move.DURATION]  = 1.0
move[obj_prop.Trigger.Move.TARGET_ID] = 10
move[obj_prop.Trigger.Move.EASING]    = obj_enum.Easing.EASE_IN_OUT
move[obj_prop.GROUPS]                 = {4}
level.objects.append(move)

level.export_to_file("my_level_updated.gmd")
```
