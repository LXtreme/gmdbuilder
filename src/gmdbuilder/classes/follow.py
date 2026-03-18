
from gmdbuilder.classes.object import ObjField
from gmdbuilder.classes.trigger import Trigger
from gmdbuilder.mappings import obj_prop, obj_id
from gmdbuilder.mappings.obj_enum import AdvFollow as AdvFollowEnum


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


class FollowPlayerY(Trigger):
    """Follow Player Y trigger. Inherits: Object -> Trigger -> FollowPlayerY"""

    def __init__(self):
        super().__init__(obj_id.Trigger.FOLLOW_PLAYER_Y)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    duration = ObjField[float](obj_prop.Trigger.FollowPlayerY.DURATION)
    """Duration in seconds (a10)"""

    target_id = ObjField[int](obj_prop.Trigger.FollowPlayerY.TARGET_ID)
    """Group ID to apply the follow effect to (a51)"""

    speed = ObjField[float](obj_prop.Trigger.FollowPlayerY.SPEED)
    """How fast the target follows the player Y position (a90)"""

    delay = ObjField[float](obj_prop.Trigger.FollowPlayerY.DELAY)
    """Delay before following begins in seconds (a91)"""

    offset = ObjField[int](obj_prop.Trigger.FollowPlayerY.OFFSET)
    """Y offset applied to the follow position (a92)"""

    max_speed = ObjField[float](obj_prop.Trigger.FollowPlayerY.MAX_SPEED)
    """Maximum follow speed cap (a105)"""


