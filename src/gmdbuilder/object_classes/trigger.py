
from gmdbuilder.object_classes.object import Object, ObjField
from gmdbuilder.mappings import obj_prop, obj_id
from gmdbuilder.mappings.obj_enum import Touch as TouchEnum
from gmdkit.models.prop.hsv import HSV


class Trigger(Object):
    """
    Wrapper for trigger objects with typed properties and helper methods.
    
    Inherits: Object -> Trigger
    """
    
    # ------------------------------------------------------------------
    # Methods
    # ------------------------------------------------------------------
    
    
    
    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    touch_trigger = ObjField[bool](obj_prop.Trigger.TOUCH_TRIGGER)
    """Activated by player touch (a11)"""
    
    editor_preview = ObjField[bool](obj_prop.Trigger.EDITOR_PREVIEW)
    """Preview in editor (a13)"""
    
    interactible = ObjField[bool](obj_prop.Trigger.INTERACTIBLE)
    """Player can interact (a36)"""
    
    spawn_trigger = ObjField[bool](obj_prop.Trigger.SPAWN_TRIGGER)
    """Must be spawn-triggered (a62)"""
    
    multi_trigger = ObjField[bool](obj_prop.Trigger.MULTI_TRIGGER)
    """Can be triggered multiple times simultaneously (a87)"""
    
    multi_activate = ObjField[bool](obj_prop.Trigger.MULTI_ACTIVATE)
    """Allow multiple activations (a99)"""
    
    order = ObjField[int](obj_prop.Trigger.ORDER)
    """Spawn order index (a115)"""
    
    reverse = ObjField[bool](obj_prop.Trigger.REVERSE)
    """Reverse effect (a117)"""
    
    channel = ObjField[int](obj_prop.Trigger.CHANNEL)
    """Trigger layer 0-15 (a170)"""
    
    ignore_gparent = ObjField[bool](obj_prop.Trigger.IGNORE_GPARENT)
    """Ignore group parent (a280)"""
    
    ignore_linked = ObjField[bool](obj_prop.Trigger.IGNORE_LINKED)
    """Ignore linked objects (a281)"""
    
    single_ptouch = ObjField[bool](obj_prop.Trigger.SINGLE_PTOUCH)
    """Single player touch only (a284)"""
    
    center_effect = ObjField[bool](obj_prop.Trigger.CENTER_EFFECT)
    """Apply effect from center (a369)"""
    
    disable_multi_activate = ObjField[bool](obj_prop.Trigger.DISABLE_MULTI_ACTIVATE)
    """Disable multi-activate (a444)"""
    
    control_id = ObjField[int](obj_prop.Trigger.CONTROL_ID)
    """Control ID for Stop/Pause/Resume targeting (a534)"""


class ColorTrigger(Trigger):
    def __init__(self):
        super().__init__(obj_id.Trigger.COLOR)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    red                = ObjField[int](obj_prop.Trigger.Color.RED)
    """Red channel 0-255 (a7)"""
    green              = ObjField[int](obj_prop.Trigger.Color.GREEN)
    """Green channel 0-255 (a8)"""
    blue               = ObjField[int](obj_prop.Trigger.Color.BLUE)
    """Blue channel 0-255 (a9)"""
    duration           = ObjField[float](obj_prop.Trigger.Color.DURATION)
    """Duration in seconds (a10)"""
    tint_ground        = ObjField[bool](obj_prop.Trigger.Color.TINT_GROUND)
    """Tint ground with this color (a14)"""
    player_1           = ObjField[bool](obj_prop.Trigger.Color.PLAYER_1)
    """Copy player 1 color (a15)"""
    player_2           = ObjField[bool](obj_prop.Trigger.Color.PLAYER_2)
    """Copy player 2 color (a16)"""
    blending           = ObjField[bool](obj_prop.Trigger.Color.BLENDING)
    """Enable additive blending (a17)"""
    channel            = ObjField[int](obj_prop.Trigger.Color.CHANNEL)
    """Color channel ID to set (a23)"""
    opacity            = ObjField[float](obj_prop.Trigger.Color.OPACITY)
    """Opacity 0.0-1.0 (a35)"""
    hsv                = ObjField[HSV](obj_prop.Trigger.Color.HSV)
    """HSV adjustment (a49)"""
    copy_id            = ObjField[int](obj_prop.Trigger.Color.COPY_ID)
    """Color channel ID to copy from (a50)"""
    copy_opacity       = ObjField[bool](obj_prop.Trigger.Color.COPY_OPACITY)
    """Copy opacity from copied channel (a60)"""
    disable_legacy_hsv = ObjField[bool](obj_prop.Trigger.Color.DISABLE_LEGACY_HSV)
    """Disable legacy HSV effect (a210)"""

    # ------------------------------------------------------------------
    # Proposed methods — let me know which you want
    # ------------------------------------------------------------------

    # set_rgb(r, g, b, duration) -> Self
    #   Sets red, green, blue, duration in one call.
    #   Rationale: RGB is always set together, and this matches the
    #   mental model of "set this channel to this color".

    # set_hex(hex_str, duration) -> Self
    #   Parses a hex string like "#FF8800" and sets red/green/blue, duration.
    #   Rationale: designers think in hex, not separate RGB channels.


