
from typing import Any, Callable, Literal, Union, get_args, get_origin, Required
from gmdbuilder.mappings import obj_id, obj_prop
from gmdbuilder import object_types as td


ObjectType = td.ObjectType
tid = obj_id.Trigger
cid = obj_id.Collectible
ID_TO_TYPEDDICT: dict[int, type[ObjectType]] = {
    tid.ALPHA: td.AlphaType,
    tid.ADV_FOLLOW: td.AdvFollowType,
    tid.ADV_RANDOM: td.AdvRandomType,
    tid.ANIMATE: td.AnimateType,
    tid.ANIMATE_KEYFRAME: td.AnimateKeyframeType,
    tid.ARROW: td.ArrowType,
    tid.BPM: td.BpmType,
    tid.CAMERA_EDGE: td.CameraEdgeType,
    tid.CAMERA_GUIDE: td.CameraGuideType,
    tid.CAMERA_MODE: td.CameraModeType,
    tid.CHANGE_BG: td.ChangeBgType,
    tid.CHANGE_GR: td.ChangeGrType,
    tid.CHANGE_MG: td.ChangeMgType,
    tid.CHECKPOINT: td.CheckpointType,
    tid.COUNT: td.CountType,
    tid.COLOR: td.ColorType,
    tid.COLLISION: td.CollisionType,
    tid.COLLISION_BLOCK: td.CollisionBlockType,
    tid.EDIT_ADV_FOLLOW: td.EditAdvFollowType,
    tid.EDIT_MG: td.MgEditType,
    tid.END: td.EndType,
    tid.FOLLOW: td.FollowType,
    tid.FOLLOW_PLAYER_Y: td.FollowPlayerYType,
    tid.GAMEPLAY_OFFSET: td.GameplayOffsetType,
    tid.GRADIENT: td.GradientType,
    tid.GRAVITY: td.GravityType,
    tid.INSTANT_COLLISION: td.InstantCollisionType,
    tid.INSTANT_COUNT: td.InstantCountType,
    tid.ITEM_COMPARE: td.ItemCompareType,
    tid.ITEM_EDIT: td.ItemEditType,
    tid.ITEM_PERSIST: td.ItemPersistType,
    tid.KEYFRAME: td.KeyframeType,
    tid.LINK_VISIBLE: td.LinkVisibleType,
    tid.MG_SPEED: td.MgSpeedType,
    tid.MOVE: td.MoveType,
    tid.ON_DEATH: td.OnDeathType,
    tid.OPTIONS: td.OptionsType,
    tid.OFFSET_CAMERA: td.OffsetCameraType,
    tid.PICKUP: td.PickupType,
    tid.PLAYER_CONTROL: td.PlayerControlType,
    tid.PULSE: td.PulseType,
    tid.RANDOM: td.RandomType,
    tid.RESET: td.ResetType,
    tid.ROTATE: td.RotateType,
    tid.ROTATE_CAMERA: td.RotateCameraType,
    tid.SCALE: td.ScaleType,
    tid.SEQUENCE: td.SequenceType,
    tid.SFX: td.SfxType,
    tid.STOP: td.StopType,
    tid.SHAKE: td.ShakeType,
    tid.SONG: td.SongType,
    tid.SPAWN: td.SpawnType,
    tid.SPAWN_PARTICLE: td.SpawnParticleType,
    tid.STATE_BLOCK: td.StateBlockType,
    tid.STATIC_CAMERA: td.StaticCameraType,
    tid.TELEPORT: td.TeleportType,
    tid.TIME: td.TimeType,
    tid.TIMEWARP: td.TimewarpType,
    tid.TIME_CONTROL: td.TimeControlType,
    tid.TIME_EVENT: td.TimeEventType,
    tid.TOGGLE: td.ToggleType,
    tid.TOGGLE_BLOCK: td.ToggleBlockType,
    tid.TOUCH: td.TouchType,
    tid.UI: td.UiType,
    tid.ZOOM_CAMERA: td.ZoomCameraType,
    cid.SECRET_COIN: td.CoinType,
    cid.KEY: td.CollectibleType,
    cid.USER_COIN: td.CollectibleType,
    cid.SMALL_COIN: td.CollectibleType,
    914: td.TextType,
}
"""Unfinished mapping of Object IDs to non-common Object TypedDicts"""

ID_TO_ALLOWED_KEYS = {
    k: set(v.__required_keys__) | set(v.__optional_keys__) 
    for k, v in ID_TO_TYPEDDICT.items()
}

COMMON_ALLOWED_KEYS = td.ObjectType.__required_keys__ | td.ObjectType.__optional_keys__

UNHASHABLE_VALUE_KEYS = {
    obj_prop.GROUPS,
    obj_prop.PARENT_GROUPS,
    obj_prop.Trigger.Spawn.REMAPS,
    obj_prop.Trigger.AdvRandom.TARGETS,
    obj_prop.Trigger.Event.EVENTS,
    obj_prop.Trigger.Sequence.SEQUENCE
}


hashable_value_key_to_isinstance: dict[str, Callable[[Any], bool]] = {}


# ACTUAL FUNCTION WE CARE ABOUT
def value_is_correct_type(key: str, v: Any) -> bool:
    """Check if value v is of the correct type for key."""
    if key in UNHASHABLE_VALUE_KEYS:
        raise ValueError(f"Key {key} has unhashable value, cannot be type checked.")
    if key not in hashable_value_key_to_isinstance:
        raise ValueError(f"No type information available for key {key!r} : {v!r}")
    return hashable_value_key_to_isinstance[key](v)


def _type_to_isinstance(typ: Any) -> Callable[[Any], bool]:
    """Convert a type annotation to a runtime check function."""
    origin = get_origin(typ)
    
    if origin is Required:
        inner_type = get_args(typ)[0]
        return _type_to_isinstance(inner_type)
    if origin is Union:
        checks = [_type_to_isinstance(t) for t in get_args(typ)]
        return lambda v: any(check(v) for check in checks)
    elif origin is Literal:
        allowed = get_args(typ)
        return lambda v: v in allowed
    elif typ is Any:
        return lambda v: True
    elif isinstance(typ, type):
        if typ is bool:
            return lambda v: isinstance(v, bool)
        elif typ is float:
            return lambda v: isinstance(v, (int, float)) and not isinstance(v, bool)
        elif typ is int:
            return lambda v: isinstance(v, int) and not isinstance(v, bool)
        else:
            return lambda v: isinstance(v, typ)

    raise ValueError(f"Unsupported type annotation: {typ!r}")


def _typeddict_to_isinstance(typeddict: type):
    """Extract type annotations from a TypedDict and populate runtime checks."""
    annotations: dict[str, Any] = {}
    
    for base in reversed(typeddict.__mro__):
        if hasattr(base, '__annotations__'):
            annotations.update(base.__annotations__)
    
    for key, typ in annotations.items():
        if key in hashable_value_key_to_isinstance: continue
        if key in UNHASHABLE_VALUE_KEYS: continue
        
        try:
            hashable_value_key_to_isinstance[key] = _type_to_isinstance(typ)
        except ValueError as e:
            print(f"Warning: Skipping key {key!r} with type {typ}: {e}")


_typeddict_to_isinstance(td.ObjectType)
for tyd in ID_TO_TYPEDDICT.values():
    _typeddict_to_isinstance(tyd)
