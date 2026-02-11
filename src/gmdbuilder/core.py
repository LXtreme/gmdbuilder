"""Core utilities for working with ObjectType dicts."""

from functools import lru_cache
from typing import Any, Literal, TypeVar, cast, overload
from gmdkit.serialization import type_cast as tc
from gmdkit.models.object import ObjectList as KitObjectList, Object as KitObject
from gmdkit.casting.object_props import PROPERTY_DECODERS, PROPERTY_ENCODERS # type: ignore
from gmdbuilder.mappings.obj_prop import ObjProp
from gmdbuilder.futils import translate_list_string, translate_map_string
from gmdbuilder.mappings.obj_id import ObjId
from gmdbuilder.validation import validate
import gmdbuilder.object_typeddict as td
ObjectType = td.ObjectType

T = TypeVar('T', bound=ObjectType)


RAW_DECODERS = {}
for key, decoder in PROPERTY_DECODERS.items():
    # Keep basic types as-is
    if decoder in (tc.to_bool, int, float):
        RAW_DECODERS[key] = decoder
    else:
        RAW_DECODERS[key] = str

RAW_ENCODERS = {}
for key, encoder in PROPERTY_ENCODERS.items(): # type: ignore
    if encoder in (tc.from_bool, tc.from_float):
        RAW_ENCODERS[key] = encoder
    else:
        RAW_ENCODERS[key] = str


class RawObject(KitObject):
    DECODER = staticmethod(tc.dict_cast(RAW_DECODERS, numkey=True)) # type: ignore
    ENCODER = staticmethod(tc.dict_cast(RAW_ENCODERS, default=tc.serialize)) # type: ignore

class RawObjectList(KitObjectList):
    DECODER = RawObject.from_string # type: ignore
    ENCODER = staticmethod(lambda obj: obj.to_string()) # type: ignore


id = ObjId.Trigger
ID_TO_TYPEDDICT = {
    id.ALPHA: td.AlphaType,
    id.ADV_FOLLOW: td.AdvFollowType,
    id.ADV_RANDOM: td.AdvRandomType,
    id.ANIMATE: td.AnimateType,
    id.ANIMATE_KEYFRAME: td.AnimateKeyframeType,
    id.ARROW: td.ArrowType,
    id.BPM: td.BpmType,
    id.CAMERA_EDGE: td.CameraEdgeType,
    id.CAMERA_GUIDE: td.CameraGuideType,
    id.CAMERA_MODE: td.CameraModeType,
    id.CHANGE_BG: td.ChangeBgType,
    id.CHANGE_GR: td.ChangeGrType,
    id.CHANGE_MG: td.ChangeMgType,
    id.CHECKPOINT: td.CheckpointType,
    id.COUNT: td.CountType,
    id.COLOR: td.ColorType,
    id.COLLISION: td.CollisionType,
    id.COLLISION_BLOCK: td.CollisionBlockType,
    id.EDIT_ADV_FOLLOW: td.EditAdvFollowType,
    id.EDIT_MG: td.MgEditType,
    id.END: td.EndType,
    id.FOLLOW: td.FollowType,
    id.FOLLOW_PLAYER_Y: td.FollowPlayerYType,
    id.GAMEPLAY_OFFSET: td.GameplayOffsetType,
    id.GRADIENT: td.GradientType,
    id.GRAVITY: td.GravityType,
    id.INSTANT_COLLISION: td.InstantCollisionType,
    id.INSTANT_COUNT: td.InstantCountType,
    id.ITEM_COMPARE: td.ItemCompareType,
    id.ITEM_EDIT: td.ItemEditType,
    id.ITEM_PERSIST: td.ItemPersistType,
    id.KEYFRAME: td.KeyframeType,
    id.LINK_VISIBLE: td.LinkVisibleType,
    id.MG_SPEED: td.MgSpeedType,
    id.MOVE: td.MoveType,
    id.ON_DEATH: td.OnDeathType,
    id.OPTIONS: td.OptionsType,
    id.OFFSET_CAMERA: td.OffsetCameraType,
    id.PICKUP: td.PickupType,
    id.PLAYER_CONTROL: td.PlayerControlType,
    id.PULSE: td.PulseType,
    id.RANDOM: td.RandomType,
    id.RESET: td.ResetType,
    id.ROTATE: td.RotateType,
    id.ROTATE_CAMERA: td.RotateCameraType,
    id.SCALE: td.ScaleType,
    id.SEQUENCE: td.SequenceType,
    id.SFX: td.SfxType,
    id.STOP: td.StopType,
    id.SHAKE: td.ShakeType,
    id.SONG: td.SongType,
    id.SPAWN: td.SpawnType,
    id.SPAWN_PARTICLE: td.SpawnParticleType,
    id.STATE_BLOCK: td.StateBlockType,
    id.STATIC_CAMERA: td.StaticCameraType,
    id.TELEPORT: td.TeleportType,
    id.TIME: td.TimeType,
    id.TIMEWARP: td.TimewarpType,
    id.TIME_CONTROL: td.TimeControlType,
    id.TIME_EVENT: td.TimeEventType,
    id.TOGGLE: td.ToggleType,
    id.TOGGLE_BLOCK: td.ToggleBlockType,
    id.TOUCH: td.TouchType,
    id.UI: td.UiType,
    id.ZOOM_CAMERA: td.ZoomCameraType,
}
"""Unfinished mapping of Object IDs to non-common Object TypedDicts"""