class AdvFollow(Trigger):
    """Advanced Follow trigger. Inherits: Object -> Trigger -> AdvFollow"""

    def __init__(self):
        super().__init__(obj_id.Trigger.ADV_FOLLOW)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    target_id = ObjField[int](obj_prop.Trigger.AdvFollow.TARGET_ID)
    """Group ID to apply the follow behaviour to (a51)"""

    follow_id = ObjField[int](obj_prop.Trigger.AdvFollow.FOLLOW_ID)
    """Group ID to follow (a71)"""

    player_1 = ObjField[bool](obj_prop.Trigger.AdvFollow.PLAYER_1)
    """Follow player 1 instead of a group (a138)"""

    player_2 = ObjField[bool](obj_prop.Trigger.AdvFollow.PLAYER_2)
    """Follow player 2 instead of a group (a200)"""

    corner = ObjField[bool](obj_prop.Trigger.AdvFollow.CORNER)
    """Use corner detection for following (a201)"""

    delay = ObjField[float](obj_prop.Trigger.AdvFollow.DELAY)
    """Startup delay in seconds (a292)"""

    delay_rand = ObjField[float](obj_prop.Trigger.AdvFollow.DELAY_RAND)
    """Random additional startup delay range (a293)"""

    max_speed = ObjField[float](obj_prop.Trigger.AdvFollow.MAX_SPEED)
    """Maximum movement speed (a298)"""

    max_speed_rand = ObjField[float](obj_prop.Trigger.AdvFollow.MAX_SPEED_RAND)
    """Random additional max speed range (a299)"""

    start_speed = ObjField[float](obj_prop.Trigger.AdvFollow.START_SPEED)
    """Initial speed when follow begins (a300)"""

    start_speed_rand = ObjField[float](obj_prop.Trigger.AdvFollow.START_SPEED_RAND)
    """Random additional start speed range (a301)"""

    target_dir = ObjField[bool](obj_prop.Trigger.AdvFollow.TARGET_DIR)
    """Orient movement towards the target direction (a305)"""

    x_only = ObjField[bool](obj_prop.Trigger.AdvFollow.X_ONLY)
    """Constrain follow to X axis only (a306)"""

    y_only = ObjField[bool](obj_prop.Trigger.AdvFollow.Y_ONLY)
    """Constrain follow to Y axis only (a307)"""

    max_range = ObjField[int](obj_prop.Trigger.AdvFollow.MAX_RANGE)
    """Maximum distance at which following is active (a308)"""

    max_range_rand = ObjField[int](obj_prop.Trigger.AdvFollow.MAX_RANGE_RAND)
    """Random additional max range (a309)"""

    steer = ObjField[float](obj_prop.Trigger.AdvFollow.STEER)
    """Steering force towards target (a316)"""

    steer_rand = ObjField[float](obj_prop.Trigger.AdvFollow.STEER_RAND)
    """Random additional steer range (a317)"""

    steer_low = ObjField[float](obj_prop.Trigger.AdvFollow.STEER_LOW)
    """Steer force at low speed (a318)"""

    steer_low_rand = ObjField[float](obj_prop.Trigger.AdvFollow.STEER_LOW_RAND)
    """Random additional steer-low range (a319)"""

    steer_high = ObjField[float](obj_prop.Trigger.AdvFollow.STEER_HIGH)
    """Steer force at high speed (a320)"""

    steer_high_rand = ObjField[float](obj_prop.Trigger.AdvFollow.STEER_HIGH_RAND)
    """Random additional steer-high range (a321)"""

    speed_range_low = ObjField[float](obj_prop.Trigger.AdvFollow.SPEED_RANGE_LOW)
    """Speed threshold for low-speed steer (a322)"""

    speed_range_low_rand = ObjField[float](obj_prop.Trigger.AdvFollow.SPEED_RANGE_LOW_RAND)
    """Random additional low speed range (a323)"""

    speed_range_high = ObjField[float](obj_prop.Trigger.AdvFollow.SPEED_RANGE_HIGH)
    """Speed threshold for high-speed steer (a324)"""

    speed_range_high_rand = ObjField[float](obj_prop.Trigger.AdvFollow.SPEED_RANGE_HIGH_RAND)
    """Random additional high speed range (a325)"""

    break_force = ObjField[float](obj_prop.Trigger.AdvFollow.BREAK_FORCE)
    """Deceleration force applied when braking (a326)"""

    break_force_rand = ObjField[float](obj_prop.Trigger.AdvFollow.BREAK_FORCE_RAND)
    """Random additional brake force range (a327)"""

    break_angle = ObjField[float](obj_prop.Trigger.AdvFollow.BREAK_ANGLE)
    """Angle threshold in degrees at which braking activates (a328)"""

    break_angle_rand = ObjField[float](obj_prop.Trigger.AdvFollow.BREAK_ANGLE_RAND)
    """Random additional brake angle range (a329)"""

    break_steer = ObjField[float](obj_prop.Trigger.AdvFollow.BREAK_STEER)
    """Steer force applied while braking (a330)"""

    break_steer_rand = ObjField[float](obj_prop.Trigger.AdvFollow.BREAK_STEER_RAND)
    """Random additional brake steer range (a331)"""

    break_steer_speed_limit = ObjField[float](obj_prop.Trigger.AdvFollow.BREAK_STEER_SPEED_LIMIT)
    """Speed limit below which brake steer activates (a332)"""

    break_steer_speed_limit_rand = ObjField[float](obj_prop.Trigger.AdvFollow.BREAK_STEER_SPEED_LIMIT_RAND)
    """Random additional brake steer speed limit range (a333)"""

    acceleration = ObjField[float](obj_prop.Trigger.AdvFollow.ACCELERATION)
    """Acceleration force applied towards max speed (a334)"""

    acceleration_rand = ObjField[float](obj_prop.Trigger.AdvFollow.ACCELERATION_RAND)
    """Random additional acceleration range (a335)"""

    ignore_disabled = ObjField[bool](obj_prop.Trigger.AdvFollow.IGNORE_DISABLED)
    """Continue following even when target group is disabled (a336)"""

    steer_low_check = ObjField[bool](obj_prop.Trigger.AdvFollow.STEER_LOW_CHECK)
    """Enable low-speed steer threshold check (a337)"""

    steer_high_check = ObjField[bool](obj_prop.Trigger.AdvFollow.STEER_HIGH_CHECK)
    """Enable high-speed steer threshold check (a338)"""

    rotate_dir = ObjField[bool](obj_prop.Trigger.AdvFollow.ROTATE_DIR)
    """Rotate the target object to face movement direction (a339)"""

    rot_offset = ObjField[int](obj_prop.Trigger.AdvFollow.ROT_OFFSET)
    """Rotation offset in degrees applied on top of direction (a340)"""

    near_accel = ObjField[float](obj_prop.Trigger.AdvFollow.NEAR_ACCEL)
    """Extra acceleration applied when near the target (a357)"""

    near_accel_rand = ObjField[float](obj_prop.Trigger.AdvFollow.NEAR_ACCEL_RAND)
    """Random additional near acceleration range (a358)"""

    near_dist = ObjField[float](obj_prop.Trigger.AdvFollow.NEAR_DIST)
    """Distance threshold for near acceleration to activate (a359)"""

    near_dist_rand = ObjField[float](obj_prop.Trigger.AdvFollow.NEAR_DIST_RAND)
    """Random additional near distance range (a360)"""

    easing = ObjField[float](obj_prop.Trigger.AdvFollow.EASING)
    """Easing strength applied to movement (a361)"""

    easing_rand = ObjField[float](obj_prop.Trigger.AdvFollow.EASING_RAND)
    """Random additional easing range (a362)"""

    rot_easing = ObjField[int](obj_prop.Trigger.AdvFollow.ROT_EASING)
    """Easing type applied to rotation (a363)"""

    rot_deadzone = ObjField[int](obj_prop.Trigger.AdvFollow.ROT_DEADZONE)
    """Angle deadzone in degrees before rotation updates (a364)"""

    priority = ObjField[int](obj_prop.Trigger.AdvFollow.PRIORITY)
    """Execution priority when multiple AdvFollow triggers affect the same group (a365)"""

    max_range_ref = ObjField[int](obj_prop.Trigger.AdvFollow.MAX_RANGE_REF)
    """Group ID used as reference for max range measurement (a366)"""

    mode = ObjField[AdvFollowEnum.Mode](obj_prop.Trigger.AdvFollow.MODE)
    """Follow mode: MODE_1 / MODE_2 / MODE_3 (a367)"""

    friction = ObjField[float](obj_prop.Trigger.AdvFollow.FRICTION)
    """Friction applied to movement each frame (a558)"""

    friction_rand = ObjField[float](obj_prop.Trigger.AdvFollow.FRICTION_RAND)
    """Random additional friction range (a559)"""

    start_speed_ref = ObjField[int](obj_prop.Trigger.AdvFollow.START_SPEED_REF)
    """Group ID used as reference for start speed direction (a560)"""

    near_friction = ObjField[float](obj_prop.Trigger.AdvFollow.NEAR_FRICTION)
    """Extra friction applied when near the target (a561)"""

    near_friction_rand = ObjField[float](obj_prop.Trigger.AdvFollow.NEAR_FRICTION_RAND)
    """Random additional near friction range (a562)"""

    start_dir = ObjField[int](obj_prop.Trigger.AdvFollow.START_DIR)
    """Initial movement direction in degrees (a563)"""

    start_dir_rand = ObjField[int](obj_prop.Trigger.AdvFollow.START_DIR_RAND)
    """Random additional start direction range (a564)"""

    start_dir_ref = ObjField[int](obj_prop.Trigger.AdvFollow.START_DIR_REF)
    """Group ID used as reference for start direction (a565)"""

    exclusive = ObjField[bool](obj_prop.Trigger.AdvFollow.EXCLUSIVE)
    """Override all other AdvFollow triggers on the same target (a571)"""

    init = ObjField[AdvFollowEnum.Init](obj_prop.Trigger.AdvFollow.INIT)
    """Initialisation mode when trigger activates: INIT / SET / ADD (a572)"""


