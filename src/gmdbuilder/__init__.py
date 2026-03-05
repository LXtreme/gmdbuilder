"""
gmdbuilder - A type-safe API for building Geometry Dash levels.

Public API surface:

  Loading a level
  ---------------
  Level                 - Level.from_file(...) / Level.from_live_editor(...)
  ObjectList            - the list of objects on a level (level.objects)

  Creating / inspecting objects
  -----------------------------
  new_obj               - create a new object with default properties by ID
  from_object_string    - parse a raw GD object string into an ObjectType dict
  is_obj_type           - TypeGuard: narrow an object to a specific TypedDict subclass
  is_obj_id             - check whether an object has a given integer ID

  Validation settings
  -------------------
  setting               - module-level validation toggle flags

  Mapping namespaces (string/int constants for object properties and IDs)
  -----------------------------------------------------------------------
  obj_prop       object property keys      (gmdbuilder.mappings.obj_prop)
  obj_id         object integer IDs        (gmdbuilder.mappings.obj_id)
  color_id       color channel IDs         (gmdbuilder.mappings.color_id)
  color_prop     color property keys       (gmdbuilder.mappings.color_prop)
  lvl_prop       level property keys       (gmdbuilder.mappings.lvl_prop)
  enum           object property values    (gmdbuilder.mappings.obj_enum)
"""

from gmdbuilder.level import (
    Level,
    ObjectList,
)

from gmdbuilder.core import (
    new_obj,
    from_object_string,
    is_obj_type,
    is_obj_id,
)

from gmdbuilder.validation import setting

import gmdbuilder.object_types as td
from gmdbuilder.object_types import AllPropsType, ObjectType

from gmdbuilder.color import Color

from gmdbuilder.mappings import obj_prop
from gmdbuilder.mappings import obj_id
from gmdbuilder.mappings import color_prop
from gmdbuilder.mappings import color_id
from gmdbuilder.mappings import lvl_prop
from gmdbuilder.mappings import obj_enum as enum

# ---------------------------------------------------------------------------
# Explicit public surface
# ---------------------------------------------------------------------------

__all__ = [
    # Level lifecycle
    "Level",
    "ObjectList",
    # Core helpers
    "new_obj",
    "from_object_string",
    "is_obj_type",
    "is_obj_id",
    # Validation
    "setting",
    # Color
    "Color",
    # TypedDicts
    "td",
    "AllPropsType",
    "ObjectType",
    # Mapping namespaces
    "obj_prop",
    "obj_id",
    "color_id",
    "color_prop",
    "lvl_prop",
    "enum",
]