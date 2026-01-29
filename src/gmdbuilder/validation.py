
from typing import Any
from gmdbuilder.internal_mappings.obj_prop import ObjProp
from gmdbuilder.object_types import ObjectType

property_range_check: bool = True
"""Checks that all property value ranges are correct as they are given"""
property_type_check: bool = True
"""Checks that all property value types are correct as they are given"""
export_target_exists_check: bool = True
"""Checks that all targets referenced by triggers actually exist"""
export_solid_target_check: bool = True
"""Checks that visual-related triggers target non-trigger & visible groups/objects"""
export_spawn_limit_check: bool = True
"""Checks for any spawn-limit occurrance within trigger execution chains"""


class ValidationError(Exception):
    def __init__(self, msg: str, deferred: bool = False):
        self.deferred = deferred
        self.context = {}
        super().__init__(msg)
    
    def add_context(self, **kwargs):
        self.context.update(kwargs)
        return self
    
    def __str__(self) -> str:
        msg = super().__str__()
        if self.context:
            context_str = "\n".join(f"  {k}: {v}" for k, v in self.context.items())
            return f"{msg}\n{context_str}"
        return msg

def validate_obj(obj: ObjectType):
    for k, v in obj.items(): validate(k, v)

def validate(key: str, value: Any):
    """immediate validation. to be called by 'level.objects' mutations"""
    if not property_type_check:
        return
    
    match key:
        case ObjProp.ID:
            if value not in [range(0,9999)]:
                raise ValidationError()
        case _:
            print('placeholder warning: key is not validated')


def export_validation(final_object_list: list[ObjectType]):
    """to be called in level.export"""
    pass