class Object(dict[str, Any]):
    """
    Note: Not for users to call directly
    
    The actual dict implementation hidden behind the ObjectType TypedDict
    
    This is to intercept & validate mutations of objects and add new helpers.
    """
    __slots__ = ("_obj_id",)

    def __init__(self, obj_id: int):
        super().__init__()
        self._obj_id = int(obj_id)
        super().__setitem__("a1", self._obj_id)

    def __setitem__(self, k: str, v: Any):
        validate(self._obj_id, k, v)
        if k == ObjProp.ID:
            self._obj_id = int(v)
        super().__setitem__(k, v)

    def update(self, *args: Any, **kwargs: Any):  # type: ignore[override]
        # Construct items dict from args and kwargs
        items: dict[str, Any]
        if args:
            if len(args) != 1:
                raise TypeError(f"update() takes at most 1 positional argument ({len(args)} given)")
            __m = args[0]
            items = dict(__m)  # type: ignore[arg-type]
            items.update(kwargs)
        else:
            items = dict(kwargs)
        
        for k, v in items.items():
            validate(self._obj_id, k, v)
        if ObjProp.ID in items:
            self._obj_id = int(items[ObjProp.ID])
        super().update(items)



@lru_cache(maxsize=1024)
def _to_raw_key_cached(key: object) -> int | str:
    if isinstance(key, int):
        return key
    if not isinstance(key, str):
        raise ValueError()
    if key.startswith('k'):
        return key
    if key.startswith('a'):
        tail = key[1:]
        if tail.isdigit():
            return int(tail)
    raise ValueError()

def to_raw_object(obj: ObjectType) -> dict[int|str, Any]:
    """
    Convert ObjectType to a new raw int-keyed dict for gmdkit or debugging.
    
    Example:
        {'a1': 900, 'a2': 50} → {1: 900, 2: 50}
    """
    raw: dict[int|str, Any] = {}
    for key, value in obj.items():
        value = cast(Any, value)
        if key == ObjProp.GROUPS:
            value = '.'.join(map(str, sorted(value)))
        elif key == ObjProp.Trigger.Event.EVENTS:
            value = '.'.join(map(str, sorted(value)))
        
        try:
            raw[_to_raw_key_cached(key)] = value
        except ValueError as e:
            raise ValueError(f"Object has bad/unsupported key {key!r}:\n{obj=}") from e
    return raw


@lru_cache(maxsize=1024)
def _from_raw_key_cached(key: object) -> str:
    if isinstance(key, int):
        return f"a{key}"
    if isinstance(key, str) and (key.startswith("a") or key.startswith("k")):
        return key
    raise ValueError()


@overload
def from_raw_object(raw_obj: dict[int|str, Any]) -> ObjectType: ...
@overload
def from_raw_object(raw_obj: dict[int|str, Any], *, obj_type: type[T]) -> T: ...
def from_raw_object(
    raw_obj: dict[int|str, Any], *,
    obj_type: type[ObjectType] | None = None
) -> ObjectType:
    """
    Convert raw int-keyed dict from gmdkit to a new ObjectType.
    
    Example:
        {1: 900, 2: 50} → {'a1': 900, 'a2': 50}
    """
    
    if (key := 57) in raw_obj:
        raw_obj[key] = translate_list_string(raw_obj[key])
    if (key := 442) in raw_obj:
        raw_obj[key] = translate_map_string(raw_obj[key])
    
    converted: ObjectType = { ObjProp.ID: -1 }
    
    for key, value in raw_obj.items():
        try:
            converted[_from_raw_key_cached(key)] = value
        except ValueError as e:
            raise ValueError(f"Object has bad/unsupported key {key!r}: \n{raw_obj=}") from e
    
    if int(converted[ObjProp.ID]) == -1:
        raise TypeError(f"Missing required Object ID key 1 in raw object: \n{raw_obj=}")
    
    wrapped = Object(converted[ObjProp.ID])
    wrapped.update(converted)
    return cast(ObjectType, wrapped)


@overload
def from_object_string(obj_string: str) -> ObjectType: ...
@overload
def from_object_string(obj_string: str, *, obj_type: type[T]) -> T: ...
def from_object_string(obj_string: str, *, obj_type: type[ObjectType] | None = None) -> ObjectType:
    """
    Convert GD level object string to ObjectType.
    
    Example:
        "1,1,2,50,3,45;" → {'a1': 1, 'a2': 50, 'a3': 45}
    """
    return from_raw_object(RawObject.from_string(obj_string))


@overload
def new_object(object_id: Literal[3016]) -> td.AdvFollowType: ...
@overload
def new_object(object_id: Literal[1346]) -> td.RotateType: ...
@overload
def new_object(object_id: Literal[901]) -> td.MoveType: ...
@overload
def new_object(object_id: int) -> ObjectType: ...
def new_object(object_id: int) -> ObjectType:
    """
    Create a new Object with defaults from gmdkit.
        
    Returns:
        ObjectType dict with default properties (using 'a<num>' keys)
    """
    # Convert from gmdkit's {1: val, 2: val} to our {'a1': val, 'a2': val}
    return from_raw_object(RawObject.default(object_id))
