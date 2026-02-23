
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
    tid.BG_EFFECT_ENABLE: td.TriggerType,
    tid.BG_EFFECT_DISABLE: td.TriggerType,
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
    tid.EVENT: td.EventType,
    tid.EDIT_SFX: td.SfxType,
    tid.EDIT_SONG: td.SongType,
    tid.END: td.EndType,
    tid.FOLLOW: td.FollowType,
    tid.FOLLOW_PLAYER_Y: td.FollowPlayerYType,
    tid.FORCE_BLOCK: td.ForceBlockType,
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
    tid.PLAYER_HIDE: td.TriggerType,
    tid.PLAYER_SHOW: td.TriggerType,
    tid.Enter.MOVE: td.EffectType,
    tid.EnterPreset.FADE_ONLY: td.TriggerType,
    cid.KEY: td.CollectibleType,
    cid.USER_COIN: td.AnimatedType,
    cid.SMALL_COIN: td.CollectibleType,
    obj_id.TEXT: td.TextType,
    obj_id.ITEM_LABEL: td.ItemLabelType,
    obj_id.PARTICLE_OBJECT: td.ParticleType,
    obj_id.Orb.BLACK: td.TriggerType,
    obj_id.Orb.BLUE: td.TriggerType,
    obj_id.Orb.GREEN: td.TriggerType,
    obj_id.Orb.RED: td.TriggerType,
    obj_id.Orb.YELLOW: td.TriggerType,
    obj_id.Orb.PINK: td.TriggerType,
    obj_id.Orb.SPIDER: td.TriggerType,
    obj_id.Orb.TELEPORT: td.TriggerType,
    obj_id.Orb.TOGGLE: td.ToggleBlockType,
    obj_id.Orb.DASH_GREEN: td.DashType,
    obj_id.Orb.DASH_PINK: td.DashType,
    obj_id.Portal.Teleport.ENTER: td.PortalType,
    obj_id.Portal.Teleport.EXIT: td.ExitPortalType,
    obj_id.Portal.Teleport.LINKED: td.PortalType,
    3002: td.AnimatedType,
    1020: td.SawType,
    1582: td.SawType,
    1709: td.SawType,
}
"""Unfinished mapping of Object IDs to non-common Object TypedDicts"""


def _assign_id_types(cls: object, obj_type: type[ObjectType]):
    if isinstance(cls, range) or isinstance(cls, list):
        for c in cls:
            if isinstance(c, int):
                ID_TO_TYPEDDICT[c] = obj_type
    else:
        for obj in [v for v in vars(cls).values() if isinstance(v, int)]:
            ID_TO_TYPEDDICT[obj] = obj_type

_assign_id_types(obj_id.Pad, td.TriggerType)
_assign_id_types(obj_id.Portal, td.GamemodePortalType)
_assign_id_types(obj_id.Speed, td.TriggerType)
_assign_id_types(obj_id.Modifier, td.TriggerType)
_assign_id_types(obj_id.Trigger.Shader, td.ShaderType)
_assign_id_types(obj_id.Trigger.Area, td.EffectType)
_assign_id_types(range(920, 925), td.AnimatedType)
_assign_id_types(range(1849, 1859), td.AnimatedType)
_assign_id_types([1936, 1937, 1938, 1939], td.AnimatedType)
_assign_id_types(range(2020, 2056), td.AnimatedType)
_assign_id_types([2864, 2865], td.AnimatedType)
_assign_id_types(range(2867, 2895), td.AnimatedType)
_assign_id_types([3000, 3001, 3002], td.AnimatedType)
_assign_id_types([85, 86, 87, 88, 89], td.SawType)
_assign_id_types([97, 98], td.SawType)
_assign_id_types([137, 138, 139], td.SawType)
_assign_id_types([154, 155, 156], td.SawType)
_assign_id_types(range(180, 189), td.SawType)
_assign_id_types([222, 223, 224], td.SawType)
_assign_id_types([375, 376, 377, 378], td.SawType)
_assign_id_types(range(394, 400), td.SawType)

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
