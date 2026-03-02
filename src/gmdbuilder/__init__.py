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
  Object                - the underlying validated dict class (subclass of dict)

  ID allocation
  -------------
  IDAllocator           - allocate unique group / item / color / collision / control IDs

  Validation settings
  -------------------
  setting               - module-level validation toggle flags

  Mapping namespaces (string/int constants for object properties and IDs)
  -----------------------------------------------------------------------
  prop           object property keys      (gmdbuilder.mappings.obj_prop)
  obj            object integer IDs        (gmdbuilder.mappings.obj_id)
  color          color channel IDs         (gmdbuilder.mappings.color_id)
  color_prop     color property keys       (gmdbuilder.mappings.color_prop)
  lvl_prop       level property keys       (gmdbuilder.mappings.lvl_prop)
  enum           object property values    (gmdbuilder.mappings.obj_enum)
"""

from gmdbuilder.level import (
    Level,
    ObjectList,
)

from gmdbuilder.core import (
    Object,
    new_obj,
    from_object_string,
    from_kit_object,
    to_kit_object,
    is_obj_type,
    is_obj_id,
)

from gmdbuilder.validation import setting

from gmdbuilder.object_types import AllPropsType, ObjectType

from gmdbuilder.mappings import obj_prop
from gmdbuilder.mappings import obj_id
from gmdbuilder.mappings import color_prop
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
    "Object",
    "new_obj",
    "from_object_string",
    "from_kit_object",
    "to_kit_object",
    "is_obj_type",
    "is_obj_id",
    # Validation
    "setting",
    # TypedDicts
    "AllPropsType",
    "ObjectType",
    # Mapping namespaces
    "obj_prop",
    "obj_id",
    "color_prop",
    "lvl_prop",
    # Enums
    "enum",
]