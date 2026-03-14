
from typing import Any, Self, TypeVar, Generic, overload

from gmdbuilder import new_obj, obj_prop
from gmdbuilder.object import ValidatedObject
from gmdbuilder.object_types import ObjectType
from gmdkit.models.prop.hsv import HSV

def _get_autoappend_level():
    from gmdbuilder.level import get_autoappend_level
    return get_autoappend_level()

T = TypeVar("T")

class ObjField(Generic[T]):
    def __init__(self, key: Any) -> None:
        self.key = key

    @overload
    def __get__(self, instance: None, owner: type[Any]) -> "ObjField[T]": ...
    @overload
    def __get__(self, instance: object, owner: type[Any] | None = None) -> T: ...
    def __get__(self, instance: object | None, owner: type[Any] | None = None) -> T | "ObjField[T]":
        if instance is None:
            return self
        return instance.obj[self.key] # type: ignore[attr-defined]

    def __set__(self, instance: Any, value: T) -> None:
        instance.obj[self.key] = value


class Object:
    """Wrapper base class for common objects with typed properties and helper methods."""
    def __init__(self, obj_id: int):
        self.obj = new_obj(obj_id)

    @classmethod
    def wrap(cls, obj: ObjectType) -> Self:
        """Wrap an existing ObjectType dict without creating a new object."""
        instance = cls.__new__(cls)
        instance.obj = ValidatedObject.wrap_object(obj)
        return instance
    
    # ------------------------------------------------------------------
    # Methods
    # ------------------------------------------------------------------

    def add_to_group(self, *group_ids: int) -> Self:
        """Add one or more group IDs to this object's groups set."""
        existing = self.obj.get(obj_prop.GROUPS)
        current: set[int] = set(existing) if existing is not None else set()
        current.update(group_ids)
        self.obj[obj_prop.GROUPS] = current
        return self

    def reset_transform(self) -> Self:
        """
        Reset position, rotation, and scale back to their default values.
        Useful when constructing a clean object from a loaded level's state.
        """
        self.obj[obj_prop.X] = 0.0
        self.obj[obj_prop.Y] = 0.0
        self.obj[obj_prop.ROTATION] = 0.0
        self.obj[obj_prop.SCALE_X] = 1.0
        self.obj[obj_prop.SCALE_Y] = 1.0
        return self

    def set_position(self, x: float, y: float) -> Self:
        self.obj[obj_prop.X] = x
        self.obj[obj_prop.Y] = y
        return self

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(obj={self.obj!r})"
    
    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    id = ObjField[int](obj_prop.ID)
    """Object ID (a1)"""
    
    x = ObjField[float](obj_prop.X)
    """X position (a2)"""
    
    y = ObjField[float](obj_prop.Y)
    """Y position (a3)"""
    
    flip_x = ObjField[bool](obj_prop.FLIP_X)
    """Flip horizontally (a4)"""
    
    flip_y = ObjField[bool](obj_prop.FLIP_Y)
    """Flip vertically (a5)"""
    
    rotation = ObjField[float](obj_prop.ROTATION)
    """Rotation in degrees (a6)"""
    
    old_color_id = ObjField[int](obj_prop.OLD_COLOR_ID)
    """Legacy color ID 0-8 (a19)"""
    
    editor_l1 = ObjField[int](obj_prop.EDITOR_L1)
    """Editor layer 1 (a20)"""
    
    color_1 = ObjField[int](obj_prop.COLOR_1)
    """Color channel 1 (a21)"""
    
    color_2 = ObjField[int](obj_prop.COLOR_2)
    """Color channel 2 (a22)"""
    
    z_layer = ObjField[int](obj_prop.Z_LAYER)
    """Z layer (a24)"""
    
    z_order = ObjField[int](obj_prop.Z_ORDER)
    """Z order (a25)"""
    
    old_scale = ObjField[float](obj_prop.OLD_SCALE)
    """Legacy scale (a32)"""
    
    group_parent = ObjField[bool](obj_prop.GROUP_PARENT)
    """Is group parent (a34)"""
    
    hsv_enabled_1 = ObjField[bool](obj_prop.HSV_ENABLED_1)
    """HSV enabled for color 1 (a41)"""
    
    hsv_enabled_2 = ObjField[bool](obj_prop.HSV_ENABLED_2)
    """HSV enabled for color 2 (a42)"""
    
    hsv_1 = ObjField[HSV](obj_prop.HSV_1)
    """HSV adjustment for color 1 (a43)"""
    
    hsv_2 = ObjField[HSV](obj_prop.HSV_2)
    """HSV adjustment for color 2 (a44)"""
    
    groups = ObjField[set[int]](obj_prop.GROUPS)
    """Group IDs this object belongs to (a57)"""
    
    editor_l2 = ObjField[int](obj_prop.EDITOR_L2)
    """Editor layer 2 (a61)"""
    
    dont_fade = ObjField[bool](obj_prop.DONT_FADE)
    """Disable fade-in on enter (a64)"""
    
    dont_enter = ObjField[bool](obj_prop.DONT_ENTER)
    """Disable enter animation (a67)"""
    
    no_glow = ObjField[bool](obj_prop.NO_GLOW)
    """Disable glow (a96)"""
    
    high_detail = ObjField[bool](obj_prop.HIGH_DETAIL)
    """Mark as high detail (a103)"""
    
    linked_group = ObjField[int](obj_prop.LINKED_GROUP)
    """Linked group ID (a108)"""
    
    no_effects = ObjField[bool](obj_prop.NO_EFFECTS)
    """Disable effects (a116)"""
    
    no_touch = ObjField[bool](obj_prop.NO_TOUCH)
    """Disable touch (a121)"""
    
    scale_x = ObjField[float](obj_prop.SCALE_X)
    """X scale (a128)"""
    
    scale_y = ObjField[float](obj_prop.SCALE_Y)
    """Y scale (a129)"""
    
    skew_x = ObjField[float](obj_prop.SKEW_X)
    """X skew (a131)"""
    
    skew_y = ObjField[float](obj_prop.SKEW_Y)
    """Y skew (a132)"""
    
    passable = ObjField[bool](obj_prop.PASSABLE)
    """Player can pass through (a134)"""
    
    hide = ObjField[bool](obj_prop.HIDE)
    """Hide object (a135)"""
    
    nonstick_x = ObjField[bool](obj_prop.NONSTICK_X)
    """No horizontal slope stick (a136)"""
    
    ice_block = ObjField[bool](obj_prop.ICE_BLOCK)
    """Ice block behaviour (a137)"""
    
    color_1_index = ObjField[int](obj_prop.COLOR_1_INDEX)
    """Color 1 index (a155)"""
    
    color_2_index = ObjField[int](obj_prop.COLOR_2_INDEX)
    """Color 2 index (a156)"""
    
    grip_slope = ObjField[bool](obj_prop.GRIP_SLOPE)
    """Grip on slope (a193)"""
    
    target_player_2 = ObjField[bool](obj_prop.TARGET_PLAYER_2)
    """Target player 2 (a200)"""
    
    parent_groups = ObjField[set[int]](obj_prop.PARENT_GROUPS)
    """Parent group IDs (a274)"""
    
    area_parent = ObjField[bool](obj_prop.AREA_PARENT)
    """Is area parent (a279)"""
    
    nonstick_y = ObjField[bool](obj_prop.NONSTICK_Y)
    """No vertical slope stick (a289)"""
    
    enter_channel = ObjField[int](obj_prop.ENTER_CHANNEL)
    """Enter effect channel (a343)"""
    
    scale_stick = ObjField[bool](obj_prop.SCALE_STICK)
    """Scale stick (a356)"""
    
    disable_grid_snap = ObjField[bool](obj_prop.DISABLE_GRID_SNAP)
    """Disable grid snap (a370)"""
    
    no_audio_scale = ObjField[bool](obj_prop.NO_AUDIO_SCALE)
    """Disable audio scale (a372)"""
    
    material = ObjField[int](obj_prop.MATERIAL)
    """Material ID (a446)"""
    
    extra_sticky = ObjField[bool](obj_prop.EXTRA_STICKY)
    """Extra sticky (a495)"""
    
    dont_boost_y = ObjField[bool](obj_prop.DONT_BOOST_Y)
    """Disable Y boost (a496)"""
    
    single_color_type = ObjField[int](obj_prop.SINGLE_COLOR_TYPE)
    """Single color type 0-2 (a497)"""
    
    no_particle = ObjField[bool](obj_prop.NO_PARTICLE)
    """Disable particle (a507)"""
    
    dont_boost_x = ObjField[bool](obj_prop.DONT_BOOST_X)
    """Disable X boost (a509)"""
    
    extended_collision = ObjField[bool](obj_prop.EXTENDED_COLLISION)
    """Extended collision (a511)"""
