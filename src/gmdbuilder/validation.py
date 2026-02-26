
from functools import lru_cache
from typing import Any, cast
from warnings import warn

from gmdbuilder.fields import COMMON_ALLOWED_KEYS, ID_TO_ALLOWED_KEYS, TARGET_GROUP_FIELDS, value_is_correct_type
from gmdbuilder.mappings import obj_prop
from gmdbuilder.object_types import AllPropsType, ObjectType



class setting:
    class immediate:
        property_allowed_check = True
        """Checks that all property keys are allowed on the given object ID."""
        
        property_type_check = True
        """Checks that all property value types and ranges are correct"""

    class export:
        target_exists_check = False
        """Checks that all targets referenced by triggers actually exist"""
        
        solid_target_check = False
        """Checks that visual-related triggers target non-trigger & visible groups/objects"""
        
        spawn_limit_check = True
        """Checks for any spawn-limit occurrance within trigger execution chains"""
        
        group_parent_check = True
        """Checks that every group parent is unique (no two parents for 1 ID)"""



def get_trigger_targets(objects: list[ObjectType]):
    targeted: dict[int, list[ObjectType]] = {}
    used: dict[int, list[ObjectType]] = {}
    
    for obj in objects:
        obj = cast(AllPropsType, obj)
        
        if gs := obj.get(obj_prop.GROUPS):
            for g in gs:
                used.setdefault(g, []).append(obj)
        
        if r := obj.get(obj_prop.Trigger.Spawn.REMAPS):
            for source, target in r.items():
                used.setdefault(target, []).append(obj)
                used.setdefault(source, []).append(obj)
        for key in obj.keys():
            if key in TARGET_GROUP_FIELDS:
                group = cast(int, obj[key])
                targeted.setdefault(group, []).append(obj)
    
    return targeted, used


def validate_target_exists(
    targeted: dict[int, list[ObjectType]], 
    used: dict[int, list[ObjectType]]
):
    """Note: Does not check for special cases like Pulse's color IDs (yet)"""
    if not setting.export.target_exists_check:
        return
    
    targeted_groups = set(targeted.keys())
    used_groups = set(used.keys())
    empty_groups = targeted_groups.difference(used_groups)
    
    if empty_groups:
        guilty = [f"{o}\n" for g in empty_groups for o in targeted[g]]
        warn(
            f"\nTARGET-EXISTS CHECK FAILED:\n"
            f"To disable this check, set 'setting.export.target_exists_check' to False.\n\n"
            f"DETAILS:\n"
            f"Some triggers target groups, which is don't exist:\n"
            f"Empty groups: \n{sorted(empty_groups)}\n"
            f"Offending triggers:\n{''.join(guilty)}"
        )


def validate_solid_targets(
    targeted: dict[int, list[ObjectType]], 
    used: dict[int, list[ObjectType]]
):
    if not setting.export.solid_target_check:
        return
    raise NotImplementedError("Solid target check is not implemented yet.")



@lru_cache(maxsize=1024)
def _assert_int_in_range(v: Any, min_val: int = 0, max_val: int = 9999):
    if not (isinstance(v, int) and min_val <= v <= max_val):
        raise ValueError(f"Key must be an int in range {min_val}-{max_val}, got {v!r}")


@lru_cache(maxsize=1024)
def _validate_key_allowed(obj_id: int, key: str):
    if key not in COMMON_ALLOWED_KEYS and key not in ID_TO_ALLOWED_KEYS.get(obj_id, {}):
        raise ValueError(f"Key {key} is not allowed for object ID {obj_id}")


@lru_cache(maxsize=1024)
def _validate_key_value(k: str, v: Any):
    if not value_is_correct_type(k,v):
        raise ValueError(f"Value {v!r} is not the correct type.")
    match k:
        case (obj_prop.Trigger.Move.TARGET_ID 
            | obj_prop.Trigger.Move.TARGET_CENTER_ID 
            | obj_prop.Trigger.Move.TARGET_POS
            | obj_prop.Trigger.Pickup.ITEM_ID
            | obj_prop.Trigger.CONTROL_ID
            | obj_prop.COLOR_1
            | obj_prop.COLOR_2
            | obj_prop.Trigger.CollisionBlock.BLOCK_ID):
            _assert_int_in_range(v)
        case _:
            pass
            # print(f'placeholder warning: {k!r} : {v!r} is not validated.')


def validate(key: str, v: Any, obj: dict[str, Any]):
    """immediate validation. to be called by 'level.objects' mutations"""
    obj_id = obj[obj_prop.ID]
    
    try:
        if setting.immediate.property_allowed_check:
            _validate_key_allowed(obj_id, key)
    except ValueError:
        raise ValueError(f"Key {key!r} not allowed for object ID {obj_id}.\n{obj=}") from None
    
    try:
        if setting.immediate.property_type_check:
            _validate_key_value(key, v)
    except ValueError as e: # from _validate_key_value or _assert_int_in_range
        raise ValueError(f"Invalid value for key {key!r} on object ID {obj_id}: {v!r}\n{obj=}") from e
    except TypeError: # Unhashable value
        match key:
            case obj_prop.GROUPS | obj_prop.PARENT_GROUPS:
                for group_id in v:
                    _assert_int_in_range(group_id)
            case obj_prop.Trigger.Event.EVENTS:
                for event_id in v:
                    if not isinstance(event_id, int) or not (0 <= event_id <= 80):
                        raise ValueError(f"Event IDs must be non-negative integers, got {event_id!r}")
            case obj_prop.Trigger.Spawn.REMAPS:
                for source, target in v.items():
                    _assert_int_in_range(source)
                    _assert_int_in_range(target)
            
            # will add gmdkit's hsv dataclass and write validation for that later
            case obj_prop.HSV_1 | obj_prop.HSV_2 | obj_prop.Trigger.Pulse.HSV:
                pass
            case obj_prop.Particle.DATA:
                pass
            case obj_prop.Trigger.AdvRandom.TARGETS:
                # for source, target in v:
                    pass
            case _:
                print(f"placeholder warning: {key} : {v!r} is unhashable and not validated.")
