# Getting Started

## Installation

Install the latest release from PyPI:

```bash
pip install gmdbuilder
```

Or install the latest development version directly from GitHub:

```bash
pip install git+https://github.com/LXtreme/gmdbuilder.git
```

Python 3.12 or newer is required.

## IDE setup

gmdbuilder is designed to be used with a type checker. Without one, you lose out on much of the value of the type system.

I heavily recommend [Zed](https://zed.dev/). It is a high-performance feature rich IDE made in rust. More importantly it comes with [basedpyright](https://docs.basedpyright.com/latest/) by default. I personally consider Zed to be a true 'VS Code killer'. However any IDE with good type checking and LSP support will suffice. In VS Code, make sure to have the [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) extension.

A good python LSP setup will give all the static type checking for properties

## Loading a level

There are two ways to load a level instance.

### From a .gmd file (GDShare)

Provide the file path:

```python
from gmdbuilder import Level

level = Level.from_file("my_level.gmd")
```

### From the live editor

This connects to the [WSLiveEditor](https://github.com/maxnut/GDMegaOverlay) running inside GD. In this mode you can push new objects into a running level in real time.

```python
level = Level.from_live_editor()
```

## Objects

Once a level is loaded, `level.objects` gives you the full list of objects as a Python list you can iterate, slice, and filter normally:

```python
all_objects = level.objects
```

Every GD object is represented as a `Typeddict` with string keys in the form `"a<property-int>"`. This unifiies all property keys (including special level keys `"kA<int>"`), and is also a workaround since Python doesnt support Typeddicts for integer keys.

```python
repr(all_objects[0])
# Object({"a1": 1, "a2": 105.0, "a3": 195.0, "a57": {3, 7}, ...})
```

You work with these using the `obj_prop` namespace, which gives every key a readable name:

```python
from gmdbuilder import obj_prop

obj = all_objects[0]
print(obj[obj_prop.X])       # same as obj["a2"]
print(obj[obj_prop.GROUPS])  # same as obj["a57"], returns a set[int]
```

Property keys are organized by trigger type under `obj_prop.Trigger.*`:

```python
obj_prop.Trigger.Move.TARGET_ID   # "a51"
obj_prop.Trigger.Move.DURATION    # "a10"
obj_prop.Trigger.Spawn.DELAY      # "a63"
obj_prop.Trigger.Color.CHANNEL    # "a23"
```

## Validation

Every assignment to an object property is validated immediately — not at export time.

```python
obj[obj_prop.Trigger.Move.DURATION] = "fast"  # raises ValueError: wrong type
obj[obj_prop.X] = 100                         # ok, X accepts int or float
obj[obj_prop.ID] = 999                        # raises KeyError: ID is read-only
```

Validation checks that:
- The key is allowed on this object type
- The value is the correct Python type
- Numeric values are within GD's accepted range

## Exporting

### To a file

```python
# Export to a new file
level.export_to_file("my_level_updated.gmd")

# Export back to the source file (prompts for confirmation)
level.export_to_file()
```

### To the live editor

```python
level.export_to_live_editor()
```

This replaces the full level string in the running editor with the current state of `level.objects` and `level.color`.

## Next steps

- [Add & Edit Objects](./objects) — creating objects, modifying properties, filtering and deleting
- [Colors](./colors) — reading and writing color channels
- [New IDs](./new-ids) — allocating group, item, color, and collision IDs safely
- [Object Types](./object-types) — using TypedDicts and type guards for static type checking