# Object Types

GD objects come in many flavors — move triggers, spawn triggers, blocks, orbs, portals — and each one has a different set of valid properties. gmdbuilder models this with **TypedDicts**: one subclass per object type, each declaring exactly which keys that object accepts and what types their values are.

You never construct these TypedDicts directly. They exist purely for the type checker. At runtime, every object is just a plain `dict`, and the TypedDicts tell Pylance or basedpyright what keys are valid on it.

## Object IDs

Every GD object has an integer ID stored at key `a1`. This is how GD itself identifies what an object is. The `obj_id` namespace organizes these into groups:

```python
from gmdbuilder import obj_id

obj_id.Trigger.MOVE       # 901
obj_id.Trigger.SPAWN      # 1268
obj_id.Trigger.COLOR      # 899
obj_id.Trigger.COUNT      # 1611
obj_id.Trigger.PICKUP     # 1817
obj_id.Trigger.COLLISION  # 1815
obj_id.Trigger.ROTATE     # 1346
obj_id.Trigger.FOLLOW     # 1347
obj_id.Trigger.PULSE      # 1006
obj_id.Trigger.ALPHA      # 1007
obj_id.Trigger.TOGGLE     # 1049
obj_id.Trigger.STOP       # 1616
obj_id.Trigger.SHAKE      # 1520
obj_id.Trigger.ANIMATE    # 1585

obj_id.Orb.YELLOW         # jump orb
obj_id.Orb.BLUE
obj_id.Orb.PINK
obj_id.Orb.RED
obj_id.Orb.GREEN
obj_id.Orb.BLACK
obj_id.Orb.DASH_GREEN
obj_id.Orb.DASH_PINK

obj_id.Portal.CUBE
obj_id.Portal.SHIP
obj_id.Portal.BALL
obj_id.Portal.UFO
obj_id.Portal.WAVE
obj_id.Portal.ROBOT
obj_id.Portal.SPIDER
obj_id.Portal.SWING

obj_id.Pad.YELLOW
obj_id.Pad.BLUE
obj_id.Pad.PINK
obj_id.Pad.RED

obj_id.Speed.NORMAL
obj_id.Speed.FAST
obj_id.Speed.FASTER
obj_id.Speed.HALF
obj_id.Speed.DOUBLE
```

## TypedDict subclasses

The `object_types` module exports a TypedDict subclass for every recognized object type. The name follows the pattern `<ObjectName>Type`:

```python
import gmdbuilder.object_types as td

td.MoveType
td.SpawnType
td.ColorType
td.CountType
td.PickupType
td.InstantCountType
td.RotateType
td.FollowType
td.AlphaType
td.ToggleType
td.PulseType
td.ShakeType
td.StopType
td.CollisionType
td.CollisionBlockType
td.AnimateType
td.TriggerType       # base type shared by all triggers
td.ObjectType        # base type shared by all objects
td.AllPropsType      # union of all known properties (for generic access)
```

These types exist for the type checker. You use them in two ways: as the argument to `is_obj_type()`, or as annotations on your own functions that accept a specific trigger type.

## Checking and narrowing types

### is_obj_id

Checks whether an object's ID matches a specific integer. Works as a TypeGuard — the type checker narrows the object type inside the `if` block:

```python
from gmdbuilder import is_obj_id, obj_id, obj_prop

for obj in level.objects:
    if is_obj_id(obj, obj_id.Trigger.MOVE):
        # obj is narrowed to MoveType here
        obj[obj_prop.Trigger.Move.TARGET_ID] = 5
        obj[obj_prop.Trigger.Move.DURATION]  = 1.0
```

### is_obj_type

Checks against a TypedDict subclass rather than a raw integer. More useful when you're passing objects to typed functions or working with the type directly:

```python
from gmdbuilder import is_obj_type
import gmdbuilder.object_types as td

for obj in level.objects:
    if is_obj_type(obj, td.SpawnType):
        # obj is narrowed to SpawnType
        obj[obj_prop.Trigger.Spawn.DELAY] = 0.1
```

Both checks are equivalent at runtime — they both just compare the `a1` key against the known ID for that TypedDict. The difference is ergonomic: use `is_obj_id` when you have the integer ID handy, and `is_obj_type` when you're working with the TypedDict type explicitly.

## Annotating your own functions

The TypedDicts are most useful when you write helper functions that work on a specific trigger type. Annotating the parameter lets the type checker verify that callers pass the right object and that the body only accesses valid keys:

```python
import gmdbuilder.object_types as td
from gmdbuilder import obj_prop

def configure_move(trigger: td.MoveType, target: int, duration: float) -> None:
    trigger[obj_prop.Trigger.Move.TARGET_ID] = target
    trigger[obj_prop.Trigger.Move.DURATION]  = duration
    trigger[obj_prop.Trigger.Move.EASING]    = obj_enum.Easing.EASE_IN_OUT

def zero_spawn_delays(objects: list[td.SpawnType]) -> None:
    for t in objects:
        t[obj_prop.Trigger.Spawn.DELAY] = 0.0
```

Calling `configure_move` with a `ColorType` would be a type error. Calling it with the result of `new_obj(obj_id.Trigger.MOVE)` would be fine — `new_obj` is overloaded to return the correct TypedDict subtype automatically.

