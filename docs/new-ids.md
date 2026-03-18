# New IDs

GD uses integer IDs to connect objects together — triggers reference group IDs, pickup/count triggers share item IDs, and color triggers reference color channel IDs. `level.new` scans the level instance and hands you the next free ID for each type, so you never have to track them manually.

Note that scanning for free IDs happens upon the level load. To exclude IDs from the free ID list afterward, see [Reserving IDs](./new-ids#reserving-ids-manually).

::: info
IDs returned by `level.new` are `IntEnum` values. They compare and behave exactly like plain integers in all contexts, but carry a descriptive repr — useful when debugging.
:::
## Fetching an ID:

The IDs given are IntEnums:

```python
level = Level.from_file("my_level.gmd")

g     = level.new.group()
item  = level.new.item()
col   = level.new.color()
block = level.new.collision()
```

You may fetch multiple in one call:
```python
g1, g2, g3 = level.new.group(3)
```


::: info
Fetching a new Color ID doesn't create the channel — you must assign a `Color` to `level.color[c]` for it to appear in the level on export. See [Colors](./colors.md#adding-a-new-color-channel)
:::

## Reserving IDs manually

Reserve a specific ID before any allocation calls to prevent it from being handed out. This may be useful if you choose to hardcode groups for some objects that you are adding:

```python
level.new.reserve_id("group", 100)
level.new.reserve_id("group", [100, 101, 102])
```

Valid type strings: `"group"`, `"item"`, `"color"`, `"collision"`.

## Return types by count

Returning multiples includes some static type safety.

| Call | Return type |
|---|---|
| `level.new.group()` | `IntEnum` |
| `level.new.group(1)` | `IntEnum` |
| `level.new.group(2)` | `tuple[IntEnum, IntEnum]` |
| `level.new.group(3)` | `tuple[IntEnum, IntEnum, IntEnum]` |
| `level.new.group(n)` | `tuple[IntEnum, ...]` |

The same applies to `.item()`, `.color()`, and `.collision()`.