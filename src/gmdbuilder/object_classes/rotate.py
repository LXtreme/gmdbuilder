
from gmdbuilder import obj_prop
from gmdbuilder.mappings import obj_id
from gmdbuilder.mappings.obj_enum import Easing
from gmdbuilder.object_classes.object import ObjField
from gmdbuilder.object_classes.trigger import Trigger


class RotateTrigger(Trigger):
    def __init__(self):
        super().__init__(obj_id.Trigger.ROTATE)
    
    # ------------------------------------------------------------------
    # Methods
    # ------------------------------------------------------------------
    
    

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    duration = ObjField[float](obj_prop.Trigger.Rotate.DURATION)
    """Duration in seconds (a10)"""
    
    easing = ObjField[Easing](obj_prop.Trigger.Rotate.EASING)
    """Easing curve type (a30)"""
    
    target_id = ObjField[int](obj_prop.Trigger.Rotate.TARGET_ID)
    """Group ID to rotate (a51)"""
    
    degrees = ObjField[float](obj_prop.Trigger.Rotate.DEGREES)
    """Degrees to rotate, clockwise positive (a68)"""
    
    full = ObjField[int](obj_prop.Trigger.Rotate.FULL)
    """Number of full 360° rotations to add (a69)"""
    
    lock_rotation = ObjField[bool](obj_prop.Trigger.Rotate.LOCK_ROTATION)
    """Lock object rotation to movement direction (a70)"""
    
    center_id = ObjField[int](obj_prop.Trigger.Rotate.CENTER_ID)
    """Group ID to rotate around (a71)"""
    
    ease_rate = ObjField[float](obj_prop.Trigger.Rotate.EASE_RATE)
    """Easing rate multiplier (a85)"""
    
    aim_mode = ObjField[bool](obj_prop.Trigger.Rotate.AIM_MODE)
    """Rotate to face another group (aim mode) (a100)"""
    
    player_1 = ObjField[bool](obj_prop.Trigger.Rotate.PLAYER_1)
    """Target player 1 (a138)"""
    
    player_2 = ObjField[bool](obj_prop.Trigger.Rotate.PLAYER_2)
    """Target player 2 (a200)"""
    
    follow_mode = ObjField[bool](obj_prop.Trigger.Rotate.FOLLOW_MODE)
    """Continuously follow target rotation (a394)"""
    
    dynamic_mode = ObjField[bool](obj_prop.Trigger.Rotate.DYNAMIC_MODE)
    """Recalculate aim direction every frame (a397)"""
    
    aim_target_id = ObjField[int](obj_prop.Trigger.Rotate.AIM_TARGET_ID)
    """Group ID to aim towards in aim mode (a401)"""
    
    aim_offset = ObjField[float](obj_prop.Trigger.Rotate.AIM_OFFSET)
    """Angle offset applied on top of aim direction (a402)"""
    
    aim_easing = ObjField[int](obj_prop.Trigger.Rotate.AIM_EASING)
    """Easing type for aim smoothing 0-1 (a403)"""
