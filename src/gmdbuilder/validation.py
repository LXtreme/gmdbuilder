
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
                used[g] = used.get(g, []) + [obj]
        
        if r := obj.get(obj_prop.Trigger.Spawn.REMAPS):
            for source, target in r.items():
                used[target] = used.get(target, []) + [obj]
                used[source] = used.get(source, []) + [obj]
        for key in obj.keys():
            if key in TARGET_GROUP_FIELDS:
                group = cast(int, obj[key])
                targeted[group] = targeted.get(group, []) + [obj]
    
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



@lru_cache(maxsize=None)
def _assert_int_in_range(v: Any, min_val: int = 1, max_val: int = 9999):
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
        case _: pass
    # print(f'placeholder warning: {k!r} : {v!r} is not validated.')


def validate(obj_id: int, key: str, v: Any):
    """immediate validation. to be called by 'level.objects' mutations"""
    
    try:
        if setting.immediate.property_allowed_check:
            _validate_key_allowed(obj_id, key)
        if setting.immediate.property_type_check:
            _validate_key_value(key, v)
    except ValueError as e:
        raise ValueError(f"Invalid value for key {key!r} on object ID {obj_id}: {v!r}") from e
    except TypeError: # Unhashable value
        match key:
            case obj_prop.GROUPS:
                for group_id in v:
                    _assert_int_in_range(group_id)
            case obj_prop.PARENT_GROUPS:
                for group_id in v:
                    _assert_int_in_range(group_id)
            case obj_prop.Trigger.Spawn.REMAPS:
                for source, target in v.items():
                    _assert_int_in_range(source)
                    _assert_int_in_range(target)
            case _:
                ...
                # print(f"placeholder warning: {key} : {v!r} is not validated.")
