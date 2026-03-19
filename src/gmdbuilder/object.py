
from typing import Any, Callable, Iterable, SupportsIndex, cast

from .mappings import obj_prop
from .object_types import ObjectType
from .validation import validate


class ValidatedObject(dict[str, Any]):
    """
    A dict subclass that represents a level object with validation on property edits.
    
    Is automatically wrapped around objects added to the level's ObjectList, so users can interact with objects as dicts while still getting validation.
    """
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
        
        for k, v in items.items():
            if k == obj_prop.ID:
                raise KeyError("Cannot change object ID after initialization")
            validate(k, v, self)
        super().update(items)
    
    @staticmethod
    def wrap_object(obj: "ObjectType | ValidatedObject") -> ObjectType:
        """Wrap an object in ValidatedObject for runtime validation."""
        if isinstance(obj, ValidatedObject):
            return cast(ObjectType, obj)
        wrapped = ValidatedObject(obj[obj_prop.ID])
        wrapped.update(obj)
        return cast(ObjectType, wrapped)



ObjectPatternMatch = dict[str, Any] | ObjectType | Callable[[ObjectType], bool]

class ObjectList(list[ObjectType]):
    """
    A list that validates ObjectType mutations.
    
    - append/extend: adds tag_group
    - Property edits (objects[i]['a2'] = x): validated by ValidatedObject.__setitem__
    """
    
    def __init__(self, *, tag_group: int = 9999):
        super().__init__()
        self.tag_group: int = tag_group
    
    def delete_where(self, condition: ObjectPatternMatch, *, limit: int = -1) -> int:
        """
        Delete objects matching a condition (dict or predicate)
        
        For dict-matching, dict must match standard ObjectType keys/values.
        'None' can be used as a wildcard value (not key).
        
        Returns number of deleted objects.
        """
        if limit < -1 or limit == 0:
            raise ValueError("delete_where limit must be -1 (no limit) or positive")
        
        predicate: Callable[[ObjectType], bool]
        if callable(condition):
            predicate = condition
        else:
            predicate = lambda obj: all(
                k in obj and (obj.get(k) == v or v is None)
                for k, v in condition.items()
            )
        
        deleted = 0
        
        for i in range(len(self) - 1, -1, -1):
            if predicate(self[i]):
                del self[i]
                deleted += 1
                if limit != -1 and deleted >= limit:
                    break
        
        return deleted
    
    def __setitem__(self, # type: ignore[override]
        index: SupportsIndex | slice, 
        value: ObjectType | list[ObjectType]):
        """Validate when setting an item by index."""
        if isinstance(index, slice):
            if not isinstance(value, list):
                raise TypeError(f"can only assign a list (not {type(value).__name__}) to a slice")
            validated = [ValidatedObject.wrap_object(obj) for obj in value]
            super().__setitem__(index, validated)
        else:
            if not isinstance(value, dict):
                raise TypeError(f"can only assign ObjectType dict (not {type(value).__name__})")
            validated = ValidatedObject.wrap_object(value)
            super().__setitem__(index, validated)
    
    def append(self, obj: ObjectType):
        """Validate and append an object."""
        obj = ValidatedObject.wrap_object(obj)
        
        groups = set(obj.get(obj_prop.GROUPS, set()))
        groups.add(self.tag_group)
        obj[obj_prop.GROUPS] = groups
        
        super().append(obj)
    
    def insert(self, index: SupportsIndex, obj: ObjectType):
        """Validate and insert an object at index."""
        obj = ValidatedObject.wrap_object(obj)
        
        groups = set(obj.get(obj_prop.GROUPS, set()))
        groups.add(self.tag_group)
        obj[obj_prop.GROUPS] = groups
        
        super().insert(index, obj)
    
    def extend(self, iterable: Iterable[ObjectType]):
        """Validate and extend with multiple objects."""
        for obj in iterable:
            self.append(obj)
    
    def __add__(self, other: object) -> "ObjectList":
        """Disabled: use extend() instead."""
        raise TypeError("Use .extend() instead of + operator")
    
    def __iadd__(self, other: object) -> "ObjectList": 
        """Disabled: use extend() instead."""
        raise TypeError("Use .extend() instead of += operator")