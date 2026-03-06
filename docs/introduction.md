# Introduction

gmdbuilder is a Python framework for reading, editing, and exporting Geometry Dash levels programmatically. Instead of clicking through the GD editor, you write a script — and the framework handles validation, ID management, and serialization for you.

It is built on top of [gmdkit](https://github.com/UHDanke/gmdkit), a low-level GD serialization library by HDanke, and extends it with a type-safe, developer-friendly API.

## What it's for

gmdbuilder is the right tool when you want to:

- **Automate repetitive level construction** — place hundreds of objects with precise positions, groups, and properties that would take hours to set manually.
- **Write reusable level components** — define a function that builds a trigger setup once, call it anywhere.
- **Transform existing levels** — load a `.gmd` file, filter or modify objects by property, and export the result.
- **Work with the live editor** — push changes into GD while it's running, without saving or reopening files.
- **Script complex logic** — counters, spawn chains, collision systems — anything that's easier to reason about in code than in the editor.

## What it's not for

gmdbuilder is not a visual editor and does not try to be one. It won't show you a canvas or let you drag objects around. It's a scripting framework for people comfortable writing Python.

## How objects work

Every GD level object is represented as a plain Python `dict` with string keys in the form `"a<number>"`:

```python
# A move trigger at position (100, 200) with group 5
{
    "a1":  901,     # object ID  (move trigger)
    "a2":  100.0,   # X position
    "a3":  200.0,   # Y position
    "a57": {5},     # groups     (a set of ints)
    "a10": 0.5,     # duration
    "a51": 5,       # target group ID
}
```

You never construct these by hand. You use `new_obj()` to create one from its ID, and the `obj_prop` namespace to write properties with readable names instead of raw key strings:

```python
from gmdbuilder import new_obj, obj_prop, obj_id

trigger = new_obj(obj_id.Trigger.MOVE)
trigger[obj_prop.X]                      = 100
trigger[obj_prop.Trigger.Move.DURATION]  = 0.5
trigger[obj_prop.Trigger.Move.TARGET_ID] = 5
```

Every assignment is validated immediately. If you pass the wrong type, a value out of range, or a key that doesn't belong on that object, you get an error at that line — not silently at export.

## Project design goals

**Correctness over convenience.** Validation happens at write time. You find out about bad values where you introduced them, not somewhere downstream.

**No magic.** Objects are dicts. Lists are lists. The framework intercepts mutations for validation, but you can use all normal Python idioms — list comprehensions, `next()`, unpacking, whatever you'd normally reach for.

**Good static analysis.** The framework ships a `.pyi` stub and uses TypedDict subclasses per trigger type, so a type checker like Pylance or basedpyright can catch type errors in your script before you ever run it.

**Stays out of the way.** You control the structure of your script. gmdbuilder doesn't impose a project layout, a build step, or any particular abstraction on top of levels. It's a library, not a framework you build inside.

## Relationship to gmdkit

[gmdkit](https://github.com/UHDanke/gmdkit) handles the low-level work: parsing GD's binary/compressed level format, serializing objects back to strings, and modeling the raw data structures. gmdbuilder sits on top of it and provides the type-safe, developer-facing API.

You generally won't need to interact with gmdkit directly. If you find yourself needing something gmdbuilder doesn't expose, the underlying `KitLevel`, `KitObject`, and related types are accessible via the internal `_kit_level` attribute on a loaded `Level`.