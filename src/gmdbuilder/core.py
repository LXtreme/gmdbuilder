"""Core utilities for working with ObjectType dicts."""

from typing import TypeGuard, TypeVar

from gmdkit.models.object import Object as KitObject

from . import object_types as td
from .fields import ID_TO_TYPEDDICT
from .mappings import obj_prop
from .level import from_kit_object
from .context import post_object_creation

ObjectType = td.ObjectType

T = TypeVar('T', bound=ObjectType)

def is_obj_type(obj: ObjectType, obj_type: type[T]) -> TypeGuard[T]:
    """Type-narrows obj to a specific TypedDict type by matching its ID."""
    return ID_TO_TYPEDDICT.get(obj.get(obj_prop.ID)) is obj_type


def is_obj_id(obj: ObjectType, object_id: int) -> bool:
    """This basically casts obj to specific ObjectType subclass via type guard"""
    return obj.get(obj_prop.ID) == object_id


def from_object_string(obj_string: str, obj_type: type = ObjectType) -> ObjectType:
    # obj_type is not used bc its only for type narrowing (see stub file `core.pyi`)
    obj = from_kit_object(KitObject.from_string(obj_string))
    post_object_creation(obj)
    return obj 


def new_obj(object_id: int) -> ObjectType:
    # Convert from gmdkit's {1: val, 2: val} to our {'a1': val, 'a2': val}
    obj = from_kit_object(KitObject.default(object_id))
    post_object_creation(obj)
    return obj

