"""Level loading and exporting for Geometry Dash."""

from pathlib import Path
import time
from typing import Any, Callable, Iterator, SupportsIndex, cast
from questionary import confirm
from gmdkit.models.level import Level as KitLevel
from gmdkit.models.object import ObjectList as KitObjectList
from gmdkit.extra.live_editor import WEBSOCKET_URL, LiveEditor

from gmdbuilder.core import Object, to_kit_object, from_kit_object
from gmdbuilder.mappings import obj_prop
from gmdbuilder.validation import validate_obj
from gmdbuilder.object_types import ObjectType



ObjectPatternMatch = dict[str, Any] | ObjectType | Callable[[ObjectType], bool]

class ObjectList(list[ObjectType]):
    """
    A list that validates ObjectType mutations.
    Only additions are allowed in live editor mode
    
    - append/insert/extend: wraps objects in ValidatedObject for runtime validation
    - Direct indexing (objects[i]): read-only access
    - Property edits (objects[i]['a2'] = x): validated by ValidatedObject.__setitem__
    - Addition operators (+, +=): disabled - use extend() instead
    """
    _MISSING = object()
    
    def __init__(self, *, live_editor: bool):
        super().__init__()
        self._live_editor_mode = live_editor
        self.added_objects: list[ObjectType] = []
    
    def delete_where(self, condition: ObjectPatternMatch, *, limit: int = -1) -> int:
        """
        Delete objects matching a condition (dict or predicate)
        
        Returns number of deleted objects.
        
        For dict-matching, dict must match standard ObjectType keys/values.
        'None' can be used as a wildcard value (not key).
        """
        if self._live_editor_mode:
            raise RuntimeError("Direct object deleting is not allowed in live editor mode")
        if limit < -1 or limit == 0:
            raise ValueError("delete_where limit must be -1 (no limit) or positive")
        
        predicate: Callable[[ObjectType], bool]
        if callable(condition):
            predicate = condition
        else:
            predicate = lambda obj: all(obj.get(k, self._MISSING) == v for k, v in condition.items())
        
        deleted = 0
        
        for i in range(len(self) - 1, -1, -1):
            if predicate(self[i]):
                del self[i]
                deleted += 1
                if limit != -1 and deleted >= limit:
                    break
        
        return deleted
    
    @staticmethod
    def _wrap_object(obj: ObjectType) -> ObjectType:
        """Wrap an object in ValidatedObject for runtime validation."""
        if isinstance(obj, Object):
            return cast(ObjectType, obj)
        validate_obj(obj)
        wrapped = Object(obj[obj_prop.ID])
        wrapped.update(obj)
        return cast(ObjectType, wrapped)
    
    def __setitem__(self, # type: ignore[override]
        index: SupportsIndex | slice, 
        value: ObjectType | list[ObjectType]):
        """Validate when setting an item by index."""
        if self._live_editor_mode:
            raise RuntimeError("Direct object editing is not supported in live editor mode")
        if isinstance(index, slice):
            if not isinstance(value, list):
                raise TypeError(f"can only assign a list (not {type(value).__name__}) to a slice")
            validated = [self._wrap_object(obj) for obj in value]
            super().__setitem__(index, validated)
        else:
            if not isinstance(value, dict):
                raise TypeError(f"can only assign ObjectType dict (not {type(value).__name__})")
            validated = self._wrap_object(value)
            super().__setitem__(index, validated)
    
    def append(self, obj: ObjectType, *, import_mode_backend_only: bool = False):
        """Validate and append an object."""
        if import_mode_backend_only:
            super().append(obj)
        else:
            obj = self._wrap_object(obj)
            super().append(obj)
            self.added_objects.append(obj)
    
    def insert(self, index: SupportsIndex, obj: ObjectType):
        """Validate and insert an object at index."""
        if self._live_editor_mode:
            raise RuntimeError("Direct item editing is not allowed in live editor mode")
        wrapped = self._wrap_object(obj)
        super().insert(index, wrapped)
        self.added_objects.append(wrapped)
    
    def extend(self, iterable: list[ObjectType]):  # type: ignore[override]
        """Validate and extend with multiple objects."""
        validated = [self._wrap_object(obj) for obj in iterable]
        super().extend(validated)
        self.added_objects.extend(validated)
    
    def __add__(self, other: object) -> "ObjectList":
        """Disabled: use extend() instead."""
        raise NotImplementedError("Use .extend() instead of + operator")
    
    def __iadd__(self, other: object) -> "ObjectList": 
        """Disabled: use extend() instead."""
        raise NotImplementedError("Use .extend() instead of += operator")


