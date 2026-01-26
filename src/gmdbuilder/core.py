"""Core utilities for working with ObjectType dicts."""

from typing import Any, Literal, overload
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
            try:
                assert key.startswith('a')
                int_key = int(key[1:])
                raw[int_key] = value
            except (AssertionError, ValueError):
                raise TypeError(f"Can't convert object with invalid non-'a<int>' keys: \n{obj}")
        else:
            raw[key] = value
    
    return raw


def from_raw_object(raw_obj: dict[int, Any]) -> ObjectType:
    """
    Convert raw int-keyed dict from gmdkit to ObjectType.
    
    Example:
        {1: 900, 2: 50} → {'a1': 900, 'a2': 50}
    """
    converted: ObjectType = { 'a1': -1 }
    
    for key, value in raw_obj.items():
        if isinstance(key, int):
            str_key = f'a{key}'
            converted[str_key] = value
        else:
            raise TypeError(f"Can't convert object with invalid non-int keys: \n{raw_obj}")
    
    if converted['a1'] == -1:
        raise TypeError("Missing required Object ID key 1 in raw object")
    
    return converted


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
    return from_raw_object(KitObject.default(object_id))
