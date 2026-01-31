
from typing import Any
from gmdbuilder.mappings.obj_prop import ObjProp
from gmdbuilder.object_types import AdvFollowType, MoveType, ObjectType, RotateType

class setting:
    immediate_property_allowed_check = True
    """Checks that all property keys are allowed on the given object ID."""
    
    immediate_property_type_check = True
    """Checks that all property value types and ranges are correct"""
    
    export_target_exists_check = True
    """Checks that all targets referenced by triggers actually exist"""
    
    export_solid_target_check = True
    """Checks that visual-related triggers target non-trigger & visible groups/objects"""
    
    export_spawn_limit_check = True
    """Checks for any spawn-limit occurrance within trigger execution chains"""
    
    export_group_parent_check = True
    """Checks that every group parent is unique (no two parents for 1 ID)"""


class ValidatedObject(dict[str, Any]):
    """
    WARNING! DONT USE DIRECTLY. THIS IS FOR LIBRARY IMPLEMENTATION
    
    The actual dict implementation hidden behind the ObjectType TypedDict
    
    This is to intercept & validate mutations of objects and add new helpers.
    """
    __slots__ = ("_obj_id",)

    def __init__(self, obj_id: int):
        super().__init__()
        self._obj_id = int(obj_id)
        super().__setitem__("a1", self._obj_id)

    def __setitem__(self, k: str, v: Any):
        validate(self._obj_id, k, v)
        if k == ObjProp.ID:
            self._obj_id = int(v)
        super().__setitem__(k, v)

    def update(self, *args: Any, **kwargs: Any):  # type: ignore[override]
        # Construct items dict from args and kwargs
        items: dict[str, Any]
        if args:
            if len(args) != 1:
                raise TypeError(f"update() takes at most 1 positional argument ({len(args)} given)")
            __m = args[0]
            items = dict(__m)  # type: ignore[arg-type]
            items.update(kwargs)
        else:
            items = dict(kwargs)
        
        for k, v in items.items():
            validate(self._obj_id, k, v)
        if id := items.get(ObjProp.ID):
            self._obj_id = int(id)
        super().update(items)


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


ID_TO_TYPEDDICT = {
    901: MoveType,
    1346: RotateType,
    3016: AdvFollowType,
}

# def typeddict_keys(td) -> set[str]:
#     return set(getattr(td, "__required_keys__", set())) | set(getattr(td, "__optional_keys__", set()))

# DEFAULT_ALLOWED = typeddict_keys(ObjectType)
# ALLOWED_BY_ID = {k: typeddict_keys(v) for k, v in ID_TO_TYPEDDICT.items()}


def validate_obj(obj: ObjectType):
    for k, v in obj.items(): validate(obj['a1'], k, v)

def validate(obj_id: int, key: str, v: Any):
    """immediate validation. to be called by 'level.objects' mutations"""
    # raise NotImplementedError()
    if not setting.immediate_property_type_check: return
    
    match key:
        case ObjProp.ID:
            if v not in range(0,9999):
                raise ValidationError(f"Object ID {v} not in range")
        case ObjProp.X: ...
        case ObjProp.Y: ...
        case _:
            print(f'placeholder warning: {key} : {v} is not validated.')


def export_validation(final_object_list: list[ObjectType]):
    """to be called in level.export"""
    pass