objects = ObjectList(live_editor=False)
"""List of level's objects."""

tag_group = 9999
"""Deletes all objects with this group and adds this group to new added objects"""

_kit_level: KitLevel | None = None
_source_file: Path | None = None
_live_editor: LiveEditor | None = None
# _start_time: float | None = None


def _time_since_last(_state:list[float]=[time.perf_counter()]) -> float:
    now = time.perf_counter()
    a = _state[0]
    _state[0] = now
    return now - a


def from_file(file_path: str | Path) -> None:
    """Load level from .gmd file into the module-level objects list."""
    global objects, tag_group, _kit_level, _source_file, _live_editor, _start_time
    
    if _source_file is not None or _live_editor is not None:
        raise RuntimeError("FORBIDDEN: Level file is loaded! Loading multiple levels at once overrides global state")
    
    _time_since_last()
    
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Level file not found: {file_path=}")
    
    _kit_level = KitLevel.from_file(path)
    _source_file = path
    objects = ObjectList(live_editor=False)
    
    for kit_obj in _kit_level.objects:
        obj = from_kit_object(kit_obj)
        if tag_group not in obj.get(obj_prop.GROUPS, set()):
            objects.append(obj, import_mode_backend_only=True)
    
    print(f"Loaded level from {file_path} with {len(objects)} objects in {_time_since_last():.2f} seconds.")


def from_live_editor(url: str = WEBSOCKET_URL) -> None:
    global objects, tag_group, _kit_level, _live_editor, _source_file
    
    if _source_file is not None or _live_editor is not None:
        raise RuntimeError("FORBIDDEN: Level file is loaded! Loading multiple levels at once overrides global state")
    
    objects = ObjectList(live_editor=True)
    _live_editor = LiveEditor(url)
    _live_editor.connect()
    _live_editor.remove_object_group(tag_group)
    _, kit_objects = _live_editor.get_level_string()
    
    for kit_obj in kit_objects:
        obj = from_kit_object(kit_obj)
        if tag_group not in obj.get(obj_prop.GROUPS, set()):
            objects.append(obj, import_mode_backend_only=True)


