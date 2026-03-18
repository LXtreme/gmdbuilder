# Colors

Color channels are exposed through `level.color` — a plain Python dict mapping channel ID integers to `Color` dataclasses. 
Changes to these values are written back to the level on export.

### Special Color Channels:

`color_id` provides named constants for GD's special built-in channels:
```python
from gmdbuilder import color_id
```
Sample:
| Constant | ID |
|---|---|
| `color_id.BACKGROUND` | 1000 |
| `color_id.GROUND` | 1001 |
| `color_id.MIDDLEGROUND` | 1011 | 
| `color_id.LINE` | 1002 |
... | ... |


## The Color dataclass

Each entry in `level.color` is a `Color` instance with these fields:

```python
@dataclass
class Color:
    red: int = 0
    green: int = 0
    blue: int = 0
    opacity: float = 0.0
    blending: bool = False
    copy_id: int = 0 # channel to copy color from (0 = none)
    hsv: HSV = HSV()
    copy_opacity: bool = False
    disable_legacy_hsv: bool = False
    player: int = -1
```


## Reading color channels

After loading a level, `level.color` is populated with every color channel defined in that level:

```python
bg = level.color[color_id.BACKGROUND]
print(bg.red, bg.green, bg.blue)   # e.g. 0 102 255
print(bg.opacity)                  # e.g. 1.0
```

Channels not in this list are accessed by their integer ID directly.

## Modifying a color channel

Modify the `Color` object in-place. 
Changes are applied to the level on the next `export_to_file()` or `export_to_live_editor()` call:

```python
from gmdbuilder import Level, color_id

level = Level.from_file("my_level.gmd")

bg = level.color[color_id.BACKGROUND]
bg.red   = 38
bg.green = 10
bg.blue  = 72

# Or use the set_rgba helper
level.color[color_id.GROUND].set_rgba(20, 5, 50)
```


## Adding a new color channel

If you assign to a channel ID that doesn't exist in the level yet, it is created and added to the level on export:

```python
from gmdbuilder import Level, Color

level = Level.from_file("my_level.gmd")

# Allocate a free channel ID and create it
c = level.new.color()
level.color[c] = Color(red=255, green=80, blue=0, opacity=1.0)
```

::: tip Allocating vs picking an ID
It is recommended to use `level.new.color()` rather than picking an ID by hand. See [New IDs](./new-ids)
:::


## Convenience helpers

`Color` provides a few helpers so you don't have to set channels manually:

### set_rgba / get_rgba

```python
color.set_rgba(255, 128, 0)           # sets red, green, blue
color.set_rgba(255, 128, 0, alpha=0.8) # also sets opacity
r, g, b, a = color.get_rgba()
```

### set_hex / get_hex

```python
color.set_hex("#FF8800")
color.set_hex("FF8800")   # hash is optional

print(color.get_hex())    # "#FF8800"
```

## A complete example

```python
from gmdbuilder import Level, Color, color_id

level = Level.from_file("my_level.gmd")

level.color[color_id.BACKGROUND].set_hex("#26064A")
if 1 in level.color:
    level.color[1].set_hex("#3A0E6E")

# Allocate a new channel for a custom object glow color
glow = level.new.color()
level.color[glow] = Color(red=245, green=197, blue=66, opacity=1.0, blending=True)

# Make channel 10 copy P1's color
level.color[10] = Color(player=1, copy_opacity=True)

level.export_to_file("my_level_updated.gmd")
```
