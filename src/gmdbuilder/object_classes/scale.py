# pyright: reportTypedDictNotRequiredAccess=false

from gmdbuilder import obj_prop
from gmdbuilder.mappings import obj_id
from gmdbuilder.mappings.obj_enum import Easing
from gmdbuilder.object_classes.object import ObjField
from gmdbuilder.object_classes.trigger import Trigger


class ScaleTrigger(Trigger):
    def __init__(self):
        super().__init__(obj_id.Trigger.SCALE)

    # ------------------------------------------------------------------
    # Methods
    # ------------------------------------------------------------------
    
    def scale(self, factor: float, duration: float = 0, divide: bool = False):
        """Uniformly scale by a factor over a duration."""
        self.scale_by_x = factor
        self.scale_by_y = factor
        self.div_by_x = divide
        self.div_by_y = divide
        self.duration = duration
        return self
    
    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    duration = ObjField[float](obj_prop.Trigger.Scale.DURATION)
    """Duration in seconds (a10)"""
    
    easing = ObjField[Easing](obj_prop.Trigger.Scale.EASING)
    """Easing curve type (a30)"""
    
    target_id = ObjField[int](obj_prop.Trigger.Scale.TARGET_ID)
    """Group ID to scale (a51)"""
    
    center_id = ObjField[int](obj_prop.Trigger.Scale.CENTER_ID)
    """Group ID to scale around (a71)"""
    
    ease_rate = ObjField[float](obj_prop.Trigger.Scale.EASE_RATE)
    """Easing rate multiplier (a85)"""
    
    only_move = ObjField[bool](obj_prop.Trigger.Scale.ONLY_MOVE)
    """Only move the object, do not visually scale it (a133)"""
    
    scale_by_x = ObjField[float](obj_prop.Trigger.Scale.SCALE_BY_X)
    """X scale multiplier (a150)"""
    
    scale_by_y = ObjField[float](obj_prop.Trigger.Scale.SCALE_BY_Y)
    """Y scale multiplier (a151)"""
    
    div_by_x = ObjField[bool](obj_prop.Trigger.Scale.DIV_BY_X)
    """Divide by X scale instead of multiplying (a153)"""
    
    div_by_y = ObjField[bool](obj_prop.Trigger.Scale.DIV_BY_Y)
    """Divide by Y scale instead of multiplying (a154)"""
    
    relative_rotation = ObjField[bool](obj_prop.Trigger.Scale.RELATIVE_ROTATION)
    """Keep rotation relative to center during scale (a452)"""
    
    relative_scale = ObjField[bool](obj_prop.Trigger.Scale.RELATIVE_SCALE)
    """Scale relative to current scale rather than base (a577)"""
