
import traceback
from dataclasses import dataclass
from typing import Any, Callable
from gmdbuilder.internal_mappings.obj_prop import ObjProp

class Settings:
    validate_solid_targets: bool = True
    """
    Checks that no transforming trigger targets non-trigger visible groups
    
    (move, rotate, follow, etc. but NOT spawn, toggle, count, etc.)
    """
    validate_target_exists: bool = True
    """Checks that all targets referenced by triggers actually exist"""
    validate_spawn_limit: bool = True
    """Check for any spawn-limit occurrance within trigger execution chains"""


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

@dataclass
class DeferredValidation:
    key: str
    value: Any
    stack_trace: traceback.FrameSummary | None
    validator: Callable | None = None
    
    def resolve(self, level: Any) -> None:
        """Try to validate now that we have full context"""
        if self.validator is None:
            return
        
        try:
            self.validator(self.value, level)
        except ValidationError as e:
            location = "unknown location"
            if self.stack_trace:
                location = f"{self.stack_trace.filename}:{self.stack_trace.lineno} in {self.stack_trace.name}"
            
            e.add_context(
                original_key=self.key,
                original_value=self.value,
                set_at=location,
                code_line=self.stack_trace.line if self.stack_trace else None
            )
            raise



def _validate_color(value: Any) -> None:
    if not isinstance(value, str):
        raise ValidationError(f"HSV color must be string, got {type(value)}")


def _validate_target_exists(target_id: int, level: Any) -> None:
    """Deferred: Check that target group exists in level"""
    pass


def validate(key: str, value: Any) -> dict[str, Any]:
    """
    Validate a key-value pair.
    
    Returns dict with:
    - deferred: bool - whether validation is deferred to export time
    - validator: Callable | None - validator function for deferred checks
    """
    
    match key:
        case ObjProp.Trigger.Pulse.HSV:
            # Immediate validation
            _validate_color(value)
            return {"deferred": False}
        
        case ObjProp.Trigger.Collision.BLOCK_A | ObjProp.Trigger.Collision.BLOCK_B:
            # Deferred: need to check if target is solid object
            if not isinstance(value, int):
                raise ValidationError(f"Block ID must be int, got {type(value)}")
            return {"deferred": True, "validator": _validate_target_exists}
        
        case _:
            # Unknown key - no validation
            return {"deferred": False}


def export_validation(level: Any) -> None:
    """
    Resolve all deferred validations for all objects in level.
    Call this before serializing.
    """
    from gmdbuilder.object import Object
    
    validation_errors = []
    
    for obj in level.objects:
        if isinstance(obj, Object):
            for deferred in obj._deferred_validations:
                try:
                    deferred.resolve(level)
                except ValidationError as e:
                    validation_errors.append(e)
    
    if validation_errors:
        error_msg = "Validation failed during export:\n\n"
        error_msg += "\n\n".join(str(e) for e in validation_errors)
        raise ValidationError(error_msg)
    