class EditAdvFollow(Trigger):
    """
    Edit Advanced Follow trigger. Modifies an active AdvFollow trigger at runtime.
    Inherits: Object -> Trigger -> EditAdvFollow

    Most properties mirror AdvFollow exactly. The M_xxx named fields are properties
    that exist in the GD data but whose exact purpose is not yet documented.
    """

    def __init__(self):
        super().__init__(obj_id.Trigger.EDIT_ADV_FOLLOW)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    target_id = ObjField[int](obj_prop.Trigger.EditAdvFollow.TARGET_ID)
    """Group ID of the AdvFollow trigger to edit (a51)"""

    follow_id = ObjField[int](obj_prop.Trigger.EditAdvFollow.FOLLOW_ID)
    """New follow target group ID (a71)"""

    player_1 = ObjField[bool](obj_prop.Trigger.EditAdvFollow.PLAYER_1)
    """Retarget to player 1 (a138)"""

    player_2 = ObjField[bool](obj_prop.Trigger.EditAdvFollow.PLAYER_2)
    """Retarget to player 2 (a200)"""

    corner = ObjField[bool](obj_prop.Trigger.EditAdvFollow.CORNER)
    """Update corner detection setting (a201)"""

    speed = ObjField[float](obj_prop.Trigger.EditAdvFollow.SPEED)
    """New max speed value (a300)"""

    speed_rand = ObjField[float](obj_prop.Trigger.EditAdvFollow.SPEED_RAND)
    """Random additional speed range (a301)"""

    x_only = ObjField[bool](obj_prop.Trigger.EditAdvFollow.X_ONLY)
    """Constrain to X axis only (a306)"""

    y_only = ObjField[bool](obj_prop.Trigger.EditAdvFollow.Y_ONLY)
    """Constrain to Y axis only (a307)"""

    use_control_id = ObjField[bool](obj_prop.Trigger.EditAdvFollow.USE_CONTROL_ID)
    """Use control ID to target specific AdvFollow instance (a535)"""

    speed_ref = ObjField[int](obj_prop.Trigger.EditAdvFollow.SPEED_REF)
    """Group ID used as reference for speed direction (a560)"""

    dir = ObjField[int](obj_prop.Trigger.EditAdvFollow.DIR)
    """New movement direction in degrees (a563)"""

    dir_rand = ObjField[int](obj_prop.Trigger.EditAdvFollow.DIR_RAND)
    """Random additional direction range (a564)"""

    dir_ref = ObjField[int](obj_prop.Trigger.EditAdvFollow.DIR_REF)
    """Group ID used as reference for direction (a565)"""

    mod_x = ObjField[float](obj_prop.Trigger.EditAdvFollow.MOD_X)
    """X velocity modifier (a566)"""

    mod_x_rand = ObjField[float](obj_prop.Trigger.EditAdvFollow.MOD_X_RAND)
    """Random additional X modifier range (a567)"""

    mod_y = ObjField[float](obj_prop.Trigger.EditAdvFollow.MOD_Y)
    """Y velocity modifier (a568)"""

    mod_y_rand = ObjField[float](obj_prop.Trigger.EditAdvFollow.MOD_Y_RAND)
    """Random additional Y modifier range (a569)"""

    redirect_dir = ObjField[bool](obj_prop.Trigger.EditAdvFollow.REDIRECT_DIR)
    """Redirect current movement direction rather than resetting it (a570)"""

    mode = ObjField[AdvFollowEnum.Mode](obj_prop.Trigger.EditAdvFollow.M_367)
    """Follow mode: MODE_1 / MODE_2 / MODE_3 (a367)"""

    init = ObjField[AdvFollowEnum.Init](obj_prop.Trigger.EditAdvFollow.M_572)
    """Initialisation mode: INIT / SET / ADD (a572)"""
