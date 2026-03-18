from gmdbuilder.classes.object import Object, ObjField
from gmdbuilder.mappings import obj_prop


class Trigger(Object):
    """
    Base class for all trigger objects with shared trigger properties.

    Inherits: Object -> Trigger
    """

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
