
from typing import Self

from gmdbuilder.object_classes.object import ObjField
from gmdbuilder.mappings import obj_prop, obj_id
from gmdbuilder.mappings.obj_enum import Easing, MoveTargetAxis
from gmdbuilder.object_classes.trigger import Trigger


class MoveTrigger(Trigger):
    """
    Wrapper for move triggers with typed properties and helper methods.
    
    Inherits: Object -> Trigger -> MoveTrigger
    """
    def __init__(self):
        super().__init__(obj_id.Trigger.MOVE)

    # ------------------------------------------------------------------
    # Methods
    # ------------------------------------------------------------------
    
    def move_by(self, dx: float, dy: float, t: float = 0) -> Self:
        """Move by a relative distance (dx, dy) over duration t."""
        self.move_x = dx
        self.move_y = dy
        self.duration = t
        self.direction_mode = False
        self.target_mode = False
        return self
    
    def move_to(self, target: int, target_pos: int, t: float) -> Self:
        """Sets to target mode (move to the target's location)."""
        self.target_id = target
        self.target_pos = target_pos
        self.duration = t
        self.target_mode = True
        self.direction_mode = False
        return self
    
    def move_towards(self, target: int, target_dir: int, distance: float, t: float) -> Self:
        """Sets to direction mode (move towards another group with distance)."""
        self.target_id = target
        self.target_pos = target_dir
        self.target_distance = distance
        self.duration = t
        self.direction_mode = True
        self.target_mode = False
        return self
    
    def set_easing(self, easing: Easing, rate: float = 2.0) -> Self:
        """Sets easing type and rate."""
        self.easing = easing
        self.ease_rate = rate
        return self

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    duration = ObjField[float](obj_prop.Trigger.Move.DURATION)
    """Duration in seconds (a10)"""
    
    move_x = ObjField[float](obj_prop.Trigger.Move.MOVE_X)
    """X distance to move in units (a28)"""
    
    move_y = ObjField[float](obj_prop.Trigger.Move.MOVE_Y)
    """Y distance to move in units (a29)"""
    
    easing = ObjField[Easing](obj_prop.Trigger.Move.EASING)
    """Easing curve type (a30)"""
    
    target_id = ObjField[int](obj_prop.Trigger.Move.TARGET_ID)
    """Group ID to move (a51)"""
    
    lock_player_x = ObjField[bool](obj_prop.Trigger.Move.LOCK_PLAYER_X)
    """Lock camera/player X to target (a58)"""
    
    lock_player_y = ObjField[bool](obj_prop.Trigger.Move.LOCK_PLAYER_Y)
    """Lock camera/player Y to target (a59)"""
    
    target_pos = ObjField[int](obj_prop.Trigger.Move.TARGET_POS)
    """Group ID to use as position reference (a71)"""
    
    ease_rate = ObjField[float](obj_prop.Trigger.Move.EASE_RATE)
    """Easing rate multiplier (a85)"""
    
    target_mode = ObjField[bool](obj_prop.Trigger.Move.TARGET_MODE)
    """Use target position (goto) mode (a100)"""
    
    target_axis = ObjField[MoveTargetAxis](obj_prop.Trigger.Move.TARGET_AXIS)
    """Axis constraint for direction mode: none/x/y (a101)"""
    
    player_1 = ObjField[bool](obj_prop.Trigger.Move.PLAYER_1)
    """Target player 1 (a138)"""
    
    lock_camera_x = ObjField[bool](obj_prop.Trigger.Move.LOCK_CAMERA_X)
    """Lock camera X (a141)"""
    
    lock_camera_y = ObjField[bool](obj_prop.Trigger.Move.LOCK_CAMERA_Y)
    """Lock camera Y (a142)"""
    
    follow_x_mod = ObjField[float](obj_prop.Trigger.Move.FOLLOW_X_MOD)
    """X follow modifier (a143)"""
    
    follow_y_mod = ObjField[float](obj_prop.Trigger.Move.FOLLOW_Y_MOD)
    """Y follow modifier (a144)"""
    
    player_2 = ObjField[bool](obj_prop.Trigger.Move.PLAYER_2)
    """Target player 2 (a200)"""
    
    use_small_step = ObjField[bool](obj_prop.Trigger.Move.USE_SMALL_STEP)
    """Use 1/30 block unit precision (a393)"""
    
    direction_mode = ObjField[bool](obj_prop.Trigger.Move.DIRECTION_MODE)
    """Move towards another group (direction mode) (a394)"""
    
    target_center_id = ObjField[int](obj_prop.Trigger.Move.TARGET_CENTER_ID)
    """Group ID to use as movement center in direction mode (a395)"""
    
    target_distance = ObjField[float](obj_prop.Trigger.Move.TARGET_DISTANCE)
    """Distance to travel in direction mode (a396)"""
    
    dynamic_mode = ObjField[bool](obj_prop.Trigger.Move.DYNAMIC_MODE)
    """Recalculate direction every frame (a397)"""
    
    silent = ObjField[bool](obj_prop.Trigger.Move.SILENT)
    """Silent move — no easing preview in editor (a544)"""

