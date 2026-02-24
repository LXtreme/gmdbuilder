
from typing import Any, Callable, Literal, Union, get_args, get_origin, Required
from gmdbuilder.mappings import obj_id, obj_prop
from gmdbuilder import object_types as td

ObjectType = td.ObjectType
tid = obj_id.Trigger
cid = obj_id.Collectible
ID_TO_TYPEDDICT: dict[int, type[ObjectType]] = {
    obj_id.Portal.GRAVITY_NORMAL: td.GamemodePortalType,
    obj_id.Portal.GRAVITY_INVERTED: td.GamemodePortalType,
    obj_id.Portal.CUBE: td.GamemodePortalType,
    obj_id.Portal.SHIP: td.GamemodePortalType,
    20: td.TriggerType,
    tid.EnterPreset.FADE_ONLY: td.TriggerType,
    tid.EnterPreset.FADE_BOTTOM: td.TriggerType,
    tid.EnterPreset.FADE_TOP: td.TriggerType,
    tid.EnterPreset.FADE_LEFT: td.TriggerType,
    tid.EnterPreset.FADE_RIGHT: td.TriggerType,
    tid.EnterPreset.SCALE_UP: td.TriggerType,
    tid.EnterPreset.SCALE_DOWN: td.TriggerType,
    tid.TRAIL_ENABLE: td.TriggerType,
    tid.TRAIL_DISABLE: td.TriggerType,
    obj_id.Pad.YELLOW: td.TriggerType,
    obj_id.Orb.YELLOW: td.TriggerType,
    40: td.TriggerType,
    obj_id.Portal.MIRROR_ENTER: td.GamemodePortalType,
    obj_id.Portal.MIRROR_EXIT: td.GamemodePortalType,
    obj_id.Portal.BALL: td.GamemodePortalType,
    tid.EnterPreset.CHAOTIC: td.TriggerType,
    tid.EnterPreset.HALF_LEFT: td.TriggerType,
    tid.EnterPreset.HALF_RIGHT: td.TriggerType,
    tid.EnterPreset.HALF: td.TriggerType,
    tid.EnterPreset.HALF_INVERT: td.TriggerType,
    obj_id.Pad.BLUE: td.TriggerType,
    71: td.TriggerType,
    obj_id.Orb.BLUE: td.TriggerType,
    obj_id.Portal.SIZE_NORMAL: td.GamemodePortalType,
    obj_id.Portal.SIZE_SMALL: td.GamemodePortalType,
    obj_id.Portal.UFO: td.GamemodePortalType,
    obj_id.Pad.PINK: td.TriggerType,
    obj_id.Orb.PINK: td.TriggerType,
    162: td.EffectType,
    obj_id.Speed.SLOW: td.TriggerType,
    obj_id.Speed.NORMAL: td.TriggerType,
    obj_id.Speed.FAST: td.TriggerType,
    obj_id.Speed.VERY_FAST: td.TriggerType,
    205: td.ShaderType,
    obj_id.Portal.DUAL_ENTER: td.GamemodePortalType,
    obj_id.Portal.DUAL_EXIT: td.GamemodePortalType,
    obj_id.Portal.WAVE: td.GamemodePortalType,
    obj_id.Portal.ROBOT: td.GamemodePortalType,
    obj_id.Portal.Teleport.LINKED: td.PortalType,
    tid.COLOR: td.ColorType,
    tid.MOVE: td.MoveType,
    obj_id.TEXT: td.TextType,
    tid.PULSE: td.PulseType,
    tid.ALPHA: td.AlphaType,
    obj_id.Orb.GREEN: td.TriggerType,
    tid.TOGGLE: td.ToggleType,
    tid.SPAWN: td.SpawnType,
    cid.KEY: td.CollectibleType,
    cid.USER_COIN: td.AnimatedType,
    obj_id.Orb.BLACK: td.TriggerType,
    obj_id.Portal.SPIDER: td.GamemodePortalType,
    obj_id.Pad.RED: td.TriggerType,
    obj_id.Orb.RED: td.TriggerType,
    obj_id.Speed.SUPER_FAST: td.TriggerType,
    tid.ROTATE: td.RotateType,
    tid.FOLLOW: td.FollowType,
    1516: td.AnimatedType,
    tid.SHAKE: td.ShakeType,
    1582: td.SawType,
    1583: td.AnimatedType,
    tid.ANIMATE: td.AnimateType,
    1587: td.CollectibleType,
    1589: td.CollectibleType,
    obj_id.Orb.TOGGLE: td.ToggleBlockType,
    tid.TOUCH: td.TouchType,
    1598: td.CollectibleType,
    tid.COUNT: td.CountType,
    tid.PLAYER_HIDE: td.TriggerType,
    tid.PLAYER_SHOW: td.TriggerType,
    cid.SMALL_COIN: td.CollectibleType,
    obj_id.ITEM_LABEL: td.ItemLabelType,
    tid.STOP: td.StopType,
    1618: td.AnimatedType,
    obj_id.Orb.DASH_GREEN: td.DashType,
    obj_id.Orb.DASH_PINK: td.DashType,
    1752: td.SawType,
    obj_id.Modifier.WAVE_COLLISION: td.TriggerType,
    tid.INSTANT_COUNT: td.InstantCountType,
    tid.ON_DEATH: td.OnDeathType,
    obj_id.Modifier.STOP_JUMP: td.TriggerType,
    tid.FOLLOW_PLAYER_Y: td.FollowPlayerYType,
    tid.COLLISION: td.CollisionType,
    tid.COLLISION_BLOCK: td.CollisionBlockType,
    tid.PICKUP: td.PickupType,
    tid.BG_EFFECT_ENABLE: td.TriggerType,
    tid.BG_EFFECT_DISABLE: td.TriggerType,
    obj_id.Modifier.STOP_DASH: td.TriggerType,
    obj_id.Modifier.HEAD_COLLISION: td.TriggerType,
    1860: td.AnimatedType,
    tid.RANDOM: td.RandomType,
    tid.ZOOM_CAMERA: td.ZoomCameraType,
    tid.STATIC_CAMERA: td.StaticCameraType,
    tid.EnterPreset.NO_FADE: td.TriggerType,
    tid.OFFSET_CAMERA: td.OffsetCameraType,
    tid.REVERSE: td.TriggerType,
    tid.PLAYER_CONTROL: td.PlayerControlType,
    obj_id.Portal.SWING: td.GamemodePortalType,
    tid.SONG: td.SongType,
    tid.TIMEWARP: td.TimewarpType,
    tid.ROTATE_CAMERA: td.RotateCameraType,
    tid.CAMERA_GUIDE: td.CameraGuideType,
    tid.CAMERA_EDGE: td.CameraEdgeType,
    tid.CHECKPOINT: td.CheckpointType,
    obj_id.Portal.Teleport.EXIT: td.ExitPortalType,
    obj_id.PARTICLE_OBJECT: td.ParticleType,
    tid.GRAVITY: td.GravityType,
    tid.SCALE: td.ScaleType,
    tid.ADV_RANDOM: td.AdvRandomType,
    tid.FORCE_BLOCK: td.ForceBlockType,
    2605: td.AnimatedType,
    2694: td.AnimatedType,
    obj_id.Modifier.GRAVITY_FLIP: td.TriggerType,
    tid.OPTIONS: td.OptionsType,
    tid.ARROW: td.ArrowType,
    tid.GAMEPLAY_OFFSET: td.GameplayOffsetType,
    obj_id.Portal.Teleport.ENTER: td.PortalType,
    tid.GRADIENT: td.GradientType,
    tid.Shader.OPTIONS: td.ShaderType,
    tid.Shader.SHOCKWAVE: td.ShaderType,
    tid.Shader.SHOCKLINE: td.ShaderType,
    tid.Shader.GLITCH: td.ShaderType,
    tid.Shader.CHROMATIC: td.ShaderType,
    tid.Shader.CHROMATIC_GLITCH: td.ShaderType,
    tid.Shader.PIXELATE: td.ShaderType,
    tid.Shader.LENS_CIRCLE: td.ShaderType,
    tid.Shader.RADIAL_BLUR: td.ShaderType,
    tid.Shader.MOTION_BLUR: td.ShaderType,
    tid.Shader.BULGE: td.ShaderType,
    tid.Shader.PINCH: td.ShaderType,
    tid.Shader.GRAY_SCALE: td.ShaderType,
    tid.Shader.SEPIA: td.ShaderType,
    tid.Shader.INVERT_COLOR: td.ShaderType,
    tid.Shader.HUE: td.ShaderType,
    tid.Shader.EDIT_COLOR: td.ShaderType,
    tid.Shader.SPLIT_SCREEN: td.ShaderType,
    tid.CAMERA_MODE: td.CameraModeType,
    obj_id.Portal.GRAVITY_TOGGLE: td.GamemodePortalType,
    tid.EDIT_MG: td.MgEditType,
    obj_id.Orb.SPIDER: td.TriggerType,
    obj_id.Pad.SPIDER: td.TriggerType,
    tid.Area.MOVE: td.EffectType,
    tid.Area.ROTATE: td.EffectType,
    tid.Area.SCALE: td.EffectType,
    tid.Area.FADE: td.EffectType,
    tid.Area.TINT: td.EffectType,
    tid.Area.EDIT_MOVE: td.EffectType,
    tid.Area.EDIT_ROTATE: td.EffectType,
    tid.Area.EDIT_SCALE: td.EffectType,
    tid.Area.EDIT_FADE: td.EffectType,
    tid.Area.EDIT_TINT: td.EffectType,
    tid.ADV_FOLLOW: td.AdvFollowType,
    tid.Enter.MOVE: td.EffectType,
    tid.Enter.ROTATE: td.TriggerType,
    tid.Enter.SCALE: td.TriggerType,
    tid.Enter.FADE: td.TriggerType,
    tid.Enter.TINT: td.TriggerType,
    tid.TELEPORT: td.TeleportType,
    tid.Enter.STOP: td.TriggerType,
    tid.Area.STOP: td.EffectType,
    obj_id.Orb.TELEPORT: td.TriggerType,
    tid.CHANGE_BG: td.ChangeBgType,
    tid.CHANGE_GR: td.ChangeGrType,
    tid.CHANGE_MG: td.ChangeMgType,
    tid.KEYFRAME: td.KeyframeType,
    tid.ANIMATE_KEYFRAME: td.AnimateKeyframeType,
    3219: td.AnimatedType,
    tid.END: td.EndType,
    3601: td.CollectibleType,
    tid.SFX: td.SfxType,
    tid.EDIT_SFX: td.SfxType,
    tid.EVENT: td.EventType,
    tid.EDIT_SONG: td.SongType,
    tid.BG_SPEED: td.TriggerType,
    tid.SEQUENCE: td.SequenceType,
    tid.SPAWN_PARTICLE: td.SpawnParticleType,
    tid.INSTANT_COLLISION: td.InstantCollisionType,
    tid.MG_SPEED: td.MgSpeedType,
    tid.UI: td.UiType,
    tid.TIME: td.TimeType,
    tid.TIME_EVENT: td.TimeEventType,
    tid.TIME_CONTROL: td.TimeControlType,
    tid.RESET: td.ResetType,
    tid.ITEM_EDIT: td.ItemEditType,
    tid.ITEM_COMPARE: td.ItemCompareType,
    tid.STATE_BLOCK: td.StateBlockType,
    tid.ITEM_PERSIST: td.ItemPersistType,
    tid.BPM: td.BpmType,
    tid.TOGGLE_BLOCK: td.ToggleBlockType,
    tid.FORCE_CIRCLE: td.ForceBlockType,
    tid.EDIT_ADV_FOLLOW: td.EditAdvFollowType,
    tid.RETARGET_ADV_FOLLOW: td.EditAdvFollowType,
    tid.LINK_VISIBLE: td.LinkVisibleType,
    4211: td.AnimatedType,
    4300: td.AnimatedType,
}
"""Unfinished mapping of Object IDs to non-common Object TypedDicts"""


