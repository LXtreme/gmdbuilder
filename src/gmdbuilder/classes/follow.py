from gmdbuilder.classes.object import ObjField
from gmdbuilder.classes.trigger import Trigger
from gmdbuilder.mappings import obj_prop, obj_id


class Follow(Trigger):
    """Follow trigger. Inherits: Object -> Trigger -> Follow"""

    def __init__(self):
        super().__init__(obj_id.Trigger.FOLLOW)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    duration = ObjField[float](obj_prop.Trigger.Follow.DURATION)
    """Duration in seconds (a10)"""

    target_id = ObjField[int](obj_prop.Trigger.Follow.TARGET_ID)
    """Group ID that follows (a51)"""

    follow_target = ObjField[int](obj_prop.Trigger.Follow.FOLLOW_TARGET)
    """Group ID to follow (a71)"""

    mod_x = ObjField[float](obj_prop.Trigger.Follow.MOD_X)
    """X movement multiplier (a72)"""

    mod_y = ObjField[float](obj_prop.Trigger.Follow.MOD_Y)
    """Y movement multiplier (a73)"""


class Shake(Trigger):
    """Shake trigger. Inherits: Object -> Trigger -> Shake"""

    def __init__(self):
        super().__init__(obj_id.Trigger.SHAKE)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    duration = ObjField[float](obj_prop.Trigger.Shake.DURATION)
    """Duration in seconds (a10)"""

    strength = ObjField[float](obj_prop.Trigger.Shake.STRENGTH)
    """Shake strength (a75)"""

    interval = ObjField[float](obj_prop.Trigger.Shake.INTERVAL)
    """Time between shake steps in seconds (a84)"""