class PulseTrigger(Trigger):
    def __init__(self):
        super().__init__(obj_id.Trigger.PULSE)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    red                 = ObjField[int](obj_prop.Trigger.Pulse.RED)
    """Red channel 0-255 (a7)"""
    green               = ObjField[int](obj_prop.Trigger.Pulse.GREEN)
    """Green channel 0-255 (a8)"""
    blue                = ObjField[int](obj_prop.Trigger.Pulse.BLUE)
    """Blue channel 0-255 (a9)"""
    fade_in             = ObjField[float](obj_prop.Trigger.Pulse.FADE_IN)
    """Fade in duration in seconds (a45)"""
    hold                = ObjField[float](obj_prop.Trigger.Pulse.HOLD)
    """Hold duration in seconds (a46)"""
    fade_out            = ObjField[float](obj_prop.Trigger.Pulse.FADE_OUT)
    """Fade out duration in seconds (a47)"""
    use_hsv             = ObjField[bool](obj_prop.Trigger.Pulse.USE_HSV)
    """Use HSV mode instead of RGB (a48)"""
    hsv                 = ObjField[HSV](obj_prop.Trigger.Pulse.HSV)
    """HSV adjustment used when use_hsv=True (a49)"""
    copy_id             = ObjField[int](obj_prop.Trigger.Pulse.COPY_ID)
    """Color channel ID to copy from (a50)"""
    target_id           = ObjField[int](obj_prop.Trigger.Pulse.TARGET_ID)
    """Group or color channel ID to pulse (a51)"""
    target_type         = ObjField[bool](obj_prop.Trigger.Pulse.TARGET_TYPE)
    """False = color channel target, True = group target (a52)"""
    main_only           = ObjField[bool](obj_prop.Trigger.Pulse.MAIN_ONLY)
    """Only pulse main color (a65)"""
    detail_only         = ObjField[bool](obj_prop.Trigger.Pulse.DETAIL_ONLY)
    """Only pulse detail color (a66)"""
    exclusive           = ObjField[bool](obj_prop.Trigger.Pulse.EXCLUSIVE)
    """Override other active pulse triggers (a86)"""
    disable_static_hsv  = ObjField[bool](obj_prop.Trigger.Pulse.DISABLE_STATIC_HSV)
    """Disable static HSV (a210)"""


class AlphaTrigger(Trigger):
    def __init__(self):
        super().__init__(obj_id.Trigger.ALPHA)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    duration = ObjField[float](obj_prop.Trigger.Alpha.DURATION)
    """Duration in seconds (a10)"""
    opacity  = ObjField[float](obj_prop.Trigger.Alpha.OPACITY)
    """Target opacity 0.0-1.0 (a35)"""
    group_id = ObjField[int](obj_prop.Trigger.Alpha.GROUP_ID)
    """Group ID to change opacity of (a51)"""


class ToggleTrigger(Trigger):
    def __init__(self):
        super().__init__(obj_id.Trigger.TOGGLE)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    group_id       = ObjField[int](obj_prop.Trigger.Toggle.GROUP_ID)
    """Group ID to toggle (a51)"""
    activate_group = ObjField[bool](obj_prop.Trigger.Toggle.ACTIVATE_GROUP)
    """True = activate, False = deactivate (a56)"""


