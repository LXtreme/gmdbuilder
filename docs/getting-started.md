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

gmdbuilder is designed to be used with a type checker. Without one, you lose most of the value of the typed object system.

The recommended setup is **VS Code** with the [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) extension (bundled with the Python extension), or any editor running [basedpyright](https://github.com/DetachHead/basedpyright). Both understand TypedDicts, overloads, and TypeGuards — all of which gmdbuilder uses heavily.

Once configured, you'll get:
- Autocomplete on `obj_prop`, `obj_id`, and `obj_enum` namespaces
- Inline type errors when you assign a wrong type to an object property
- Narrowed types when you use `is_obj_type()` or `is_obj_id()` as guards

::: tip
If you're using VS Code, set `"python.analysis.typeCheckingMode": "basic"` in your settings to enable inline diagnostics without being too strict on your own code.
:::

## Loading a level

There are two ways to load a level.

### From a .gmd file

This is the standard mode. You get full read/write access to all objects in the level.

```python
from gmdbuilder import Level

level = Level.from_file("my_level.gmd")
```

Pass a `tag_group` to control which group is used internally to track objects added by your script. The default is `9999`. On load, any object already carrying that group is filtered out (cleaning up from a previous script run). On export, every object your script appends gets that group added automatically so the next run can clean it up again.

```python
level = Level.from_file("my_level.gmd", tag_group=9999)
```

### From the live editor

This connects to the [WSLiveEditor](https://github.com/maxnut/GDMegaOverlay) running inside GD. In this mode you can push new objects into a running level in real time.

```python
level = Level.from_live_editor()
```

## The object list

Once a level is loaded, `level.objects` gives you the full list of objects as a Python list you can iterate, slice, and filter normally:

```python
all_objects = level.objects

print(len(all_objects))         # number of objects
print(all_objects[0])           # first object as a dict

for obj in all_objects:
    print(obj)
```

## What objects look like

Every GD object is a plain Python `dict` with string keys in the form `"a<number>"`, corresponding to GD's internal property numbering:

```python
repr(all_objects[0])
# {"a1": 1, "a2": 105.0, "a3": 195.0, "a57": {3, 7}, ...}
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

You can tune validation behaviour globally via the `setting` class:

```python
from gmdbuilder import setting

setting.property_type_check    = True   # on by default
setting.property_allowed_check = True   # on by default
setting.target_exists_check    = False  # off by default
```

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