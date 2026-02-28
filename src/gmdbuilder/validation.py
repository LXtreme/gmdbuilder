
from functools import lru_cache
from typing import Any, cast
from warnings import warn

from gmdbuilder.fields import SPECIAL_KEYS, TARGET_GROUP_FIELDS, value_is_correct_type, key_is_allowed, int_is_in_range
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



@lru_cache(maxsize=2048)
def _value_is_allowed(k: str, v: Any) -> bool:
    if not value_is_correct_type(k,v):
        return False
    match k:
        case (obj_prop.Trigger.Move.TARGET_ID 
            | obj_prop.Trigger.Move.TARGET_CENTER_ID 
            | obj_prop.Trigger.Move.TARGET_POS
            | obj_prop.Trigger.Pickup.ITEM_ID
            | obj_prop.Trigger.CONTROL_ID
            | obj_prop.COLOR_1
            | obj_prop.COLOR_2
            | obj_prop.Trigger.CollisionBlock.BLOCK_ID):
            return int_is_in_range(v)
        case _:
            pass
            # print(f'placeholder warning: {k!r} : {v!r} is not validated.')
    return True


def validate(key: str, v: Any, obj: dict[str, Any]):
    """immediate validation. to be called by 'level.objects' mutations"""
    obj_id = obj[obj_prop.ID]
    
    if setting.immediate.property_allowed_check:
        if not key_is_allowed(obj_id, key):
            raise ValueError(f"Key {key!r} not allowed for object ID {obj_id}:\n{obj=}")
    
    if not setting.immediate.property_type_check:
        return
    
    ValueNotAllowed = ValueError(f"Invalid value for {key=}:{v=} on object ID {obj_id}:\n{obj=}")
    
    try:
        if not _value_is_allowed(key, v):
            raise ValueNotAllowed
    except TypeError: # Unhashable value
        if s := SPECIAL_KEYS.get(key):
            if not s.is_valid_val(v):
                raise ValueNotAllowed
        else:
            pass
            print(f"placeholder warning: {key} : {v!r} is unhashable and not validated.")