class new():
    """Return the next free ID for group, item, color, collision, control IDs."""
    _initialized = False
    _group_iter: Iterator[int] | None = None
    _item_iter: Iterator[int] | None = None
    _color_iter: Iterator[int] | None = None
    _collision_iter: Iterator[int] | None = None
    _control_iter: Iterator[int] | None = None
    
    @classmethod
    def _register_free_ids(cls):
        cls._initialized = True
        global objects
        
        cls._used_group_ids: set[int] = set()
        cls._used_item_ids: set[int] = set()
        cls._used_color_ids: set[int] = set()
        cls._used_collision_ids: set[int] = set()
        cls._used_control_ids: set[int] = set()
        
        for obj in objects:
            if (key := obj_prop.GROUPS) in obj:
                cls._used_group_ids.update(obj[key])
            if (key := obj_prop.Trigger.Count.ITEM_ID) in obj:
                cls._used_item_ids.add(int(obj[key]))
            if (key := obj_prop.Trigger.CollisionBlock.BLOCK_ID) in obj:
                cls._used_collision_ids.add(int(obj[key]))
            if (key := obj_prop.Trigger.CONTROL_ID) in obj:
                cls._used_control_ids.add(int(obj[key]))
        
        cls._group_iter = (i for i in range(1, 9999) if i not in cls._used_group_ids)
        cls._item_iter = (i for i in range(1, 9999) if i not in cls._used_item_ids)
        # cls._color_iter = (i for i in range(1, 9999) if i not in cls._used_color_ids)
        cls._collision_iter = (i for i in range(1, 9999) if i not in cls._used_collision_ids)
        cls._control_iter = (i for i in range(1, 9999) if i not in cls._used_control_ids)
    
    
    @classmethod
    def _get_next(cls, iterator: Iterator[int] | None, id_type: str) -> int:
        if not cls._initialized:
            cls._register_free_ids()
        if iterator is None:
            raise RuntimeError(f"Iterator for {id_type} IDs is not initialized")
        try:
            return next(iterator)
        except StopIteration:
            raise RuntimeError(f"No free {id_type} IDs available")
    
    @classmethod
    def group(cls) -> int:
        """Get next free group ID (1-9999)."""
        return cls._get_next(cls._group_iter, "group")
    
    @classmethod
    def item(cls) -> int:
        """Get next free item ID (1-9999)."""
        return cls._get_next(cls._item_iter, "item")
    
    @classmethod
    def color(cls) -> int:
        """Get next free color ID (1-9999)."""
        return cls._get_next(cls._color_iter, "color")
    
    @classmethod
    def collision(cls) -> int:
        """Get next free collision block ID (1-9999)."""
        return cls._get_next(cls._collision_iter, "collision")
    
    @classmethod
    def control(cls) -> int:
        """Get next free control ID (1-9999)."""
        return cls._get_next(cls._control_iter, "control")
    
    @classmethod
    def group_multi(cls, count: int) -> tuple[int,...]:
        """Get next free group IDs (1-9999)."""
        return tuple(cls._get_next(cls._group_iter, "group") for _ in range(count))
    
    @classmethod
    def item_multi(cls, count: int) -> tuple[int,...]:
        """Get next free item IDs (1-9999)."""
        return tuple(cls._get_next(cls._item_iter, "item") for _ in range(count))
    
    @classmethod
    def color_multi(cls, count: int) -> tuple[int,...]:
        """Get next free color IDs (1-9999)."""
        return tuple(cls._get_next(cls._color_iter, "color") for _ in range(count))
    
    @classmethod
    def collision_multi(cls, count: int) -> tuple[int,...]:
        """Get next free collision block IDs (1-9999)."""
        return tuple(cls._get_next(cls._collision_iter, "collision") for _ in range(count))
    
    @classmethod
    def control_multi(cls, count: int) -> tuple[int,...]:
        """Get next free control IDs (1-9999)."""
        return tuple(cls._get_next(cls._control_iter, "control") for _ in range(count))
    
    @classmethod
    def reset_all(cls):
        """Reset and rescan level objects. Call after significant object changes."""
        cls._initialized = False
        cls._group_iter = None
        cls._item_iter = None
        cls._color_iter = None
        cls._collision_iter = None
        cls._control_iter = None



def _validate_and_prepare_objects(validated_objects: ObjectList) -> None:
    """Run validation and preparation checks on objects before export."""
    
    for obj in validated_objects.added_objects:
        groups = obj.get(obj_prop.GROUPS, set())
        groups.add(tag_group)
        obj[obj_prop.GROUPS] = groups


def export_to_file(file_path: str | Path | None = None) -> None:
    """Export level to .gmd file."""
    global objects, _kit_level, _source_file, _start_time
    
    print(f"gmdbuilder took {_time_since_last():.2f} seconds to prepare for export.")
    
    if _kit_level is None:
        raise RuntimeError("No level loaded. Use level.from_file() first")
    
    # Determine export path
    if file_path is None:
        if _source_file is None:
            raise RuntimeError("No export path available. Provide file_path argument")
        
        if confirm("Overwrite the source file?", default=False).ask() is False:
            raise RuntimeError("Export cancelled by user")
        export_path = _source_file
    else:
        export_path = Path(file_path)
    
    _validate_and_prepare_objects(objects)
    
    kit_objects = _kit_level.objects
    kit_objects.clear()
    kit_objects.extend(to_kit_object(obj) for obj in objects)
    
    _kit_level.to_file(str(export_path))
    
    print(f"Exported level to {export_path} with {len(objects)} objects in {_time_since_last():.2f} seconds.")
    
    new.reset_all()
    objects.clear()


def export_to_live_editor(*, batch_size: int = 500) -> None:
    """Export level to live editor."""
    global objects, _live_editor
    
    if _live_editor is None:
        raise RuntimeError("No live editor connection. Use level.from_live_editor() first")
    
    _validate_and_prepare_objects(objects)
    
    # Convert to gmdkit ObjectList
    kit_objects = KitObjectList()
    kit_objects.extend(to_kit_object(obj) for obj in objects.added_objects)
    
    _live_editor.add_objects(kit_objects, batch_size)
    _live_editor.close()
    new.reset_all()
    objects.clear()
    _live_editor = None