"""Level loading and exporting for Geometry Dash."""

from collections import deque
from pathlib import Path
import time
from typing import Any, Callable, Iterable, Literal, SupportsIndex, cast, overload
from questionary import confirm
from gmdkit.models.level import Level as KitLevel
from gmdkit.models.object import ObjectList as KitObjectList
from gmdkit.extra.live_editor import WEBSOCKET_URL, LiveEditor
from gmdkit.serialization.functions import compress_string

from gmdbuilder.core import Object, to_kit_object, from_kit_object
from gmdbuilder.mappings import obj_prop
from gmdbuilder.validation import validate
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
    
    @staticmethod
    def _wrap_object(obj: ObjectType) -> ObjectType:
        """Wrap an object in ValidatedObject for runtime validation."""
        if isinstance(obj, Object):
            return cast(ObjectType, obj)
        for k, v in obj.items():
            validate(obj[obj_prop.ID], k, v)
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
        obj = self._wrap_object(obj)
        if not import_mode_backend_only:
            self.added_objects.append(obj)
        super().append(obj)
    
    def insert(self, index: SupportsIndex, obj: ObjectType):
        """Validate and insert an object at index."""
        if self._live_editor_mode:
            raise RuntimeError("Direct item editing is not allowed in live editor mode")
        wrapped = self._wrap_object(obj)
        super().insert(index, wrapped)
        self.added_objects.append(wrapped)
    
    def extend(self, iterable: Iterable[ObjectType]):
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


def _time_since_last(_state:list[float]=[time.perf_counter()]) -> float:
    now = time.perf_counter()
    a = _state[0]
    _state[0] = now
    return now - a


def from_file(file_path: str | Path) -> None:
    """Load level from .gmd file into the module-level objects list."""
    global objects, tag_group, _kit_level, _source_file, _live_editor
    
    if _source_file is not None or _live_editor is not None:
        raise RuntimeError("FORBIDDEN: Level file is loaded! Loading multiple levels at once overrides global state")
    
    _time_since_last()
    
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Level file not found: {file_path=}")
    
    _kit_level = KitLevel.from_file(path)
    _source_file = path
    objects = ObjectList(live_editor=False)
    
    obj_count = len(_kit_level.objects)
    
    for kit_obj in _kit_level.objects:
        obj = from_kit_object(kit_obj)
        if tag_group not in obj.get(obj_prop.GROUPS, set()):
            objects.append(obj, import_mode_backend_only=True)
    
    print(f"\nLoaded '{file_path}' with {obj_count} objects in {_time_since_last():.3f} seconds.")
    print(f"\nRemoved {obj_count-len(objects)} objects with tag group {tag_group}, level is now {len(objects)} objects.")


def from_live_editor(url: str = WEBSOCKET_URL) -> None:
    global objects, tag_group, _kit_level, _live_editor, _source_file
    
    if _source_file is not None or _live_editor is not None:
        raise RuntimeError("FORBIDDEN: Level file is loaded! Loading multiple levels at once overrides global state")
    
    _time_since_last()
    
    objects = ObjectList(live_editor=True)
    _live_editor = LiveEditor(url)
    _live_editor.connect()
    _live_editor.remove_objects(tag_group)
    _, kit_objects = _live_editor.get_level()
    
    obj_count = len(kit_objects)
    
    for kit_obj in kit_objects:
        obj = from_kit_object(kit_obj)
        if tag_group not in obj.get(obj_prop.GROUPS, set()):
            objects.append(obj, import_mode_backend_only=True)
    
    print(f"\nLoaded level with {obj_count} objects in {_time_since_last():.3f} seconds.")
    print(f"\nRemoved {obj_count-len(objects)} objects with tag group {tag_group}, level is now {len(objects)} objects.")
    