## Enum values

Many trigger properties accept a fixed set of integer values. The `obj_enum` namespace provides named constants for all of them so you don't have to look up or hardcode magic numbers:

```python
from gmdbuilder import obj_enum, obj_prop

# Easing types for Move, Rotate, Scale, etc.
trigger[obj_prop.Trigger.Move.EASING] = obj_enum.Easing.NONE
trigger[obj_prop.Trigger.Move.EASING] = obj_enum.Easing.EASE_IN
trigger[obj_prop.Trigger.Move.EASING] = obj_enum.Easing.EASE_OUT
trigger[obj_prop.Trigger.Move.EASING] = obj_enum.Easing.EASE_IN_OUT
trigger[obj_prop.Trigger.Move.EASING] = obj_enum.Easing.ELASTIC_IN
trigger[obj_prop.Trigger.Move.EASING] = obj_enum.Easing.BOUNCE_OUT
trigger[obj_prop.Trigger.Move.EASING] = obj_enum.Easing.BACK_IN_OUT
# ... and all other combinations
```

Enum values are plain `int` subclasses. They compare equal to their integer equivalents and work anywhere an integer is accepted.

## Property keys

Every property key is a string in the form `"a<number>"`, mirroring GD's internal numbering. The `obj_prop` namespace maps readable names to these strings:

```python
obj_prop.ID          # "a1"   — object ID (read-only after creation)
obj_prop.X           # "a2"   — X position
obj_prop.Y           # "a3"   — Y position
obj_prop.ROTATION    # "a6"   — rotation in degrees
obj_prop.GROUPS      # "a57"  — set[int] of group IDs
obj_prop.COLOR_1     # "a21"  — primary color channel ID
obj_prop.COLOR_2     # "a22"  — secondary color channel ID
obj_prop.Z_ORDER     # "a25"  — Z layer order
obj_prop.EDITOR_L1   # "a20"  — editor layer 1
obj_prop.EDITOR_L2   # "a61"  — editor layer 2
```

Trigger-specific keys are nested under `obj_prop.Trigger.<Name>.*`:

```python
# Move trigger
obj_prop.Trigger.Move.TARGET_ID          # "a51"
obj_prop.Trigger.Move.DURATION           # "a10"
obj_prop.Trigger.Move.EASING             # "a30"
obj_prop.Trigger.Move.X_MOD              # "a28"
obj_prop.Trigger.Move.Y_MOD              # "a29"
obj_prop.Trigger.Move.LOCK_TO_PLAYER_X   # "a58"
obj_prop.Trigger.Move.LOCK_TO_PLAYER_Y   # "a59"
obj_prop.Trigger.Move.USE_SMALL_STEP     # "a401"

# Spawn trigger
obj_prop.Trigger.Spawn.TARGET_ID         # "a51"
obj_prop.Trigger.Spawn.DELAY             # "a63"
obj_prop.Trigger.Spawn.ORDERED           # "a96"
obj_prop.Trigger.Spawn.RESET_REMAP       # "a128"
obj_prop.Trigger.Spawn.REMAPS            # "a129" — dict[int, int]

# Color trigger
obj_prop.Trigger.Color.CHANNEL           # "a23"
obj_prop.Trigger.Color.DURATION          # "a10"
obj_prop.Trigger.Color.RED               # "a7"
obj_prop.Trigger.Color.GREEN             # "a8"
obj_prop.Trigger.Color.BLUE              # "a9"
obj_prop.Trigger.Color.OPACITY           # "a35"
obj_prop.Trigger.Color.BLENDING          # "a17"
obj_prop.Trigger.Color.COPY_ID           # "a50"

# Count / Pickup triggers
obj_prop.Trigger.Count.ITEM_ID           # "a80"
obj_prop.Trigger.Count.TARGET_ID         # "a51"
obj_prop.Trigger.Count.TARGET_COUNT      # "a77"
obj_prop.Trigger.Count.ACTIVATE_GROUP    # "a56"
obj_prop.Trigger.Pickup.ITEM_ID          # "a80"
obj_prop.Trigger.Pickup.COUNT            # "a77"

# Collision
obj_prop.Trigger.Collision.BLOCK_A       # "a71"
obj_prop.Trigger.Collision.BLOCK_B       # "a72"
obj_prop.Trigger.Collision.TARGET_ID     # "a51"
obj_prop.Trigger.CollisionBlock.BLOCK_ID # "a80"
```

::: tip Finding keys
Not sure what key a property uses? Use the [Property Search](./reference) page — search by property name or key string to find the right constant and its type.
:::

## from_object_string

If you have a raw GD object string (from an external tool, exported from the editor, or copied from game data), parse it with `from_object_string`:

```python
from gmdbuilder import from_object_string
import gmdbuilder.object_types as td

# Parse and get a generic ObjectType
obj = from_object_string("1,901,2,300,3,105,10,1.5,51,5;")

# Parse with an explicit type hint for static analysis
trigger: td.MoveType = from_object_string("1,901,2,300,3,105,10,1.5,51,5;")
```

The resulting object is a fully validated `Object` dict — you can modify it and append it to `level.objects` like anything else.