
from functools import lru_cache
from typing import Any

from gmdbuilder.fields import COMMON_ALLOWED_KEYS, ID_TO_ALLOWED_KEYS, value_is_correct_type
from gmdbuilder.mappings import obj_prop
from gmdbuilder.object_types import ObjectType

class setting:
    class immediate:
        property_allowed_check = True
        """Checks that all property keys are allowed on the given object ID."""
        
        property_type_check = True
        """Checks that all property value types and ranges are correct"""

    class export:
        target_exists_check = True
        """Checks that all targets referenced by triggers actually exist"""
        
        solid_target_check = True
        """Checks that visual-related triggers target non-trigger & visible groups/objects"""
        
        spawn_limit_check = True
        """Checks for any spawn-limit occurrance within trigger execution chains"""
        
        group_parent_check = True
        """Checks that every group parent is unique (no two parents for 1 ID)"""


class ValidationError(Exception):
    def __init__(self, msg: str, deferred: bool = False):
        self.deferred = deferred
        self.context: dict[str, Any] = {}
        super().__init__(msg)
    
    def add_context(self, **kwargs: Any):
        self.context.update(kwargs)
        return self
    
    def __str__(self) -> str:
        msg = super().__str__()
        if self.context:
            context_str = "\n".join(f"  {k}: {v}" for k, v in self.context.items())
            return f"{msg}\n{context_str}"
        return msg


# def typeddict_keys(td) -> set[str]:
#     return set(getattr(td, "__required_keys__", set())) | set(getattr(td, "__optional_keys__", set()))

# DEFAULT_ALLOWED = typeddict_keys(ObjectType)
# ALLOWED_BY_ID = {k: typeddict_keys(v) for k, v in ID_TO_TYPEDDICT.items()}


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
            if not value_is_correct_type(k,v):
                 raise ValueError(f"Value {v!r} is not the correct type.")
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


def export_validation(final_object_list: list[ObjectType]):
    """to be called in level.export"""
    pass