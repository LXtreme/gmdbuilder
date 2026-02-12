
from functools import lru_cache
from typing import Any, TYPE_CHECKING
from gmdbuilder.mappings.obj_prop import ObjProp

if TYPE_CHECKING:
    from gmdbuilder.object_typeddict import ObjectType

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


def validate_obj(obj: ObjectType):
    obj_id = obj[ObjProp.ID]
    for k, v in obj.items(): validate(obj_id, k, v)


@lru_cache(maxsize=1024)
def _validate_key_value(k: str, v: Any):
    match k:
        case ObjProp.ID:
            if not (1 <= v <= 9999):
                raise ValidationError(f"ID {v} is not a vaid object ID")
        case ObjProp.X: ...
        case ObjProp.Y: ...
        case ObjProp.GROUPS: ...
        case _:
            print(f'placeholder warning: {k} : {v} is not validated.')


@lru_cache(maxsize=1024)
def _validate_key_allowed(obj_id: int, k: str):
    pass


def validate(obj_id: int, key: str, v: Any):
    """immediate validation. to be called by 'level.objects' mutations"""
    if not setting.immediate.property_type_check: return
    
    if key == ObjProp.GROUPS:
        for group_id in v:
            if not isinstance(group_id, int):
                raise ValidationError(f"Group ID {group_id} in Groups must be an int, got {type(group_id)}")
            if not (1 <= group_id <= 9999):
                raise ValidationError(f"Group ID {group_id} in Groups must be in range 1-9999")
        return
    elif key == ObjProp.PARENT_GROUPS:
        return
    elif key == ObjProp.Trigger.Spawn.REMAPS:
        return
    
    _validate_key_allowed(obj_id, key)
    try:
        _validate_key_value(key, v)
    except TypeError as e:
        print(f"Type error validating key {key} with value {v} on object ID {obj_id}")
        raise e
    


def export_validation(final_object_list: list[ObjectType]):
    """to be called in level.export"""
    pass