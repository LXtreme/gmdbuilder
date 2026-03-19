![Python Badge](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff&style=for-the-badge)
![Framework](https://img.shields.io/badge/Framework-6A1B9A?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-blue?style=for-the-badge)
![Level Editor](https://img.shields.io/badge/Level%20Editor-424242?style=for-the-badge)

# gmdbuilder
A type-safe general-purpose Python framework for Geometry Dash level editing and scripting.

gmdbuilder lets you:
- Read & write GD levels
- Autoscan to protect against bugs (property types/ranges, spawn limit, no empty triggers, etc.)
- Work directly with triggers, groups, and objects - and choose your own abstractions
- Use pre-built systems and templates to accelerate development
- Know exactly what's happening in your scripts

**gmdbuilder** is developed in collaboration with HDanke, the creator of [gmdkit](https://github.com/UHDanke/gmdkit) (a dependency of this framework) and his unofficial [GD Editor Docs](https://github.com/UHDanke/gd_docs).


## [Documentation (WIP)](https://lxtreme.github.io/gmdbuilder)

*(No overengineered language was made in the making of this project)*


## Why Python?

Python fits surprisingly well as a language for GD scripting:
- Exceptionally good at building/verifying dictionaries (which all GD objects are)
- Operator overloading for counters and other special logic
- Any programming paradigm that you want is well supported
- Reliable type system with good debugger/type-checker tooling
- Huge package ecosystem

## Installation
Install the latest release from PyPI:

```bash
pip install gmdbuilder
```

Install the latest development version from GitHub:

```bash
pip install git+https://github.com/LXtreme/gmdbuilder.git
```

## Getting Started

```python
from gmdbuilder import level

# From .gmd file, supports full object editing/deleting
level.from_file("example.gmd")

# From WSLiveEditor, only supports adidng objects
level.from_live_editor()

obj_list = level.objects # mutations are validated

# Object properties are in the form { "a<key number>": value }
repr(obj_list[1])

from gmdbuilder import obj_prop   # property key str Literals
from gmdbuilder import enum       # enum values for object properties
from gmdbuilder import obj_id     # object ID int Literals

# Similar to 'next' button in the editor.
a = level.new.group()

from gmdbuilder import is_obj_type, is_obj_id, from_object_string, new_obj
import gmdbuilder.object_types as td # TypedDict dictionaries

ppt = obj_prop.Trigger

for obj in obj_list:
    # is_obj_id and is_obj_type are both TypeGuards. 
    # Allows editing generic object lists to be done fully type-safe
    if is_obj_id(obj, obj_id.Trigger.MOVE):
        obj[obj_prop.GROUPS] = { a }
        obj[ppt.Move.EASING] = obj_enum.Easing.NONE
    if is_obj_type(obj, td.MoveType):
        obj[ppt.Move.USE_SMALL_STEP] = True


filter = {
    obj_prop.ID: obj_id.Trigger.COUNT,
    obj_prop.GROUPS: { 15 }
}
obj_list.delete_where(filter)
obj_list.delete_where(lambda obj: obj[ObjProp.ID] == 1)


# CountType is a typed_dict, allowing per-field static type checking
# Translates to { a1: 1611, a2: 50, a3: 45 }
object = from_object_string("1,1611,2,50,3,45;", obj_type=td.CountType)
object[ppt.Count.ACTIVATE_GROUP] = True
object[ppt.Count.TARGET_ID] = a
object["a2"] = 50 # also validated and provides type info

move = new_obj(obj_id.Trigger.MOVE)   # casts to MoveType typed_dict automatically
instant_count = new_obj(1611)         # casts to InstantCountType typed_dict

obj_list.append(object)
obj_list.extend([move, instant_count])

# Wrapper classes and context managers:

from gmdbuilder import level_context, autoappend, targets
from gmdbuilder.classes import Move, Count

with targets(45):
    a = Move() # creates new Move object that targets 45
    a.spawn_trigger = True
    a.easing = 1
    level.objects.append(a.obj)
    
    with level_context(level), autoappend():
        # auto-appended to level, targets 45
        b = Count()
        b.count = 4

# Export object edits, deletions and additions
# Added objects recieve the tag_group
level.export_to_file(file_path="example_updated.gmd")
level.export_to_live_editor()
```