def _assign_id_types(cls: range, obj_type: type[ObjectType]):
    for c in cls: ID_TO_TYPEDDICT[c] = obj_type

_assign_id_types(range(85, 89 + 1), td.SawType)
_assign_id_types(range(97, 98 + 1), td.SawType)
_assign_id_types(range(137, 139 + 1), td.SawType)
_assign_id_types(range(154, 156 + 1), td.SawType)
_assign_id_types(range(180, 188 + 1), td.SawType)
_assign_id_types(range(222, 224 + 1), td.SawType)
_assign_id_types(range(375, 378 + 1), td.SawType)
_assign_id_types(range(394, 399 + 1), td.SawType)
_assign_id_types(range(678, 680 + 1), td.SawType)
_assign_id_types(range(740, 742 + 1), td.SawType)
_assign_id_types(range(920, 924 + 1), td.AnimatedType)
_assign_id_types(range(997, 1000 + 1), td.SawType)
_assign_id_types(range(1019, 1021 + 1), td.SawType)
_assign_id_types(range(1050, 1054 + 1), td.AnimatedType)
_assign_id_types(range(1055, 1061 + 1), td.SawType)
_assign_id_types(range(1518, 1519 + 1), td.AnimatedType)
_assign_id_types(range(1521, 1528 + 1), td.SawType)
_assign_id_types(range(1591, 1593 + 1), td.AnimatedType)
_assign_id_types(range(1619, 1620 + 1), td.SawType)
_assign_id_types(range(1697, 1699 + 1), td.AnimatedType)
_assign_id_types(range(1705, 1710 + 1), td.SawType)
_assign_id_types(range(1734, 1736 + 1), td.SawType)
_assign_id_types(range(1831, 1834 + 1), td.SawType)
_assign_id_types(range(1839, 1842 + 1), td.AnimatedType)
_assign_id_types(range(1849, 1858 + 1), td.AnimatedType)
_assign_id_types(range(1936, 1939 + 1), td.AnimatedType)
_assign_id_types(range(2020, 2055 + 1), td.AnimatedType)
_assign_id_types(range(2629, 2630 + 1), td.AnimatedType)
_assign_id_types(range(2864, 2865 + 1), td.AnimatedType)
_assign_id_types(range(2867, 2894 + 1), td.AnimatedType)
_assign_id_types(range(2895, 2897 + 1), td.TemplateType)
_assign_id_types(range(3000, 3002 + 1), td.AnimatedType)
_assign_id_types(range(3119, 3121 + 1), td.AnimatedType)
_assign_id_types(range(3303, 3304 + 1), td.AnimatedType)
_assign_id_types(range(3482, 3484 + 1), td.AnimatedType)
_assign_id_types(range(3492, 3493 + 1), td.AnimatedType)
_assign_id_types(range(4401, 4539 + 1), td.CollectibleType)


