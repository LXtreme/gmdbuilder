from typing import Self

from gmdbuilder.classes.object import ObjField
from gmdbuilder.classes.trigger import Trigger
from gmdbuilder.mappings import obj_prop, obj_id
from gmdbuilder.mappings.obj_enum import Easing, MoveTargetAxis


class Move(Trigger):
    """Move trigger. Inherits: Object -> Trigger -> Move"""

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


class Rotate(Trigger):
    """Rotate trigger. Inherits: Object -> Trigger -> Rotate"""

    def __init__(self):
        super().__init__(obj_id.Trigger.ROTATE)

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


class Scale(Trigger):
    """Scale trigger. Inherits: Object -> Trigger -> Scale"""

    def __init__(self):
        super().__init__(obj_id.Trigger.SCALE)

    # ------------------------------------------------------------------
    # Methods
    # ------------------------------------------------------------------

    def scale(self, factor: float, duration: float = 0, divide: bool = False) -> Self:
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
