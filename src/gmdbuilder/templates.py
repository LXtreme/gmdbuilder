
import gmdbuilder.object_typeddict as td
from gmdbuilder.core import new_object
from gmdbuilder.mappings.obj_id import ObjId
from gmdbuilder.mappings.obj_prop import ObjProp

def to_spawn_multi(obj: td.TriggerType) -> td.TriggerType:
    """Convert trigger to Spawn-Triggered & Multi-triggered"""
    obj[ObjProp.Trigger.MULTI_TRIGGER] = True
    obj[ObjProp.Trigger.SPAWN_TRIGGER] = True
    return obj

class Trigger:
    @staticmethod
    def move_to_target(
        x: float, y: float, 
        target: int, location: int, duration: float = 0, 
        easing_type: int = 0, easing_rate: float = 1
    ) -> td.MoveType:
        """Create a move trigger template object."""
        obj = new_object(ObjId.Trigger.MOVE)
        obj[ObjProp.X] = x
        obj[ObjProp.Y] = y
        obj[ObjProp.Trigger.Move.TARGET_ID] = target 
        obj[ObjProp.Trigger.Move.TARGET_POS] = location
        obj[ObjProp.Trigger.Move.TARGET_MODE] = True # untested
        obj[ObjProp.Trigger.Move.DURATION] = duration
        obj[ObjProp.Trigger.Move.EASING] = easing_type
        obj[ObjProp.Trigger.Move.EASE_RATE] = easing_rate
        return obj