from typing import Self

from gmdbuilder.classes.object import ObjField
from gmdbuilder.classes.trigger import Trigger
from gmdbuilder.mappings import obj_prop, obj_id
from gmdkit.models.prop.hsv import HSV


class Color(Trigger):
    """Color trigger. Inherits: Object -> Trigger -> Color"""

    def __init__(self):
        super().__init__(obj_id.Trigger.COLOR)

    # ------------------------------------------------------------------
    # Methods
    # ------------------------------------------------------------------

    def set_rgb(self, r: int, g: int, b: int, duration: float = 0) -> Self:
        """Set red, green, blue and duration in one call."""
        self.red = r
        self.green = g
        self.blue = b
        self.duration = duration
        return self

    def set_hex(self, hex_str: str, duration: float = 0) -> Self:
        """Parse a hex string like '#FF8800' and set red/green/blue and duration."""
        hex_str = hex_str.lstrip('#')
        if len(hex_str) != 6:
            raise ValueError(f"Invalid hex string: {hex_str!r}")
        self.red   = int(hex_str[0:2], 16)
        self.green = int(hex_str[2:4], 16)
        self.blue  = int(hex_str[4:6], 16)
        self.duration = duration
        return self

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    red = ObjField[int](obj_prop.Trigger.Color.RED)
    """Red channel 0-255 (a7)"""

    green = ObjField[int](obj_prop.Trigger.Color.GREEN)
    """Green channel 0-255 (a8)"""

    blue = ObjField[int](obj_prop.Trigger.Color.BLUE)
    """Blue channel 0-255 (a9)"""

    duration = ObjField[float](obj_prop.Trigger.Color.DURATION)
    """Duration in seconds (a10)"""

    tint_ground = ObjField[bool](obj_prop.Trigger.Color.TINT_GROUND)
    """Tint ground with this color (a14)"""

    player_1 = ObjField[bool](obj_prop.Trigger.Color.PLAYER_1)
    """Copy player 1 color (a15)"""

    player_2 = ObjField[bool](obj_prop.Trigger.Color.PLAYER_2)
    """Copy player 2 color (a16)"""

    blending = ObjField[bool](obj_prop.Trigger.Color.BLENDING)
    """Enable additive blending (a17)"""

    target = ObjField[int](obj_prop.Trigger.Color.CHANNEL)
    """Color channel ID to set (a23)"""

    opacity = ObjField[float](obj_prop.Trigger.Color.OPACITY)
    """Opacity 0.0-1.0 (a35)"""

    hsv = ObjField[HSV](obj_prop.Trigger.Color.HSV)
    """HSV adjustment (a49)"""

    copy_id = ObjField[int](obj_prop.Trigger.Color.COPY_ID)
    """Color channel ID to copy from (a50)"""

    copy_opacity = ObjField[bool](obj_prop.Trigger.Color.COPY_OPACITY)
    """Copy opacity from copied channel (a60)"""

    disable_legacy_hsv = ObjField[bool](obj_prop.Trigger.Color.DISABLE_LEGACY_HSV)
    """Disable legacy HSV effect (a210)"""


class Pulse(Trigger):
    """Pulse trigger. Inherits: Object -> Trigger -> Pulse"""

    def __init__(self):
        super().__init__(obj_id.Trigger.PULSE)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    red = ObjField[int](obj_prop.Trigger.Pulse.RED)
    """Red channel 0-255 (a7)"""

    green = ObjField[int](obj_prop.Trigger.Pulse.GREEN)
    """Green channel 0-255 (a8)"""

    blue = ObjField[int](obj_prop.Trigger.Pulse.BLUE)
    """Blue channel 0-255 (a9)"""

    fade_in = ObjField[float](obj_prop.Trigger.Pulse.FADE_IN)
    """Fade in duration in seconds (a45)"""

    hold = ObjField[float](obj_prop.Trigger.Pulse.HOLD)
    """Hold duration in seconds (a46)"""

    fade_out = ObjField[float](obj_prop.Trigger.Pulse.FADE_OUT)
    """Fade out duration in seconds (a47)"""

    use_hsv = ObjField[bool](obj_prop.Trigger.Pulse.USE_HSV)
    """Use HSV mode instead of RGB (a48)"""

    hsv = ObjField[HSV](obj_prop.Trigger.Pulse.HSV)
    """HSV adjustment used when use_hsv=True (a49)"""

    copy_id = ObjField[int](obj_prop.Trigger.Pulse.COPY_ID)
    """Color channel ID to copy from (a50)"""

    target_id = ObjField[int](obj_prop.Trigger.Pulse.TARGET_ID)
    """Group or color channel ID to pulse (a51)"""

    target_type = ObjField[bool](obj_prop.Trigger.Pulse.TARGET_TYPE)
    """False = color channel target, True = group target (a52)"""

    main_only = ObjField[bool](obj_prop.Trigger.Pulse.MAIN_ONLY)
    """Only pulse main color (a65)"""

    detail_only = ObjField[bool](obj_prop.Trigger.Pulse.DETAIL_ONLY)
    """Only pulse detail color (a66)"""

    exclusive = ObjField[bool](obj_prop.Trigger.Pulse.EXCLUSIVE)
    """Override other active pulse triggers (a86)"""

    disable_static_hsv = ObjField[bool](obj_prop.Trigger.Pulse.DISABLE_STATIC_HSV)
    """Disable static HSV (a210)"""


class Alpha(Trigger):
    """Alpha trigger. Inherits: Object -> Trigger -> Alpha"""

    def __init__(self):
        super().__init__(obj_id.Trigger.ALPHA)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    duration = ObjField[float](obj_prop.Trigger.Alpha.DURATION)
    """Duration in seconds (a10)"""

    opacity = ObjField[float](obj_prop.Trigger.Alpha.OPACITY)
    """Target opacity 0.0-1.0 (a35)"""

    target_id = ObjField[int](obj_prop.Trigger.Alpha.TARGET_ID)
    """Target ID to change opacity of (a51)"""


class Toggle(Trigger):
    """Toggle trigger. Inherits: Object -> Trigger -> Toggle"""

    def __init__(self):
        super().__init__(obj_id.Trigger.TOGGLE)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    target_id = ObjField[int](obj_prop.Trigger.Toggle.TARGET_ID)
    """Target ID to toggle (a51)"""

    activate_group = ObjField[bool](obj_prop.Trigger.Toggle.ACTIVATE_GROUP)
    """True = activate, False = deactivate (a56)"""


class Animate(Trigger):
    """Animate trigger. Inherits: Object -> Trigger -> Animate"""

    def __init__(self):
        super().__init__(obj_id.Trigger.ANIMATE)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    target_id = ObjField[int](obj_prop.Trigger.Animate.TARGET_ID)
    """Group ID of the animated object (a51)"""

    animation_id = ObjField[int](obj_prop.Trigger.Animate.ANIMATION_ID)
    """Animation ID to play (a76)"""
