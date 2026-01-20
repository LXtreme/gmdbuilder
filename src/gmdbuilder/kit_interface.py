"""
Internal bridge between gmdkit and gmdbuilder's type-safe interfaces.

NOT for end users. Only used internally by Object and Level classes.
"""

from typing import Any, TypeAlias, cast

from gmdkit.models.level import Level as KitLevel  # type: ignore
from gmdkit.models.object import Object as KitObject, ObjectList as KitObjectList  # type: ignore
from gmdkit.defaults.objects import OBJECT_DEFAULT  # type: ignore

from gmdbuilder.object_types import ObjectType

RawObjectDict: TypeAlias = dict[int, Any]
TypedObjectDict: TypeAlias = ObjectType


# Key conversion: "a2" <-> 2
def string_key_to_int(key: str) -> int:
    if key.startswith('a') and len(key) > 1:
        return int(key[1:])
    raise ValueError(f"Invalid string key format: {key}")


def int_key_to_string(key: int) -> str:
    return f"a{key}"


# TypedDict <-> Raw Dict conversion
def raw_to_typed(raw_obj: RawObjectDict | KitObject) -> TypedObjectDict:
    """Convert gmdkit object {1: val, 2: val} to TypedDict {"a1": val, "a2": val}"""
    typed_obj: dict[str, Any] = {}
    
    if isinstance(raw_obj, KitObject):
        raw_obj = dict(raw_obj)
    
    for int_key, value in raw_obj.items():
        string_key = int_key_to_string(int_key)
        typed_obj[string_key] = value
    
    return cast(TypedObjectDict, typed_obj)


def typed_to_raw(typed_obj: TypedObjectDict) -> RawObjectDict:
    """Convert TypedDict {"a1": val, "a2": val} to gmdkit format {1: val, 2: val}"""
    raw_obj: RawObjectDict = {}
    
    for string_key, value in typed_obj.items():
        int_key = string_key_to_int(string_key)
        raw_obj[int_key] = value
    
    return raw_obj


# KitObject conversion
def kit_object_to_typed(kit_obj: KitObject) -> TypedObjectDict:
    return raw_to_typed(kit_obj)


def typed_to_kit_object(typed_obj: TypedObjectDict) -> KitObject:
    raw_obj = typed_to_raw(typed_obj)
    kit_obj = KitObject()
    kit_obj.update(raw_obj)
    return kit_obj


# ObjectList conversion
def kit_object_list_to_typed(kit_list: KitObjectList) -> list[TypedObjectDict]:
    return [kit_object_to_typed(obj) for obj in kit_list]


def typed_to_kit_object_list(typed_list: list[TypedObjectDict]) -> KitObjectList:
    kit_list = KitObjectList()
    for typed_obj in typed_list:
        kit_obj = typed_to_kit_object(typed_obj)
        kit_list.append(kit_obj)
    return kit_list


# Get defaults from gmdkit
def get_object_defaults(object_id: int) -> TypedObjectDict:
    raw_defaults = OBJECT_DEFAULT.get(object_id, {})
    typed_defaults = raw_to_typed(raw_defaults)
    typed_defaults["a1"] = object_id  # Ensure ID is set
    return typed_defaults


# Level file I/O
def load_level_from_file(file_path: str) -> KitLevel:
    return KitLevel.from_file(file_path)


def save_level_to_file(kit_level: KitLevel, file_path: str) -> None:
    kit_level.to_file(file_path)


# Level object extraction/injection
def get_level_objects(kit_level: KitLevel) -> list[TypedObjectDict]:
    object_string = kit_level.get(4)  # Property 4 = OBJECT_STRING
    
    if object_string is None or not hasattr(object_string, 'objects'):
        return []
    
    return kit_object_list_to_typed(object_string.objects)


def set_level_objects(kit_level: KitLevel, typed_objects: list[TypedObjectDict]) -> None:
    kit_list = typed_to_kit_object_list(typed_objects)
    
    object_string = kit_level.get(4)
    
    if object_string is None:
        from gmdkit.models.prop.gzip import ObjectString  # type: ignore
        object_string = ObjectString()
        kit_level[4] = object_string
    
    object_string.objects = kit_list