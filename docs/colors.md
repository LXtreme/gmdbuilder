# Colors

Color channels in GD control the fill color of objects that reference them. gmdbuilder exposes them through `level.color` — a plain Python dict mapping channel IDs to `Color` dataclasses. Changes to these values are written back to the level on export.

## Reading color channels

After loading a level, `level.color` is populated with every color channel defined in that level:

```python
from gmdbuilder import Level, color_id

level = Level.from_file("my_level.gmd")

# Access a channel by its integer ID
bg = level.color[color_id.BACKGROUND]
print(bg.red, bg.green, bg.blue)   # e.g. 0 102 255
print(bg.opacity)                  # e.g. 1.0
```

`color_id` provides named constants for GD's special built-in channels:

| Constant | ID | Description |
|---|---|---|
| `color_id.BACKGROUND` | 1000 | Background color |
| `color_id.GROUND` | 1001 | Ground color |
| `color_id.GROUND_2` | 1009 | Secondary ground color |
| `color_id.MIDDLEGROUND` | 1011 | Middleground color |
| `color_id.LIGHT_BG` | 1003 | Background light color |
| `color_id.LIGHTER` | 1007 | Lighter color |
| `color_id.LINE` | 1002 | Object outline color |
| `color_id.OBJECT` | 1004 | Default object color |
| `color_id.PLAYER_1` | 1005 | Player 1 color |
| `color_id.PLAYER_2` | 1006 | Player 2 color |

Channels not in this list (custom channels 1–999) are accessed by their integer ID directly.

## The Color dataclass

Each entry in `level.color` is a `Color` instance with these fields:

```python
@dataclass
class Color:
    channel:             int                      # required, set automatically from the dict key
    red:                 int   = 0
    green:               int   = 0
    blue:                int   = 0
    opacity:             float = 0.0
    blending:            bool  = False
    copy_id:             int   = 0                # channel to copy color from (0 = none)
    hsv:                 HSV   = HSV()
    copy_opacity:        bool  = False
    disable_legacy_hsv:  bool  = False
    player:              int   = -1               # -1 = none, 1 = P1, 2 = P2
```

## Modifying a color channel

Modify the `Color` object in-place. Changes are applied to the level on the next `export_to_file()` or `export_to_live_editor()` call:

```python
from gmdbuilder import Level, color_id

level = Level.from_file("my_level.gmd")

# Change the background to a deep purple
bg = level.color[color_id.BACKGROUND]
bg.red   = 38
bg.green = 10
bg.blue  = 72

# Or use the set_rgba helper
level.color[color_id.GROUND].set_rgba(20, 5, 50)
```

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

## Adding a new color channel

If you assign to a channel ID that doesn't exist in the level yet, it is created and added to the level on export:

```python
from gmdbuilder import Level, Color

level = Level.from_file("my_level.gmd")

# Allocate a free channel ID and create it
c = level.new.color()
level.color[c] = Color(int(c), red=255, green=80, blue=0, opacity=1.0)
```

::: tip Allocating vs picking an ID
Use `level.new.color()` rather than picking an ID by hand. It scans the loaded level and guarantees the returned ID is not already in use. See [New IDs](./new-ids) for details.
:::

## Copying a color channel

Set `copy_id` to make a channel copy its color from another one at runtime. This is the equivalent of the "Copy Color" option in the editor:

```python
channel = level.color[42]
channel.copy_id = color_id.PLAYER_1    # copies P1 color at runtime
channel.copy_opacity = True            # also copies opacity
```

## Player colors

Setting `player` makes a channel follow Player 1 or Player 2's color:

```python
from gmdbuilder import Color

level.color[50] = Color(50, player=1)  # follow P1
level.color[51] = Color(51, player=2)  # follow P2
```

## A complete example

```python
from gmdbuilder import Level, Color, color_id

level = Level.from_file("my_level.gmd")

# Deep purple background
level.color[color_id.BACKGROUND].set_hex("#26064A")

# Slightly lighter ground
level.color[color_id.GROUND].set_hex("#3A0E6E")

# Allocate a new channel for a custom object glow color
glow = level.new.color()
level.color[glow] = Color(int(glow), red=245, green=197, blue=66, opacity=1.0, blending=True)

# Make channel 10 copy P1's color
level.color[10] = Color(10, player=1, copy_opacity=True)

level.export_to_file("my_level_updated.gmd")
```
