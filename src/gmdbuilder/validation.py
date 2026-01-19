

from gmdbuilder.object_types import Object, Trigger
from gmdbuilder.level import Level

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


def enforce_spawn_limit(triggers: list[Trigger]):
    objs: list[Object] = [ o for o in Level.get_objects() if o.get('')]
    ...