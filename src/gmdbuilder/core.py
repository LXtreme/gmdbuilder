"""Core utilities for working with ObjectType dicts."""

from functools import lru_cache
from typing import Any, TypeGuard, TypeVar, cast

from gmdkit.models.object import Object as KitObject
from gmdkit.models.prop.list import IDList, RemapList

import gmdbuilder.object_types as td
from gmdbuilder.fields import ID_TO_TYPEDDICT
from gmdbuilder.mappings import obj_prop
from gmdbuilder.validation import validate

ObjectType = td.ObjectType

T = TypeVar('T', bound=ObjectType)

def is_obj_type(obj: ObjectType, obj_type: type[T]) -> TypeGuard[T]:
    """Type-narrows obj to a specific TypedDict type by matching its ID."""
    return ID_TO_TYPEDDICT.get(obj.get(obj_prop.ID)) is obj_type


def is_obj_id(obj: ObjectType, object_id: int) -> bool:
    """This basically casts obj to specific ObjectType subclass via type guard"""
    return obj.get(obj_prop.ID) == object_id


class Object(dict[str, Any]):
    __slots__ = ("_obj_id",)

    def __init__(self, obj_id: int):
        super().__init__()
        self._obj_id = int(obj_id)
        super().__setitem__(obj_prop.ID, self._obj_id)

    def __setitem__(self, k: str, v: Any):
        if k == obj_prop.ID:
            raise KeyError("Cannot change object ID after initialization")
        validate(k, v, self)
        super().__setitem__(k, v)

    def update(self, *args: Any, **kwargs: Any):
        # Construct items dict from args and kwargs
        items: dict[str, Any]
        if args:
            if len(args) != 1:
                raise TypeError(f"update() takes at most 1 positional argument ({len(args)} given)")
            __m = args[0]
            items = dict(__m)
            items.update(kwargs)
        else:
            items = dict(kwargs)
        
        if obj_prop.ID in items:
            raise KeyError("Cannot change object ID after initialization")
        for k, v in items.items():
            validate(k, v, self)
        super().update(items)
    
    @staticmethod
    def wrap_object(obj: "ObjectType | Object") -> ObjectType:
        """Wrap an object in ValidatedObject for runtime validation."""
        if isinstance(obj, Object):
            return cast(ObjectType, obj)
        wrapped = Object(obj[obj_prop.ID])
        wrapped.update(obj)
        return cast(ObjectType, wrapped)



@lru_cache(maxsize=1024)
def _to_raw_key_cached(key: str) -> int | str:
    if key.startswith('k'):
        return key
    if key.startswith('a'):
        tail = key[1:]
        if tail.isdigit():
            return int(tail)
    raise ValueError()

def to_kit_object(obj: ObjectType) -> KitObject:
    raw: dict[int|str, Any] = {}
    for k, v in obj.items():
        match k:
            case obj_prop.GROUPS | obj_prop.PARENT_GROUPS:
                raw[_to_raw_key_cached(k)] = IDList(v)
            case obj_prop.Trigger.Spawn.REMAPS:
                raw[_to_raw_key_cached(k)] = RemapList.from_dict(v) # type: ignore
            case _:
                try:
                    raw[_to_raw_key_cached(k)] = v
                except ValueError as e:
                    raise ValueError(f"Object has bad/unsupported key {k!r}:\n{obj=}") from e
    return KitObject(raw)


@lru_cache(maxsize=1024)
def _from_raw_key_cached(key: int|str) -> str:
    if isinstance(key, int):
        return f"a{key}"
    if key.startswith("a") or key.startswith("k"):
        return key
    raise ValueError("Unrecognized key format")


def from_kit_object(obj: dict[int|str, Any]) -> ObjectType:
    new = Object(obj[1])
    for k, v in obj.items():
        match k:
            case 1: pass
            case 57:
                new[obj_prop.GROUPS] = set(v) if v else set()
            case 274:
                new[obj_prop.PARENT_GROUPS] = set(v) if v else set()
            case 442:
                new[obj_prop.Trigger.Spawn.REMAPS] = v.to_dict()
            case 52:
                new[obj_prop.Trigger.Pulse.TARGET_TYPE] = bool(v)
            # case 152:
                # new[obj_prop.Trigger.AdvRandom.TARGETS] = [(i.key, i.value) for i in v]
            case _:
                try:
                    raw_key = _from_raw_key_cached(k)
                except ValueError:
                    raise TypeError(f"Object has unsupported key {k=}. Found {k=}:{v=} :: \n{obj=}")
                new[raw_key] = v
    return cast(ObjectType, new)


def from_object_string(obj_string: str, obj_type: type = ObjectType) -> ObjectType:
    return from_kit_object(KitObject.from_string(obj_string)) # type: ignore


def new_obj(object_id: int) -> ObjectType:
    # Convert from gmdkit's {1: val, 2: val} to our {'a1': val, 'a2': val}
    return from_kit_object(KitObject.default(object_id)) # type: ignore
