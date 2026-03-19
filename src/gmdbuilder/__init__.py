
from .level import Level
from .id import NamedInt
from . import context
from .context import (
    level_context,
    autoappend,
    transform,
    targets,
    groups,
    set_prop
)

from .core import (
    new_obj,
    from_object_string,
    is_obj_type,
    is_obj_id,
)

from .validation import setting

from . import object_types as td
from .object_types import AllPropsType, ObjectType

from .object import ObjectList

from .color import Color

from .mappings import obj_prop
from .mappings import obj_id
from .mappings import color_prop
from .mappings import color_id
from .mappings import lvl_prop
from .mappings import obj_enum as enum


# ---------------------------------------------------------------------------
# Explicit public surface
# ---------------------------------------------------------------------------

__all__ = [
    "Level",
    # Context
    "context",
    "level_context",
    "autoappend",
    "transform",
    "targets",
    "groups",
    "set_prop",
    # Object
    "ObjectList",
    # ID allocation
    "NamedInt",
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
