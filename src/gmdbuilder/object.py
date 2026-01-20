"""Object builder"""

import traceback
from typing import Any
from gmdbuilder.object_types import ObjectType
from gmdbuilder.internal_mappings.obj_prop import ObjProp
from gmdbuilder.validation import DeferredValidation, validate
from gmdbuilder.kit_interface import (
    get_object_defaults,
    typed_to_kit_object,
    kit_object_to_typed,
    KitObject,
)


class Object:
    def __init__(self, object_id: int):
        self._dict: ObjectType = get_object_defaults(object_id)
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
        
        self._dict[key] = value
    
    def __getitem__(self, key: str) -> Any:
        return self._dict[key]
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a property value with optional default."""
        return self._dict.get(key, default)
    
    @property
    def properties(self) -> ObjectType:
        """Access the underlying TypedDict of properties, w/ string keys. for int keys, use to_kit_object"""
        return self._dict
    
    def _to_kit_object(self) -> KitObject:
        """Internal: Convert to gmdkit KitObject."""
        return typed_to_kit_object(self._dict)
    
    @classmethod
    def _from_kit_object(cls, kit_obj: KitObject) -> "Object":
        """Internal: Create Object from gmdkit KitObject."""
        object_id = kit_obj.get(1)
        if object_id is None:
            raise ValueError("KitObject missing required ID property (key 1)")
        
        # Create new instance with defaults
        obj = cls(object_id)
        obj._dict = kit_object_to_typed(kit_obj)
        return obj
    
    @classmethod
    def from_dict(cls, typed_dict: ObjectType) -> "Object":
        """
        Create an Object from a dictionary.
        
        Useful for advanced use cases where you have a pre-built dict.
        
        Args:
            typed_dict: Dictionary with string keys (a1, a2, etc.)
            
        Returns:
            New Object instance
        """
        # Extract object ID from a1 key
        object_id_value = typed_dict.get("a1")
        if object_id_value is None:
            raise ValueError("Object dict missing required ID (a1)")
        
        # Create new instance
        obj = cls(object_id_value)
        obj._dict = typed_dict.copy()
        
        return obj
    
    def copy(self) -> "Object":
        """
        Create a deep copy of this object.
        
        Returns:
            New Object instance with copied properties
        """
        new_obj = Object(self._dict[ObjProp.ID])
        new_obj._dict = self._dict.copy()
        new_obj._deferred_validations = self._deferred_validations.copy()
        return new_obj
    
    def __repr__(self) -> str:
        return f"Object(id={self._dict[ObjProp.ID]}, properties={len(self._dict)})"