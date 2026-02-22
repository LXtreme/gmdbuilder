![Python Badge](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff&style=for-the-badge)
![Framework](https://img.shields.io/badge/Framework-6A1B9A?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-blue?style=for-the-badge)
![Level Editor](https://img.shields.io/badge/Level%20Editor-424242?style=for-the-badge)

# gmdbuilder
A type-safe general-purpose Python framework for pragmatic Geometry Dash level editing and scripting.

gmdbuilder lets you:
- Read & write Geometry Dash levels
- Automatically scan and protect against bugs (property types/ranges, spawn limit, etc.)
- Work directly with triggers, groups, and objects - and choose your own abstractions
- Use pre-built systems and templates to accelerate development

**gmdbuilder** is developed in collaboration with HDanke, the creator of **gmdkit** (a dependency of this framework) and his unofficial **GD Editor Docs**.

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

# This group gets deleted at level-load and automatically added to new objects at level-export
level.tag_group = 9999 # Set to 9999 by default

# From .gmd file, supports full object editing/deleting
level.from_file("example.gmd")

# From WSLiveEditor, only supports adidng objects
level.from_live_editor()

obj_list = level.objects # mutations are validated

# Object properties are in the form { "a<key number>": value }
repr(obj_list[1])

# Object ID and Property enums (all values are Literal) 
from gmdbuilder.mappings.obj_prop import ObjProp
from gmdbuilder.mappings.obj_id import ObjId

for obj in obj_list:
    if obj[ObjProp.ID] == ObjID.Trigger.MOVE:
        obj[ObjProp.GROUPS] = {}
    elif obj[ObjProp.ID] == ObjID.Trigger.COUNT:
        obj_list.remove(obj)

# Translates to { a1: 1 }
block = from_raw_object({1: 1})

obj_list.delete_where(block)
obj_list.delete_where(lambda obj: obj[ObjProp.ID] == 1)

# Translates to { a1: 1611, a2: 50, a3: 45 }
object = from_object_string("1,1611,2,50,3,45;", obj_type=CountType)
object[ObjProp.Trigger.Count.ACTIVATE_GROUP] = True

# Export object edits, deletions and additions
level.export_to_file(file_path="example_updated.gmd")

# Export added objects to WSLiveEditor
level.export_to_live_editor()
```
