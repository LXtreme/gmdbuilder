"""Core utilities for working with ObjectType dicts."""

from functools import lru_cache
from typing import Any, Literal, cast, overload
from gmdkit.models.object import Object as KitObject
from gmdbuilder.mappings.obj_prop import ObjProp
from gmdbuilder.validation import setting
from gmdbuilder.futils import translate_list_string, translate_map_string
from gmdbuilder.object_typeddict import AdvFollowType, MoveType, ObjectType, RotateType
from gmdbuilder.object_types import Object

@lru_cache(maxsize=1024)
def _to_raw_key_cached(key: object) -> int | str:
    if isinstance(key, int):
        return key
    if not isinstance(key, str):
        raise ValueError()
    if key.startswith('k'):
        return key
    if key.startswith('a'):
        tail = key[1:]
        if tail.isdigit():
            return int(tail)
    raise ValueError()

def to_raw_object(obj: ObjectType) -> dict[int|str, Any]:
    """
    Convert ObjectType to a new raw int-keyed dict for gmdkit or debugging.
    
    Example:
        {'a1': 900, 'a2': 50} → {1: 900, 2: 50}
    """
    raw: dict[int|str, Any] = {}
    for key, value in obj.items():
        value = cast(Any, value)
        if key == ObjProp.GROUPS:
            value = '.'.join(map(str, sorted(value)))
        elif key == ObjProp.Trigger.Event.EVENTS:
            value = '.'.join(map(str, sorted(value)))
        
        try:
            raw[_to_raw_key_cached(key)] = value
        except ValueError as e:
            raise ValueError(f"Object has bad/unsupported key {key!r}: {obj=}") from e
    return raw


@lru_cache(maxsize=1024)
def _from_raw_key_cached(key: object) -> str:
    if isinstance(key, int):
        return f"a{key}"
    if isinstance(key, str) and (key.startswith("a") or key.startswith("k")):
        return key
    raise ValueError()

def from_raw_object(raw_obj: dict[int|str, Any], bypass_validation: bool = False) -> ObjectType:
    """
    Convert raw int-keyed dict from gmdkit to a new ObjectType.
    
    Example:
        {1: 900, 2: 50} → {'a1': 900, 'a2': 50}
    """
    
    if (key := ObjProp.GROUPS) in raw_obj:
        raw_obj[key] = translate_list_string(raw_obj[key])
    if (key := ObjProp.Trigger.Spawn.REMAPS) in raw_obj:
        raw_obj[key] = translate_map_string(raw_obj[key])
    
    converted: ObjectType = { ObjProp.ID: -1 }
    
    for key, value in raw_obj.items():
        try:
            converted[_from_raw_key_cached(key)] = value
        except ValueError as e:
            raise ValueError(f"Object has bad/unsupported key {key!r}: {raw_obj=}") from e
    
    if int(converted[ObjProp.ID]) == -1:
        raise TypeError(f"Missing required Object ID key 1 in raw object: \n{raw_obj=}")
    
    if setting.export_solid_target_check and not bypass_validation:
        wrapped = Object(converted[ObjProp.ID])
        wrapped.update(converted)
        return cast(ObjectType, wrapped)
    return converted


def from_object_string(obj_string: str) -> ObjectType:
    """
    Convert GD level object string to ObjectType.
    
    Example:
        "1,1,2,50,3,45;" → {'a1': 1, 'a2': 50, 'a3': 45}
    """
    raw_obj = kit_to_raw_obj(KitObject.from_string(obj_string)) # type: ignore
    return from_raw_object(raw_obj)


def kit_to_raw_obj(obj: dict[int|str, Any]) -> dict[int|str, Any]:
    """Mutates KitObject for specific props like 'group' to normal representation"""
    
    if (k := ObjProp.GROUPS) in obj:
        obj[k] = '.'.join(map(str, sorted(obj[k])))
    if (k := ObjProp.Trigger.Spawn.REMAPS) in obj:
        raise ValueError(f"found kit remaps: \n\n{obj[k]=}\n\n")
    
    return obj


@overload
def new_object(object_id: Literal[3016]) -> AdvFollowType: ...
@overload
def new_object(object_id: Literal[1346]) -> RotateType: ...
@overload
def new_object(object_id: Literal[901]) -> MoveType: ...
@overload
def new_object(object_id: int) -> ObjectType: ...
def new_object(object_id: int) -> ObjectType:
    """
    Create a new Object with defaults from gmdkit.
        
    Returns:
        ObjectType dict with default properties (using 'a<num>' keys)
    """
    # Convert from gmdkit's {1: val, 2: val} to our {'a1': val, 'a2': val}
    return from_raw_object(kit_to_raw_obj(KitObject.default(object_id))) # type: ignore
