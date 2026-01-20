# kit_interface Module

**Internal bridge between gmdkit and GMDBuilder's type-safe API.**

## Purpose

This module converts between:
- **String keys** (`"a1"`, `"a2"`, `"a3"`) used by GMDBuilder's TypedDicts
- **Integer keys** (`1`, `2`, `3`) used by gmdkit

## DO NOT USE DIRECTLY

Users should **never** import from `kit_interface`. It's only used internally by `Object` and `Level` classes.

## Key Functions

### Key Conversion
- `string_key_to_int()` - `"a2"` → `2`
- `int_key_to_string()` - `2` → `"a2"`

### Object Conversion
- `raw_to_typed()` - `{1: val, 2: val}` → `{"a1": val, "a2": val}`
- `typed_to_raw()` - `{"a1": val, "a2": val}` → `{1: val, 2: val}`
- `kit_object_to_typed()` - KitObject → TypedDict
- `typed_to_kit_object()` - TypedDict → KitObject

### Level Operations
- `load_level_from_file()` - Wrap gmdkit's file loading
- `save_level_to_file()` - Wrap gmdkit's file saving
- `get_level_objects()` - Extract objects from KitLevel as TypedDicts
- `set_level_objects()` - Inject TypedDicts into KitLevel

### Defaults
- `get_object_defaults()` - Get default properties for object ID

## How It Works

```
User Code:
    obj[ObjProp.X] = 100  # ObjProp.X = "a2"
    
Object class:
    self._dict["a2"] = 100  # Stores as TypedDict
    
When saving (via kit_interface):
    typed_to_raw({"a2": 100})  → {2: 100}
    → gmdkit receives {2: 100}
```

## Architecture

```
User Code (type-safe)
    ↓
Level & Object (public API)
    ↓
kit_interface (internal bridge) ← YOU ARE HERE
    ↓
gmdkit (raw dicts with int keys)
```

## Adding New Features

If you need gmdkit functionality:
1. Add function to `kit_interface.py`
2. Call it from `Level` or `Object` classes
3. Never expose it to users directly

Example:
```python
# In kit_interface.py
def get_replay_data(kit_level: KitLevel) -> list[int]:
    replay_string = kit_level.get(34)  # Property 34
    return replay_string.data if replay_string else []

# In level.py
def get_replay(self) -> list[int]:
    """Get replay data."""
    from gmdbuilder.kit_interface import get_replay_data
    return get_replay_data(self._kit_level)
```
