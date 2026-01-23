

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



def _validate_color(value: Any) -> None:
    if not isinstance(value, str):
        raise ValidationError(f"HSV color must be string, got {type(value)}")


def _validate_target_exists(target_id: int, level: Any) -> None:
    """Deferred: Check that target group exists in level"""
    pass


def validate(key: str, value: Any) -> None:
    """immediate validation"""
    pass


def export_validation(level: Any) -> None:
    pass