class IDAllocator:
    """Singleton class to manage unique ID allocation. Instance is 'new'."""
    
    def __init__(self):
        self._initialized = False
        
        self._group_pool: deque[int] = deque()
        self._item_pool: deque[int] = deque()
        self._color_pool: deque[int] = deque()
        self._collision_pool: deque[int] = deque()
        self._control_pool: deque[int] = deque()
        
        self.used_group_ids: set[int] = set()
        self.used_item_ids: set[int] = set()
        self.used_color_ids: set[int] = set()
        self.used_collision_ids: set[int] = set()
        self.used_control_ids: set[int] = set()
    
    def reserve_id(self, id_type: str, id_value: int):
        """Manually reserve an ID (e.g. for objects not in the main list)."""
        if id_type == "group":
            self.used_group_ids.add(id_value)
        elif id_type == "item":
            self.used_item_ids.add(id_value)
        elif id_type == "color":
            self.used_color_ids.add(id_value)
        elif id_type == "collision":
            self.used_collision_ids.add(id_value)
        elif id_type == "control":
            self.used_control_ids.add(id_value)
        else:
            raise ValueError(f"Unknown ID type: {id_type}")
    
    def _register_free_ids(self):
        """Runs automatically at first new ID call."""
        self._initialized = True
        global objects
        
        if len(objects) == 0:
            raise RuntimeError("Objects not found. Load a level first with from_file() or from_live_editor()")
        
        for obj in objects:
            if (key := obj_prop.GROUPS) in obj:
                self.used_group_ids.update(obj[key])
            if (key := obj_prop.Trigger.Count.ITEM_ID) in obj:
                self.used_item_ids.add(obj[key])
            if (key := obj_prop.Trigger.CollisionBlock.BLOCK_ID) in obj:
                self.used_collision_ids.add(obj[key])
            if (key := obj_prop.Trigger.CONTROL_ID) in obj:
                self.used_control_ids.add(obj[key])
        
        # Build sorted deques of available IDs using set difference (O(n) but very fast)
        all_ids = set(range(1, 9999))
        self._group_pool = deque(sorted(all_ids - self.used_group_ids))
        self._item_pool = deque(sorted(all_ids - self.used_item_ids))
        self._color_pool = deque(sorted(all_ids - self.used_color_ids))
        self._collision_pool = deque(sorted(all_ids - self.used_collision_ids))
        self._control_pool = deque(sorted(all_ids - self.used_control_ids))
    
    def _get_next(self, pool_name: str) -> int:
        """Get next free ID from pool. O(1) operation."""
        if not self._initialized:
            self._register_free_ids()
        
        pool = getattr(self, f"_{pool_name}_pool")        
        if not pool:
            raise RuntimeError(f"No free {pool_name} IDs available (1-9999 range exhausted)")
        
        used_set = getattr(self, f"used_{pool_name}_ids")
        next_id = pool.popleft()
        used_set.add(next_id)
        return next_id
    
    @overload
    def group(self) -> int: ...
    @overload
    def group(self, count: Literal[1]) -> int: ... # type: ignore[override]
    @overload
    def group(self, count: Literal[2]) -> tuple[int, int]: ...
    @overload
    def group(self, count: int) -> tuple[int, ...]: ...
    def group(self, count: int = 1) -> tuple[int,...] | int:
        """Get next free group ID (1-9999)."""
        if count == 1:
            return self._get_next("group")
        return tuple(self._get_next("group") for _ in range(count))
    
    @overload
    def item(self) -> int: ...
    @overload
    def item(self, count: Literal[1]) -> int: ... # type: ignore[override]
    @overload
    def item(self, count: Literal[2]) -> tuple[int, int]: ...
    @overload
    def item(self, count: int) -> tuple[int, ...]: ...
    def item(self, count: int = 1) -> tuple[int,...] | int:
        """Get next free item ID (1-9999)."""
        if count == 1:
            return self._get_next("item")
        return tuple(self._get_next("item") for _ in range(count))
    
    @overload
    def color(self) -> int: ...
    @overload
    def color(self, count: Literal[1]) -> int: ... # type: ignore[override]
    @overload
    def color(self, count: Literal[2]) -> tuple[int, int]: ...
    @overload
    def color(self, count: int) -> tuple[int, ...]: ...
    def color(self, count: int = 1) -> tuple[int,...] | int:
        """Get next free color ID (1-9999)."""
        if count == 1:
            return self._get_next("color")
        return tuple(self._get_next("color") for _ in range(count))
    
    @overload
    def collision(self) -> int: ...
    @overload
    def collision(self, count: Literal[1]) -> int: ... # type: ignore[override]
    @overload
    def collision(self, count: Literal[2]) -> tuple[int, int]: ...
    @overload
    def collision(self, count: int) -> tuple[int, ...]: ...
    def collision(self, count: int = 1) -> tuple[int,...] | int:
        """Get next free collision block ID (1-9999)."""
        if count == 1:
            return self._get_next("collision")
        return tuple(self._get_next("collision") for _ in range(count))
    
    @overload
    def control(self) -> int: ...
    @overload
    def control(self, count: Literal[1]) -> int: ... # type: ignore[override]
    @overload
    def control(self, count: Literal[2]) -> tuple[int, int]: ...
    @overload
    def control(self, count: int) -> tuple[int, ...]: ...
    def control(self, count: int = 1) -> tuple[int,...] | int:
        """Get next free control ID (1-9999)."""
        if count == 1:
            return self._get_next("control")
        return tuple(self._get_next("control") for _ in range(count))
    
    def reset_all(self):
        self._initialized = False
        self._group_pool.clear()
        self._item_pool.clear()
        self._color_pool.clear()
        self._collision_pool.clear()
        self._control_pool.clear()
        self.used_group_ids.clear()
        self.used_item_ids.clear()
        self.used_color_ids.clear()
        self.used_collision_ids.clear()
        self.used_control_ids.clear()

new = IDAllocator()
"""Allocate free IDs for level objects."""

def _validate_and_prepare_objects(validated_objects: ObjectList) -> None:
    """Run validation and preparation checks on objects before export."""
    global tag_group
    for obj in validated_objects.added_objects:
        groups = obj.get(obj_prop.GROUPS, {tag_group})
        groups.add(tag_group)
        obj[obj_prop.GROUPS] = groups


def export_to_file(file_path: str | Path | None = None) -> None:
    """Export level to .gmd file."""
    global objects, _kit_level, _source_file
    
    print(f"\ngmdbuilder took {_time_since_last():.4f} seconds to prepare for export.")
    
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

    # gmdkit bug workaround: ObjectList.to_string() joins items with ";" but each
    # Object already ends with ";" (END_DELIMITER), producing double ";;" in the
    # output. Passing keep_sep=True makes it use "" as the separator instead,
    # giving the correct single-semicolon GD format. We pre-build the compressed
    # string and bypass ObjectString.save() (save=False) so it isn't overwritten.
    obj_str_handler = _kit_level['k4']
    correct_string = obj_str_handler.start.to_string() + kit_objects.to_string(keep_sep=True)
    obj_str_handler.string = compress_string(correct_string)

    _kit_level.to_file(str(export_path), save=False)
    # _kit_level.to_file(str(export_path))
    
    print(f"\nExported level to {export_path} with {len(objects)} objects in {_time_since_last():.3f} seconds.\n")
    
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
    
    print(f"\nExported to live editor with {len(objects)} objects in {_time_since_last():.3f} seconds.\n")
    
    new.reset_all()
    objects.clear()
    _live_editor = None