class SpawnTrigger(Trigger):
    def __init__(self):
        super().__init__(obj_id.Trigger.SPAWN)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    target_id       = ObjField[int](obj_prop.Trigger.Spawn.TARGET_ID)
    """Group ID to spawn (a51)"""
    delay           = ObjField[float](obj_prop.Trigger.Spawn.DELAY)
    """Delay before spawning in seconds (a63)"""
    disable_preview = ObjField[bool](obj_prop.Trigger.Spawn.DISABLE_PREVIEW)
    """Disable editor preview (a102)"""
    ordered         = ObjField[bool](obj_prop.Trigger.Spawn.ORDERED)
    """Spawn triggers left-to-right in order (a441)"""
    remaps          = ObjField[dict[int, int]](obj_prop.Trigger.Spawn.REMAPS)
    """Group ID remaps applied when spawning: {source: target} (a442)"""
    delay_rand      = ObjField[float](obj_prop.Trigger.Spawn.DELAY_RAND)
    """Random additional delay range in seconds (a556)"""
    reset_remap     = ObjField[bool](obj_prop.Trigger.Spawn.RESET_REMAP)
    """Block incoming remaps from affecting this trigger's spawns (a581)"""

    # ------------------------------------------------------------------
    # Proposed methods — let me know which you want
    # ------------------------------------------------------------------

    # add_remap(source, target) -> Self
    #   Adds a single source->target entry to remaps, creating the dict if needed.
    #   Raises if source is already mapped to a different target.
    #   Rationale: directly assigning remaps={} replaces all existing remaps,
    #   add_remap is the safe incremental version.

    # remove_remap(source) -> Self
    #   Removes a single entry from remaps by source ID.


class FollowTrigger(Trigger):
    def __init__(self):
        super().__init__(obj_id.Trigger.FOLLOW)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    duration      = ObjField[float](obj_prop.Trigger.Follow.DURATION)
    """Duration in seconds (a10)"""
    target_id     = ObjField[int](obj_prop.Trigger.Follow.TARGET_ID)
    """Group ID that follows (a51)"""
    follow_target = ObjField[int](obj_prop.Trigger.Follow.FOLLOW_TARGET)
    """Group ID to follow (a71)"""
    mod_x         = ObjField[float](obj_prop.Trigger.Follow.MOD_X)
    """X movement multiplier (a72)"""
    mod_y         = ObjField[float](obj_prop.Trigger.Follow.MOD_Y)
    """Y movement multiplier (a73)"""


class ShakeTrigger(Trigger):
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


class AnimateTrigger(Trigger):
    def __init__(self):
        super().__init__(obj_id.Trigger.ANIMATE)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    target_id    = ObjField[int](obj_prop.Trigger.Animate.TARGET_ID)
    """Group ID of the animated object (a51)"""
    animation_id = ObjField[int](obj_prop.Trigger.Animate.ANIMATION_ID)
    """Animation ID to play (a76)"""


class TouchTrigger(Trigger):
    def __init__(self):
        super().__init__(obj_id.Trigger.TOUCH)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    group_id    = ObjField[int](obj_prop.Trigger.Touch.GROUP_ID)
    """Group ID to activate on touch (a51)"""
    hold_mode   = ObjField[bool](obj_prop.Trigger.Touch.HOLD_MODE)
    """Activate while held, deactivate on release (a81)"""
    toggle_mode = ObjField[TouchEnum.Mode](obj_prop.Trigger.Touch.TOGGLE_MODE)
    """Toggle behaviour: flip/on/off (a82)"""
    dual_mode   = ObjField[bool](obj_prop.Trigger.Touch.DUAL_MODE)
    """Activate on both player touch areas (a89)"""
    only_player = ObjField[TouchEnum.OnlyPlayer](obj_prop.Trigger.Touch.ONLY_PLAYER)
    """Restrict to player 1, player 2, or both (a198)"""


class CountTrigger(Trigger):
    def __init__(self):
        super().__init__(obj_id.Trigger.COUNT)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    target_id      = ObjField[int](obj_prop.Trigger.Count.TARGET_ID)
    """Group ID to activate when count is reached (a51)"""
    activate_group = ObjField[bool](obj_prop.Trigger.Count.ACTIVATE_GROUP)
    """True = activate group, False = deactivate (a56)"""
    count          = ObjField[int](obj_prop.Trigger.Count.COUNT)
    """Item count value to trigger at (a77)"""
    item_id        = ObjField[int](obj_prop.Trigger.Count.ITEM_ID)
    """Item ID to watch (a80)"""
    multi_activate = ObjField[bool](obj_prop.Trigger.Count.MULTI_ACTIVATE)
    """Trigger every time count is reached, not just the first (a104)"""
