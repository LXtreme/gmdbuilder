# New IDs

GD uses integer IDs to connect objects together — triggers reference group IDs, pickup/count triggers share item IDs, and color triggers reference color channel IDs. `level.new` scans the loaded level and hands you the next free ID for each type, so you never have to track them manually.

```python
from gmdbuilder import Level

level = Level.from_file("my_level.gmd")

g     = level.new.group()
item  = level.new.item()
col   = level.new.color()
block = level.new.collision()
```

::: info
IDs returned by `level.new` are `IntEnum` values. They compare and behave exactly like plain integers in all contexts, but carry a descriptive repr — useful when debugging.
:::

## Groups

```python
g = level.new.group()

trigger = new_obj(obj_id.Trigger.MOVE)
trigger[obj_prop.GROUPS]                 = {g}
trigger[obj_prop.Trigger.Move.TARGET_ID] = g
```

Request multiple at once:

```python
g1, g2, g3 = level.new.group(3)
```

Counts 1–5 have precise tuple return types so your type checker knows exactly how many values to unpack.

## Items

Item IDs are shared between Pickup and Count triggers to track in-game counters:

```python
item = level.new.item()

pickup[obj_prop.Trigger.Pickup.ITEM_ID]    = item
count[obj_prop.Trigger.Count.ITEM_ID]      = item
count[obj_prop.Trigger.Count.TARGET_COUNT] = 5
```

## Colors

The allocator is aware of both the level's existing color channels and any `COLOR_1`/`COLOR_2` references on objects, so it won't hand you an ID that's already in use:

```python
from gmdbuilder import Color

c = level.new.color()
level.color[c] = Color(red=255, green=128, blue=0, opacity=1.0)
```

::: tip
Allocating the ID doesn't create the channel — you must assign a `Color` to `level.color[c]` for it to appear in the level on export.
:::

## Collision blocks

```python
block_id = level.new.collision()

collision_block[obj_prop.Trigger.CollisionBlock.BLOCK_ID] = block_id
collision_trigger[obj_prop.Trigger.Collision.BLOCK_A]     = block_id
```

## Reserving IDs manually

Reserve a specific ID before any allocation calls to prevent it from being handed out:

```python
level.new.reserve_id("group", 100)
level.new.reserve_id("group", [100, 101, 102])
```

Valid type strings: `"group"`, `"item"`, `"color"`, `"collision"`.

::: warning
`reserve_id` must be called before the first allocation of that type. The scan that populates used-ID sets happens on the first `.group()` / `.item()` / etc. call — reservations after that have no effect.
:::

## Return types by count

| Call | Return type |
|---|---|
| `level.new.group()` | `IntEnum` |
| `level.new.group(1)` | `IntEnum` |
| `level.new.group(2)` | `tuple[IntEnum, IntEnum]` |
| `level.new.group(3)` | `tuple[IntEnum, IntEnum, IntEnum]` |
| `level.new.group(n)` | `tuple[IntEnum, ...]` |

The same applies to `.item()`, `.color()`, and `.collision()`.