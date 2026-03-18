from typing import Self

from gmdbuilder.classes.object import ObjField
from gmdbuilder.classes.trigger import Trigger
from gmdbuilder.mappings import obj_prop, obj_id
from gmdbuilder.mappings.obj_enum import Touch as TouchEnum


class Spawn(Trigger):
    """Spawn trigger. Inherits: Object -> Trigger -> Spawn"""

    def __init__(self):
        super().__init__(obj_id.Trigger.SPAWN)

    # ------------------------------------------------------------------
    # Methods
    # ------------------------------------------------------------------

    def add_remap(self, source: int, target: int) -> Self:
        """Add a single source->target remap entry. Raises if source is already mapped differently."""
        current: dict[int, int] = dict(self.obj.get(obj_prop.Trigger.Spawn.REMAPS) or {})
        if source in current and current[source] != target:
            raise ValueError(
                f"Group {source} is already remapped to {current[source]}, cannot remap to {target}"
            )
        current[source] = target
        self.remaps = current
        return self

    def remove_remap(self, source: int) -> Self:
        """Remove a single remap entry by source ID."""
        current: dict[int, int] = dict(self.obj.get(obj_prop.Trigger.Spawn.REMAPS) or {})
        current.pop(source, None)
        self.remaps = current
        return self

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    target_id = ObjField[int](obj_prop.Trigger.Spawn.TARGET_ID)
    """Group ID to spawn (a51)"""

    delay = ObjField[float](obj_prop.Trigger.Spawn.DELAY)
    """Delay before spawning in seconds (a63)"""

    disable_preview = ObjField[bool](obj_prop.Trigger.Spawn.DISABLE_PREVIEW)
    """Disable editor preview (a102)"""

    ordered = ObjField[bool](obj_prop.Trigger.Spawn.ORDERED)
    """Spawn triggers left-to-right in order (a441)"""

    remaps = ObjField[dict[int, int]](obj_prop.Trigger.Spawn.REMAPS)
    """Group ID remaps applied when spawning: {source: target} (a442)"""

    delay_rand = ObjField[float](obj_prop.Trigger.Spawn.DELAY_RAND)
    """Random additional delay range in seconds (a556)"""

    reset_remap = ObjField[bool](obj_prop.Trigger.Spawn.RESET_REMAP)
    """Block incoming remaps from affecting this trigger's spawns (a581)"""




class Touch(Trigger):
    """Touch trigger. Inherits: Object -> Trigger -> Touch"""

    def __init__(self):
        super().__init__(obj_id.Trigger.TOUCH)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    group_id = ObjField[int](obj_prop.Trigger.Touch.GROUP_ID)
    """Group ID to activate on touch (a51)"""

    hold_mode = ObjField[bool](obj_prop.Trigger.Touch.HOLD_MODE)
    """Activate while held, deactivate on release (a81)"""

    toggle_mode = ObjField[TouchEnum.Mode](obj_prop.Trigger.Touch.TOGGLE_MODE)
    """Toggle behaviour: flip/on/off (a82)"""

    dual_mode = ObjField[bool](obj_prop.Trigger.Touch.DUAL_MODE)
    """Activate on both player touch areas (a89)"""

    only_player = ObjField[TouchEnum.OnlyPlayer](obj_prop.Trigger.Touch.ONLY_PLAYER)
    """Restrict to player 1, player 2, or both (a198)"""