ID_TO_ALLOWED_KEYS = {
    k: set(v.__required_keys__) | set(v.__optional_keys__) 
    for k, v in ID_TO_TYPEDDICT.items()
}

COMMON_ALLOWED_KEYS = td.ObjectType.__required_keys__ | td.ObjectType.__optional_keys__

TARGET_GROUP_FIELDS = { "a51", "a71", "a401", "a395", "a76" }
"""All fields are hashable"""

TARGETS_SOLID_GROUPS = {
    tid.MOVE,
    tid.ROTATE,
    tid.FOLLOW,
    tid.ADV_FOLLOW,
    tid.ANIMATE,
    tid.ANIMATE_KEYFRAME,
    tid.KEYFRAME,
    tid.PULSE,
    tid.Area.MOVE,
    tid.Area.ROTATE,
    tid.Area.SCALE,
    tid.Area.FADE,
    tid.Area.TINT,
    tid.Area.EDIT_MOVE,
    tid.Area.EDIT_ROTATE,
    tid.Area.EDIT_SCALE,
    tid.Area.EDIT_FADE,
    tid.Area.EDIT_TINT,
}
"""All triggers that primarily target solid objects, not other triggers"""

UNHASHABLE_VALUE_KEYS = {
    obj_prop.GROUPS,
    obj_prop.PARENT_GROUPS,
    obj_prop.Trigger.Spawn.REMAPS,
    obj_prop.Trigger.AdvRandom.TARGETS,
    obj_prop.Trigger.Event.EVENTS,
    obj_prop.Trigger.Sequence.SEQUENCE
}


def is_group_id(object_id: int, key: str, id: int) -> bool:
    match object_id:
        case obj_id.Trigger.PULSE:
            if key == obj_prop.Trigger.Pulse.TARGET_ID:
                return 1 <= id <= 999 or 1015 <= id <= 9999
        case _:
            pass
    return 1 <= id <= 9999


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
