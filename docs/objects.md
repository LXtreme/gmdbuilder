# Add & Edit Objects

## How are objects represented?

In GD, objects (after parsing from an object string) are expressed as dict pairs of `int|str`- `Any`.

In gmdbuilder, every object is represented as a `dict[str, Any]` with GD's integer keys converted to `"a<property-int>"`. 

This unifiies all property keys (including special level keys `"kA<int>"`). Most importantly, typeddicts grants static type information for each property field, as well as defining which properties are allowed on the given object type.

```python
repr(all_objects[0])
# Object({"a1": 1, "a2": 105.0, "a3": 195.0, "a57": {3, 7}, ...})
```

In GD's object strings, many special property values are represented as custom formatted strings. To make them easier to work with, they are converted to more usable forms. 
Here are some examples:
| Property | Name | GD type | gmdbuilder type |
| --- | --- | --- | --- |
| 57 | GROUPS | `1.2.3.4` | `{ 1, 2, 3, 4 }` |
| 442 | REMAPS | `1.2.3.4` | `{ 1: 2, 3: 4 }` |

See [Property Search](./reference.md)

## Creating objects

Use `new_obj()` to create a new object with its default properties populated:

```python
from gmdbuilder import new_obj, obj_id

trigger = new_obj(obj_id.Trigger.SPAWN)
orb = new_obj(obj_id.Orb.YELLOW)
portal = new_obj(obj_id.Portal.CUBE)
move = new_obj(901) # automatically casted as MoveType
```

You can also parse a raw GD object string directly:

```python
from gmdbuilder import from_object_string

# "1,1611,2,50,3,45" → {"a1": 1611, "a2": 50.0, "a3": 45.0, ...}
obj = from_object_string("1,1611,2,50,3,45;")
```

## Setting properties

Assign properties using keys from the `obj_prop` namespace. Every assignment is validated immediately:

```python
from gmdbuilder import new_obj, enum

trigger = new_obj(obj_id.Trigger.MOVE)
trigger[obj_prop.X] = 300
trigger[obj_prop.Y] = 105
trigger[obj_prop.GROUPS] = {4, -8} # Invalid group -8, throws ValueError
trigger[obj_prop.Trigger.Move.DURATION] = 1.5
trigger[obj_prop.Trigger.Move.EASING] = enum.Easing.EASE_IN_OUT
trigger[obj_prop.Trigger.SPAWN_TRIGGERED] = True
```


`enum` provides named constants for properties that take a fixed set of integer values — easing types, pulse modes, and so on. The values are plain `int` subclasses and work anywhere an integer is accepted.

## Adding objects to a level

Use `append()` for a single object or `extend()` for multiple:

```python
level.objects.append(trigger)
level.objects.extend([move_a, move_b, spawn])
```

Every appended object automatically receives the level's `tag_group` in its `GROUPS` set. This is how gmdbuilder tracks which objects belong to the current script run. On the next load, those objects are stripped and the level starts clean. The `tag_group` is configured when the level is loaded:
```python
level = Level.from_file("my_level.gmd", tag_group=9999) # default is 9999
level = Level.from_live_editor(tag_group=9000)
```

## Deleting objects

`delete_where()` removes objects matching a condition and returns the count deleted:

```python
from gmdbuilder import obj_prop, obj_id

# By dict — all key/value pairs must match (None is a wildcard value)
level.objects.delete_where({obj_prop.ID: obj_id.Trigger.MOVE})

# By predicate
level.objects.delete_where(lambda obj: obj[obj_prop.X] < 0)

# Limit how many are removed
level.objects.delete_where({obj_prop.ID: obj_id.Trigger.MOVE}, limit=3)
```

## Type narrowing

When iterating a mixed object list, use the TypeGuard helpers to narrow to a specific type:

`is_obj_id()` checks the integer ID:

```python
from gmdbuilder import is_obj_id, obj_id, obj_prop

for obj in level.objects:
    if is_obj_id(obj, obj_id.Trigger.MOVE):
        obj[obj_prop.Trigger.Move.TARGET_ID] = 5
```

`is_obj_type()` checks against a TypedDict subclass:

```python
from gmdbuilder import is_obj_type, object_types as td

for obj in level.objects:
    if is_obj_type(obj, td.SpawnType):
        obj[obj_prop.Trigger.Spawn.DELAY] = 0.1
```
