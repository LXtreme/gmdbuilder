"""Object builder"""

import traceback
from typing import Any
from gmdkit.models.object import Object as kit_object
from gmdbuilder.object_types import Object as ObjectType
from src.gmdbuilder.internal_mappings.obj_prop import ObjProp
from src.gmdbuilder.validation import DeferredValidation, validate
# Object

class Object:
    def __init__(self, object_id: int):
        self.dict: ObjectType = kit_object.DEFAULTS.get(object_id, {})
        self._deferred_validations: list[DeferredValidation] = []
    
    def __setitem__(self, key: str, value: Any) -> None:
        validation_result = validate(key, value)
        
        if validation_result["deferred"]:
            stack = traceback.extract_stack()
            user_frame = None
            for frame in reversed(stack[:-1]):
                if "gmdbuilder" in frame.filename and "validation" not in frame.filename:
                    user_frame = frame
                    break
            
            pending = DeferredValidation(
                key=key,
                value=value,
                stack_trace=user_frame,
                validator=validation_result.get("validator")
            )
            self._deferred_validations.append(pending)
        
        self.dict[key] = value
    
    def __getitem__(self, key: str) -> Any:
        return self.dict[key]
    
    def get(self, key: str) -> Any:
        return self.dict.get(key)
    

a = Object(2)
b = a[ObjProp.COLOR_1]