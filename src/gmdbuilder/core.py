"""Core utilities for working with ObjectType dicts."""

from typing import Any, Literal, cast, overload
from gmdbuilder.internal_mappings.obj_prop import ObjProp
from gmdbuilder.validation import ValidatedObject, setting
from gmdbuilder.internal_mappings.obj_id import ObjId
from gmdkit.models.object import Object as KitObject
from gmdbuilder.object_types import AdvFollowType, MoveType, ObjectType, RotateType

def to_raw_object(obj: ObjectType) -> dict[int, Any]:
    """
    Convert ObjectType to raw int-keyed dict for gmdkit or debugging.
    
    Example:
        {'a1': 900, 'a2': 50} → {1: 900, 2: 50}
    """
    raw: dict[int, Any] = {}
    
    for key, value in obj.items():
        if isinstance(key, str):
            if key.startswith('a'):
                int_key = int(key[1:])
                raw[int_key] = value
        else:
            raw[key] = value
    
    return raw


def from_raw_object(raw_obj: dict[int, Any], bypass_check: bool = False) -> ObjectType:
    """
    Convert raw int-keyed dict from gmdkit to ObjectType.
    
    Example:
        {1: 900, 2: 50} → {'a1': 900, 'a2': 50}
    """
    converted: ObjectType = { ObjProp.ID: -1 }
    
    for key, value in raw_obj.items():
        if not isinstance(key, int):
            raise TypeError(f"Can't convert object with invalid non-int keys: \n{raw_obj}")
        
        converted[f'a{key}'] = value
    
    if int(converted[ObjProp.ID]) == -1:
        raise TypeError(f"Missing required Object ID key 1 in raw object: \n{raw_obj}")
    
    if setting.export_solid_target_check and not bypass_check:
        wrapped = ValidatedObject(converted[ObjProp.ID])
        wrapped.update(converted)
        return cast(ObjectType, wrapped)
    return cast(ObjectType, converted)


def from_object_string(obj_string: str) -> ObjectType:
    """
    Convert GD level object string to ObjectType.
    
    Args:
        obj_string: GD format string like "1,1,2,50,3,45;"
    
    Example:
        "1,1,2,50,3,45;" → {'a1': 1, 'a2': 50.0, 'a3': 45.0}
    """
    # Use gmdkit to parse the string
    return from_raw_object(KitObject.from_string(obj_string))


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
    obj = from_raw_object(KitObject.default(object_id))
    match object_id:
        case ObjId.Trigger.MOVE:
            return cast(MoveType, obj)
        case ObjId.Trigger.ROTATE:
            return cast(RotateType, obj)
        case _:
            return cast(ObjectType, obj)
