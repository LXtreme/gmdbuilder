# New IDs

GD uses integer IDs to connect objects together — a move trigger targets a group ID, a pickup trigger references an item ID, and color triggers reference color channel IDs. To avoid collisions with IDs already in use in a level, gmdbuilder provides `level.new`, which scans the loaded level and hands you the next free ID for each type.

## How it works

When you call `level.new.group()` (or `.item()`, `.color()`, `.collision()`), gmdbuilder:

1. Scans all objects in `level.objects` the first time any ID is requested, collecting every ID already in use.
2. Finds the lowest unused ID in the 1–9999 range.
3. Marks it as used so the next call returns the one after it.

This scan happens lazily — only on the first call, not at load time. After that, the allocator keeps a frontier and steps forward without rescanning.

::: info
IDs returned by `level.new` are `IntEnum` values, not plain `int`. They compare and behave exactly like integers in all contexts, but their repr shows which allocation they came from — useful when debugging.
:::

## Groups

```python
from gmdbuilder import Level, new_obj, obj_prop, obj_id

level = Level.from_file("my_level.gmd")

# Get a single free group ID
g = level.new.group()
print(int(g))  # e.g. 42

# Assign it to an object
trigger = new_obj(obj_id.Trigger.MOVE)
trigger[obj_prop.GROUPS]                   = {g}
trigger[obj_prop.Trigger.Move.TARGET_ID]   = g
trigger[obj_prop.Trigger.Move.DURATION]    = 1.0

level.objects.append(trigger)
```

You can request multiple IDs at once:

```python
g1, g2, g3 = level.new.group(3)

move[obj_prop.Trigger.Move.TARGET_ID]  = g1
spawn[obj_prop.Trigger.Spawn.TARGET_ID] = g2
toggle[obj_prop.Trigger.Move.TARGET_ID] = g3
```

Counts 1 through 5 have precise tuple return types so your type checker knows exactly how many values to unpack.

## Items

Item IDs are used by Pickup and Count triggers to track in-game counters:

```python
item = level.new.item()

pickup = new_obj(obj_id.Trigger.PICKUP)
pickup[obj_prop.Trigger.Pickup.ITEM_ID] = item
pickup[obj_prop.Trigger.Pickup.COUNT]   = 1

count = new_obj(obj_id.Trigger.COUNT)
count[obj_prop.Trigger.Count.ITEM_ID]     = item
count[obj_prop.Trigger.Count.TARGET_ID]   = some_group
count[obj_prop.Trigger.Count.TARGET_COUNT] = 5

level.objects.extend([pickup, count])
```

## Colors

Color IDs are allocated the same way. The allocator is aware of both the level's existing color channels and any `COLOR_1`/`COLOR_2` assignments on objects, so it won't hand you an ID that's already referenced anywhere:

```python
from gmdbuilder import Color

c = level.new.color()
level.color[c] = Color(int(c), red=255, green=128, blue=0, opacity=1.0)

# Assign the channel to an object
block = new_obj(obj_id.Orb.YELLOW)
block[obj_prop.COLOR_1] = c
```

::: tip
You must explicitly add the new channel to `level.color` if you want it to appear in the level's color list on export. Just allocating the ID doesn't create the channel — it only reserves the number.
:::

## Collision blocks

Collision block IDs are used by Collision triggers and Collision Block objects:

```python
block_id = level.new.collision()

collision_block = new_obj(obj_id.Trigger.COLLISION_BLOCK)
collision_block[obj_prop.Trigger.CollisionBlock.BLOCK_ID] = block_id

collision_trigger = new_obj(obj_id.Trigger.COLLISION)
collision_trigger[obj_prop.Trigger.Collision.BLOCK_A]   = block_id
collision_trigger[obj_prop.Trigger.Collision.TARGET_ID] = some_group
```

## Reserving IDs manually

If your script needs a specific ID to not be allocated — because you're targeting it from a trigger you're not creating through gmdbuilder, for example — you can reserve it before any allocation calls:

```python
# Reserve a single ID
level.new.reserve_id("group", 100)

# Reserve multiple IDs at once
level.new.reserve_id("group", [100, 101, 102])
level.new.reserve_id("item",  range(1, 10))
```

Valid type strings are `"group"`, `"item"`, `"color"`, and `"collision"`.

::: warning
`reserve_id` must be called before the first allocation of that type. The scan that populates the used-ID sets happens on the first call to `.group()`, `.item()`, etc. — any `reserve_id` calls after that point have no effect on the frontier.
:::

## Return types by count

Each method follows the same overload pattern:

| Call | Return type |
|---|---|
| `level.new.group()` | `IntEnum` |
| `level.new.group(1)` | `IntEnum` |
| `level.new.group(2)` | `tuple[IntEnum, IntEnum]` |
| `level.new.group(3)` | `tuple[IntEnum, IntEnum, IntEnum]` |
| `level.new.group(n)` | `tuple[IntEnum, ...]` |

The same applies to `.item()`, `.color()`, and `.collision()`.

## A complete example

```python
from gmdbuilder import Level, new_obj, obj_id, obj_prop, Color

level = Level.from_file("my_level.gmd")

# Allocate everything we need up front
player_group        = level.new.group()
counter_item        = level.new.item()
highlight_color     = level.new.color()
collision_block     = level.new.collision()

# Set up the highlight color
level.color[highlight_color] = Color(
    int(highlight_color),
    red=245, green=197, blue=66,
    opacity=1.0, blending=True,
)

# Pickup trigger: increment the counter when the player hits group player_group
pickup = new_obj(obj_id.Trigger.PICKUP)
pickup[obj_prop.X]                      = 300
pickup[obj_prop.Y]                      = 105
pickup[obj_prop.GROUPS]                 = {player_group}
pickup[obj_prop.Trigger.Pickup.ITEM_ID] = counter_item
pickup[obj_prop.Trigger.Pickup.COUNT]   = 1

# Count trigger: when counter reaches 3, activate a spawn group
spawn_group = level.new.group()
count = new_obj(obj_id.Trigger.COUNT)
count[obj_prop.X]                          = 350
count[obj_prop.Y]                          = 105
count[obj_prop.Trigger.Count.ITEM_ID]      = counter_item
count[obj_prop.Trigger.Count.TARGET_ID]    = spawn_group
count[obj_prop.Trigger.Count.TARGET_COUNT] = 3

level.objects.extend([pickup, count])
level.export_to_file("my_level_updated.gmd")
```
